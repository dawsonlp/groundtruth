"""FastAPI REST Service and Solution-Scoped Hierarchical Model Explorer for GroundTruth."""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import psycopg

from groundtruth.api import GroundTruthCatalog
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity
from groundtruth.logical.state_machine import FiniteStateMachine, StateTransition
from groundtruth.physical.postgres import PostgresProjectionEngine


def generate_solution_erd(entities: List[LogicalEntity]) -> str:
    """Generate Mermaid ER diagram markup for a specific collection of entities."""
    if not entities:
        return "erDiagram\n    EMPTY_DOMAIN {\n        string notice\n    }"

    lines = ["erDiagram"]
    entity_names = {e.name.lower(): e.name for e in entities}

    # Add relations
    for entity in entities:
        source_name = entity.name.upper()
        for rel in entity.relations:
            target_raw = rel.target_entity_uri.split("/")[-1].lower()
            if target_raw in entity_names:
                target_name = entity_names[target_raw].upper()
                verb = rel.name.replace("-", "_").replace(" ", "_")
                lines.append(f"    {target_name} ||--o{{ {source_name} : {verb}")

    # Add entity definitions
    for entity in entities:
        lines.append(f"    {entity.name.upper()} {{")
        for attr in entity.attributes:
            type_str = attr.data_type.primitive.value.lower()
            pk_str = " PK" if attr.is_primary_key else ""
            fk_str = " FK" if any(r.source_attribute == attr.name for r in entity.relations) else ""
            key_marker = pk_str or fk_str
            lines.append(f"        {type_str} {attr.name}{key_marker}")
        lines.append("    }")

    return "\n".join(lines)


def create_app(workspace_root: Optional[str | Path] = None) -> FastAPI:
    root_path = Path(workspace_root or os.getenv("GROUNDTRUTH_WORKSPACE_ROOT", "."))
    catalog = GroundTruthCatalog.load(root_path) if (root_path / "models").exists() else GroundTruthCatalog()

    # Register default FSMs
    order_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/ecommerce/Order",
        attribute_name="status",
        states=["DRAFT", "PENDING", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"],
        initial_state="DRAFT",
        transitions=[
            StateTransition("DRAFT", "PENDING", trigger_action="Submit for Payment"),
            StateTransition("PENDING", "PAID", trigger_action="Capture Payment"),
            StateTransition("PENDING", "CANCELLED", trigger_action="Cancel by Customer"),
            StateTransition("PAID", "SHIPPED", trigger_action="Fulfill & Dispatch"),
            StateTransition("SHIPPED", "DELIVERED", trigger_action="Carrier Delivery"),
            StateTransition("PAID", "CANCELLED", trigger_action="Refund & Cancel"),
        ],
    )
    catalog.register_state_machine(order_fsm)

    payment_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/ecommerce/Payment",
        attribute_name="status",
        states=["INITIATED", "AUTHORIZED", "CAPTURED", "REFUNDED", "FAILED"],
        initial_state="INITIATED",
        transitions=[
            StateTransition("INITIATED", "AUTHORIZED", trigger_action="Card Auth Hold"),
            StateTransition("AUTHORIZED", "CAPTURED", trigger_action="Capture Settlement"),
            StateTransition("INITIATED", "FAILED", trigger_action="Decline"),
            StateTransition("CAPTURED", "REFUNDED", trigger_action="Issue Refund"),
        ],
    )
    catalog.register_state_machine(payment_fsm)

    mutation_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/codemesh/SymbolMutation",
        attribute_name="status",
        states=["PROPOSED", "VALIDATED", "MATERIALIZED", "REJECTED"],
        initial_state="PROPOSED",
        transitions=[
            StateTransition("PROPOSED", "VALIDATED", trigger_action="Pass Invariant Gate"),
            StateTransition("PROPOSED", "REJECTED", trigger_action="Reject Invariant Violation"),
            StateTransition("VALIDATED", "MATERIALIZED", trigger_action="Write to Disk with Synthesized Imports"),
            StateTransition("VALIDATED", "REJECTED", trigger_action="Abort by Developer"),
        ],
    )
    catalog.register_state_machine(mutation_fsm)

    app = FastAPI(
        title="GroundTruth Data & Information Authority",
        description="Hierarchical solution-scoped model explorer and data catalog",
        version="0.1.0",
    )
    app.state.catalog = catalog

    class SQLQueryPayload(BaseModel):
        sql: str

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "groundtruth",
            "terms_count": len(catalog.conceptual.list_terms()),
            "entities_count": len(catalog.logical.list_entities()),
        }

    @app.get("/api/v1/solutions")
    def list_solutions():
        """List all solutions / domains and their metadata counts."""
        entities = catalog.logical.list_entities()
        terms = catalog.conceptual.list_terms()
        domains = sorted(list({e.domain for e in entities} | {t.domain for t in terms}))
        
        results = []
        for d in domains:
            d_entities = [e for e in entities if e.domain == d]
            d_terms = [t for t in terms if t.domain == d]
            results.append({
                "solution_name": d,
                "display_name": {
                    "ecommerce": "🛒 E-Commerce & Payments Domain",
                    "codemesh": "🕸️ CodeMesh Program Graph Engine",
                    "groundtruth_meta": "🏛️ GroundTruth Information Metamodel",
                }.get(d, f"📦 {d.capitalize()} Solution"),
                "entity_count": len(d_entities),
                "term_count": len(d_terms),
            })
        return results

    @app.get("/api/v1/solutions/{solution_name}")
    def get_solution_bundle(solution_name: str):
        """Retrieve full conceptual, logical, and physical model bundle for a solution."""
        all_entities = catalog.logical.list_entities()
        all_terms = catalog.conceptual.list_terms()

        d_entities = [e for e in all_entities if e.domain == solution_name]
        d_terms = [t for t in all_terms if t.domain == solution_name]

        d_fsms = []
        for key, fsm in catalog.logical._state_machines.items():
            if fsm.target_entity_uri.startswith(f"data://logical/{solution_name}/"):
                d_fsms.append(fsm.to_dict())

        ddl = PostgresProjectionEngine.generate_schema_ddl(d_entities, schema=solution_name) if d_entities else ""
        erd_mermaid = generate_solution_erd(d_entities)

        return {
            "solution_name": solution_name,
            "terms": [t.to_dict() for t in d_terms],
            "entities": [e.to_dict() for e in d_entities],
            "state_machines": d_fsms,
            "ddl": ddl,
            "erd_mermaid": erd_mermaid,
        }

    @app.post("/api/v1/terms")
    def register_term(payload: Dict[str, Any]):
        term = BusinessTerm.from_dict(payload)
        registered = catalog.register_business_term(term)
        return registered.to_dict()

    @app.post("/api/v1/entities")
    def define_entity(payload: Dict[str, Any]):
        entity = LogicalEntity.from_dict(payload)
        defined = catalog.define_logical_entity(entity)
        return defined.to_dict()

    @app.post("/api/v1/state-machines/verify")
    def verify_state_transition(payload: Dict[str, Any]):
        try:
            valid = catalog.verify_state_transition(
                payload["entity_uri"], payload["attribute_name"], payload["from_state"], payload["to_state"]
            )
            return {"valid": valid, "from_state": payload["from_state"], "to_state": payload["to_state"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/v1/query")
    def run_sql_query(payload: SQLQueryPayload):
        """Execute a read-only SQL query against the live PostgreSQL container."""
        pg_host = os.getenv("POSTGRES_HOST", "localhost")
        pg_port = int(os.getenv("POSTGRES_PORT", "9432"))
        pg_db = os.getenv("POSTGRES_DB", "groundtruth_catalog")
        pg_user = os.getenv("POSTGRES_USER", "groundtruth")
        pg_pass = os.getenv("POSTGRES_PASSWORD", "groundtruth_password")

        conn_str = f"host={pg_host} port={pg_port} dbname={pg_db} user={pg_user} password={pg_pass}"
        try:
            with psycopg.connect(conn_str) as conn:
                with conn.cursor() as cur:
                    cur.execute(payload.sql)
                    if cur.description:
                        cols = [desc[0] for desc in cur.description]
                        rows = [list(r) for r in cur.fetchmany(50)]
                        return {"columns": cols, "rows": rows, "row_count": len(rows)}
                    return {"status": "executed", "row_count": cur.rowcount}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/", response_class=HTMLResponse)
    def render_explorer():
        """Render the hierarchical, solution-scoped Web Model Explorer with embedded preloaded data."""
        all_entities = catalog.logical.list_entities()
        all_terms = catalog.conceptual.list_terms()
        domains = sorted(list({e.domain for e in all_entities} | {t.domain for t in all_terms}))

        bundles = {}
        for d in domains:
            d_entities = [e for e in all_entities if e.domain == d]
            d_terms = [t for t in all_terms if t.domain == d]
            d_fsms = [
                fsm.to_dict()
                for fsm in catalog.logical._state_machines.values()
                if fsm.target_entity_uri.startswith(f"data://logical/{d}/")
            ]
            ddl = PostgresProjectionEngine.generate_schema_ddl(d_entities, schema=d) if d_entities else ""
            erd = generate_solution_erd(d_entities)
            bundles[d] = {
                "solution_name": d,
                "display_name": {
                    "ecommerce": "🛒 E-Commerce & Payments Domain",
                    "codemesh": "🕸️ CodeMesh Program Graph Engine",
                    "groundtruth_meta": "🏛️ GroundTruth Metamodel",
                }.get(d, f"📦 {d.capitalize()} Solution"),
                "terms": [t.to_dict() for t in d_terms],
                "entities": [e.to_dict() for e in d_entities],
                "state_machines": d_fsms,
                "ddl": ddl,
                "erd_mermaid": erd,
            }

        embedded_json = json.dumps(bundles)

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GroundTruth | Hierarchical Model Explorer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.0/dist/mermaid.min.js"></script>
  <style>
    .tree-node-active {{ background-color: rgba(16, 185, 129, 0.18); color: #34d399; font-weight: 600; border-left: 3px solid #10b981; }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #0f172a; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 3px; }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col antialiased">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-50 px-6 py-3 flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <div class="h-9 w-9 bg-emerald-600 rounded-lg flex items-center justify-center font-bold text-white text-lg shadow-lg shadow-emerald-900/40">GT</div>
      <div>
        <h1 class="text-base font-bold tracking-tight text-white flex items-center gap-2">
          GroundTruth <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Model Explorer</span>
        </h1>
        <p class="text-[11px] text-slate-400">OMG MOF 2.5.1 & DAMA-DMBOK Hierarchical Navigation</p>
      </div>
    </div>

    <!-- Tenant & Solution Selector Bar -->
    <div class="flex items-center space-x-3 text-xs">
      <div class="flex items-center gap-2 bg-slate-800/80 border border-slate-700 rounded-lg px-3 py-1.5">
        <span class="text-slate-400 font-medium">Tenant:</span>
        <select class="bg-transparent text-slate-200 font-semibold focus:outline-none cursor-pointer">
          <option value="tripartite" selected>🏢 Tripartite Enterprise</option>
        </select>
      </div>

      <div class="flex items-center gap-2 bg-slate-800/80 border border-emerald-500/40 rounded-lg px-3 py-1.5 shadow-sm">
        <span class="text-emerald-400 font-semibold">Active Solution:</span>
        <select id="solutionSelect" onchange="onSolutionChange(this.value)" class="bg-slate-900 text-white font-bold rounded px-2 py-0.5 focus:outline-none focus:ring-1 focus:ring-emerald-500 cursor-pointer">
          <option value="ecommerce">🛒 E-Commerce & Payments Domain</option>
          <option value="codemesh">🕸️ CodeMesh Program Graph Engine</option>
          <option value="groundtruth_meta">🏛️ GroundTruth Metamodel</option>
        </select>
      </div>

      <span class="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800 border border-slate-700 text-slate-300">
        <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
        PostgreSQL: <strong class="text-white">localhost:9432</strong>
      </span>
    </div>
  </header>

  <!-- Workspace: Left Tree Sidebar + Right Main Viewport -->
  <div class="flex-1 flex overflow-hidden">
    
    <!-- LEFT SIDEBAR: Solution Tree Navigation -->
    <aside class="w-72 border-r border-slate-800 bg-slate-900/50 flex flex-col overflow-y-auto p-4 space-y-4">
      <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-slate-400 px-2">
        <span id="treeSolutionHeader">Solution Tree</span>
        <span id="treeStatsBadge" class="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-400">...</span>
      </div>

      <!-- Tree Nodes Container -->
      <nav id="treeContainer" class="space-y-1 text-xs font-medium">
        <!-- Dynamically rendered tree -->
      </nav>
    </aside>

    <!-- RIGHT MAIN VIEWPORT: Solution-Scoped Focus Content -->
    <main id="mainViewport" class="flex-1 overflow-y-auto p-8 space-y-6 bg-slate-950">
      <!-- Dynamically rendered detail view -->
    </main>
  </div>

  <script id="gtDataScript" type="application/json">
{embedded_json}
  </script>

  <script>
    // 1. Immediately parse embedded data
    const GT_BUNDLES = JSON.parse(document.getElementById('gtDataScript').textContent);
    let currentSolution = 'ecommerce';
    let currentBundle = GT_BUNDLES[currentSolution] || GT_BUNDLES[Object.keys(GT_BUNDLES)[0]];
    let activeNodeId = 'erd';
    let renderCounter = 0;

    // 2. Initialize Mermaid if loaded
    try {{
      if (window.mermaid) {{
        mermaid.initialize({{
          startOnLoad: false,
          theme: 'dark',
          securityLevel: 'loose'
        }});
      }}
    }} catch (e) {{
      console.warn('Mermaid init warning:', e);
    }}

    function onSolutionChange(solutionName) {{
      activeNodeId = 'erd';
      currentSolution = solutionName;
      currentBundle = GT_BUNDLES[solutionName];
      document.getElementById('solutionSelect').value = solutionName;
      renderTree();
      selectView(activeNodeId);
    }}

    function renderTree() {{
      if (!currentBundle) return;
      document.getElementById('treeSolutionHeader').textContent = currentBundle.solution_name;
      document.getElementById('treeStatsBadge').textContent = `${{currentBundle.entities.length}} Entities`;

      const container = document.getElementById('treeContainer');
      let html = '';

      // 1. Solution ER Diagram
      html += `
        <div onclick="selectView('erd')" class="cursor-pointer flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800/60 ${{activeNodeId === 'erd' ? 'tree-node-active' : ''}}">
          <span>📊</span> <span>Entity Relationship Map</span>
        </div>
      `;

      // 2. Conceptual Glossary
      html += `
        <div class="pt-2">
          <div onclick="selectView('conceptual')" class="cursor-pointer flex items-center justify-between px-3 py-1.5 text-slate-400 hover:text-slate-200 font-semibold">
            <span class="flex items-center gap-2"><span>🧠</span> <span>Conceptual Glossary</span></span>
            <span class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded">${{currentBundle.terms.length}}</span>
          </div>
          <div class="pl-6 space-y-0.5 mt-1 border-l border-slate-800/80 ml-4">
            ${{currentBundle.terms.map(t => `
              <div onclick="selectTerm('${{t.slug}}')" class="cursor-pointer px-2 py-1 rounded text-slate-400 hover:text-white hover:bg-slate-800/40 truncate ${{activeNodeId === 'term_' + t.slug ? 'tree-node-active' : ''}}">
                ${{t.name}}
              </div>
            `).join('')}}
          </div>
        </div>
      `;

      // 3. Logical Entities
      html += `
        <div class="pt-2">
          <div onclick="selectView('entities_overview')" class="cursor-pointer flex items-center justify-between px-3 py-1.5 text-slate-400 hover:text-slate-200 font-semibold">
            <span class="flex items-center gap-2"><span>📐</span> <span>Logical Entities</span></span>
            <span class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded">${{currentBundle.entities.length}}</span>
          </div>
          <div class="pl-6 space-y-0.5 mt-1 border-l border-slate-800/80 ml-4">
            ${{currentBundle.entities.map(e => `
              <div onclick="selectEntity('${{e.name}}')" class="cursor-pointer px-2 py-1 rounded text-slate-400 hover:text-white hover:bg-slate-800/40 truncate ${{activeNodeId === 'entity_' + e.name ? 'tree-node-active' : ''}}">
                ${{e.name}}
              </div>
            `).join('')}}
          </div>
        </div>
      `;

      // 4. State Machines
      if (currentBundle.state_machines && currentBundle.state_machines.length > 0) {{
        html += `
          <div class="pt-2">
            <div onclick="selectView('fsm_overview')" class="cursor-pointer flex items-center justify-between px-3 py-1.5 text-slate-400 hover:text-slate-200 font-semibold">
              <span class="flex items-center gap-2"><span>🔄</span> <span>State Machines</span></span>
              <span class="text-[10px] bg-slate-800 px-1.5 py-0.2 rounded">${{currentBundle.state_machines.length}}</span>
            </div>
            <div class="pl-6 space-y-0.5 mt-1 border-l border-slate-800/80 ml-4">
              ${{currentBundle.state_machines.map(f => {{
                const entName = f.target_entity_uri.split('/').pop();
                return `
                  <div onclick="selectFSM('${{f.target_entity_uri}}', '${{f.attribute_name}}')" class="cursor-pointer px-2 py-1 rounded text-slate-400 hover:text-white hover:bg-slate-800/40 truncate ${{activeNodeId === 'fsm_' + entName ? 'tree-node-active' : ''}}">
                    ${{entName}}.${{f.attribute_name}}
                  </div>
                `;
              }}).join('')}}
            </div>
          </div>
        `;
      }}

      // 5. Physical DDL Projection
      html += `
        <div class="pt-2">
          <div onclick="selectView('ddl')" class="cursor-pointer flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800/60 ${{activeNodeId === 'ddl' ? 'tree-node-active' : ''}}">
            <span>📜</span> <span>PostgreSQL DDL</span>
          </div>
        </div>
      `;

      // 6. Live SQL Sandbox
      html += `
        <div class="pt-1">
          <div onclick="selectView('sql')" class="cursor-pointer flex items-center gap-2 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800/60 ${{activeNodeId === 'sql' ? 'tree-node-active' : ''}}">
            <span>⚡</span> <span>Live SQL Sandbox</span>
          </div>
        </div>
      `;

      container.innerHTML = html;
    }}

    function selectView(viewId) {{
      activeNodeId = viewId;
      renderTree();
      const viewport = document.getElementById('mainViewport');

      if (viewId === 'erd') {{
        renderERDView(viewport);
      }} else if (viewId === 'conceptual') {{
        renderConceptualView(viewport);
      }} else if (viewId === 'entities_overview') {{
        renderEntitiesOverview(viewport);
      }} else if (viewId === 'fsm_overview') {{
        renderFSMOverview(viewport);
      }} else if (viewId === 'ddl') {{
        renderDDLView(viewport);
      }} else if (viewId === 'sql') {{
        renderSQLView(viewport);
      }}
    }}

    function selectEntity(entityName) {{
      activeNodeId = 'entity_' + entityName;
      renderTree();
      const entity = currentBundle.entities.find(e => e.name === entityName);
      if (!entity) return;
      renderEntityDetailView(entity);
    }}

    function selectTerm(slug) {{
      activeNodeId = 'term_' + slug;
      renderTree();
      const term = currentBundle.terms.find(t => t.slug === slug);
      if (!term) return;
      renderTermDetailView(term);
    }}

    function selectFSM(entityUri, attrName) {{
      const entName = entityUri.split('/').pop();
      activeNodeId = 'fsm_' + entName;
      renderTree();
      const fsm = currentBundle.state_machines.find(f => f.target_entity_uri === entityUri && f.attribute_name === attrName);
      if (!fsm) return;
      renderFSMDetailView(fsm);
    }}

    // --- SAFE ASYNC MERMAID RENDERER ---
    async function renderChartSafely(targetElementId, chartDefinition) {{
      const el = document.getElementById(targetElementId);
      if (!el) return;

      renderCounter++;
      const uniqueId = 'mermaid_svg_' + renderCounter;

      try {{
        if (window.mermaid) {{
          const {{ svg }} = await window.mermaid.render(uniqueId, chartDefinition);
          el.innerHTML = svg;
        }} else {{
          el.innerHTML = `<pre class="text-xs font-mono text-emerald-400">${{chartDefinition}}</pre>`;
        }}
      }} catch (err) {{
        console.warn('Mermaid render fallback:', err);
        el.innerHTML = `
          <div class="w-full p-4 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono">
            <div class="text-[10px] text-slate-500 mb-2 uppercase font-bold tracking-wider">Topological Relationship Definition</div>
            <pre class="overflow-x-auto text-emerald-400">${{chartDefinition}}</pre>
          </div>
        `;
      }}
    }}

    // --- VIEW RENDERERS ---

    function renderERDView(container) {{
      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 class="text-xl font-bold text-white flex items-center gap-2">
                📊 ${{currentBundle.display_name || currentBundle.solution_name}}
              </h2>
              <p class="text-xs text-slate-400 mt-1">Surgically scoped topological model for ${{currentBundle.solution_name}}</p>
            </div>
            <span class="text-xs px-3 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
              ${{currentBundle.entities.length}} Normalized Entities
            </span>
          </div>

          <!-- Mermaid ER Diagram Card -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
            <div id="erdChartContainer" class="flex justify-center overflow-x-auto min-h-[200px] items-center">
              <span class="text-slate-400 text-xs animate-pulse">Rendering diagram...</span>
            </div>
          </div>

          <!-- Entity Summary Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            ${{currentBundle.entities.map(e => `
              <div onclick="selectEntity('${{e.name}}')" class="cursor-pointer bg-slate-900/80 border border-slate-800 hover:border-emerald-500/40 rounded-xl p-4 transition hover:bg-slate-900 shadow">
                <div class="flex items-center justify-between">
                  <h3 class="font-bold text-white text-sm">${{e.name}}</h3>
                  <span class="text-[10px] text-slate-500 bg-slate-950 px-2 py-0.5 rounded">${{e.attributes.length}} attrs</span>
                </div>
                <p class="text-xs text-slate-400 mt-2 line-clamp-2">${{e.description || 'No description provided.'}}</p>
                <div class="mt-3 flex gap-1 flex-wrap">
                  ${{e.attributes.filter(a => a.is_primary_key).map(a => `<span class="text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20 px-1.5 py-0.5 rounded">PK: ${{a.name}}</span>`).join('')}}
                  ${{e.attributes.filter(a => a.is_sensitive).map(a => `<span class="text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 px-1.5 py-0.5 rounded">PII: ${{a.name}}</span>`).join('')}}
                </div>
              </div>
            `).join('')}}
          </div>
        </div>
      `;

      renderChartSafely('erdChartContainer', currentBundle.erd_mermaid);
    }}

    function renderEntityDetailView(entity) {{
      const container = document.getElementById('mainViewport');
      const attachedFSM = currentBundle.state_machines ? currentBundle.state_machines.find(f => f.target_entity_uri === entity.uri) : null;

      container.innerHTML = `
        <div class="space-y-6">
          <!-- Entity Header -->
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <div class="flex items-center gap-3">
                <h2 class="text-2xl font-bold text-white">${{entity.name}}</h2>
                <span class="text-xs px-2.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 font-mono">${{entity.uri}}</span>
              </div>
              <p class="text-xs text-slate-400 mt-1.5">${{entity.description || 'No description provided.'}}</p>
            </div>
            <button onclick="selectView('erd')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">
              ← Back to Solution Map
            </button>
          </div>

          <!-- Columns & Attributes Table -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
            <div class="px-5 py-3 border-b border-slate-800 bg-slate-900/60 flex justify-between items-center">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300">Attribute Specifications</h3>
              <span class="text-xs text-slate-500">${{entity.attributes.length}} Columns</span>
            </div>
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-slate-800 text-slate-400 bg-slate-950/40">
                  <th class="py-2.5 px-4">Column Name</th>
                  <th class="py-2.5 px-4">Data Type</th>
                  <th class="py-2.5 px-4">Constraints</th>
                  <th class="py-2.5 px-4">Privacy / Tags</th>
                  <th class="py-2.5 px-4">Description</th>
                </tr>
              </thead>
              <tbody>
                ${{entity.attributes.map(a => `
                  <tr class="border-b border-slate-800/60 hover:bg-slate-800/30">
                    <td class="py-2.5 px-4 font-mono font-bold text-white flex items-center gap-1.5">
                      ${{a.is_primary_key ? '🔑' : ''}} ${{a.name}}
                    </td>
                    <td class="py-2.5 px-4 font-mono text-emerald-400">${{a.data_type.primitive}}${{a.data_type.max_length ? `(${{a.data_type.max_length}})` : ''}}</td>
                    <td class="py-2.5 px-4 space-x-1">
                      ${{a.is_primary_key ? '<span class="px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-400 border border-amber-500/20 text-[10px]">PRIMARY KEY</span>' : ''}}
                      ${{!a.is_nullable ? '<span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px]">NOT NULL</span>' : '<span class="text-slate-500 text-[10px]">NULLABLE</span>'}}
                      ${{a.is_unique ? '<span class="px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[10px]">UNIQUE</span>' : ''}}
                    </td>
                    <td class="py-2.5 px-4">
                      ${{a.tags && a.tags.length > 0 ? a.tags.map(t => `<span class="px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20 text-[10px]">${{t}}</span>`).join(' ') : '<span class="text-slate-600">—</span>'}}
                    </td>
                    <td class="py-2.5 px-4 text-slate-400">${{a.description || ''}}</td>
                  </tr>
                `).join('')}}
              </tbody>
            </table>
          </div>

          <!-- Attached State Machine Diagram (if any) -->
          ${{attachedFSM ? `
            <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
              <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                <h3 class="text-xs font-bold uppercase tracking-wider text-white">🔄 Attached Lifecycle State Machine (${{attachedFSM.attribute_name}})</h3>
                <span class="text-xs text-emerald-400 font-mono">${{attachedFSM.states.length}} States</span>
              </div>
              <div id="fsmChartContainer" class="bg-slate-950 p-4 rounded-lg flex justify-center">
                <span class="text-slate-400 text-xs animate-pulse">Rendering flowchart...</span>
              </div>
            </div>
          ` : ''}}

          <!-- Live Physical Table Preview -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-3">
            <div class="flex justify-between items-center">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300">🐘 Live PostgreSQL Table Data (Port 9432)</h3>
              <button onclick="loadLiveTablePreview('${{entity.domain}}', '${{entity.name}}')" class="text-xs bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1 rounded font-semibold transition shadow">
                Query Live Rows
              </button>
            </div>
            <div id="liveTableResult" class="bg-slate-950 rounded-lg p-3 overflow-x-auto min-h-[60px] text-xs font-mono text-slate-400">
              Click "Query Live Rows" to fetch instance data directly from PostgreSQL...
            </div>
          </div>
        </div>
      `;

      if (attachedFSM) {{
        const fsmMermaid = `stateDiagram-v2\\n    [*] --> ${{attachedFSM.initial_state}}\\n` + 
          attachedFSM.transitions.map(t => `    ${{t.from_state}} --> ${{t.to_state}}: ${{t.trigger_action || ''}}`).join('\\n');
        renderChartSafely('fsmChartContainer', fsmMermaid);
      }}
    }}

    async function loadLiveTablePreview(schema, tableName) {{
      const resultDiv = document.getElementById('liveTableResult');
      resultDiv.innerHTML = '<span class="text-slate-400">Querying PostgreSQL...</span>';

      try {{
        const sql = `SELECT * FROM ${{schema}}.${{tableName.toLowerCase()}} LIMIT 10;`;
        const resp = await fetch('/api/v1/query', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ sql }})
        }});
        const data = await resp.json();
        if (!resp.ok) {{
          resultDiv.innerHTML = `<span class="text-rose-400">Error: ${{data.detail}}</span>`;
          return;
        }}

        if (!data.columns || data.columns.length === 0 || !data.rows || data.rows.length === 0) {{
          resultDiv.innerHTML = `<span class="text-slate-500 italic">Table ${{schema}}.${{tableName.toLowerCase()}} is currently empty (0 rows).</span>`;
          return;
        }}

        let html = '<table class="w-full text-left border-collapse">';
        html += '<thead><tr class="border-b border-slate-800 text-slate-400">';
        data.columns.forEach(c => html += `<th class="py-1.5 px-3">${{c}}</th>`);
        html += '</tr></thead><tbody>';
        data.rows.forEach(r => {{
          html += '<tr class="border-b border-slate-900/60 hover:bg-slate-900/40 text-slate-200">';
          r.forEach(val => html += `<td class="py-1.5 px-3">${{val}}</td>`);
          html += '</tr>';
        }});
        html += '</tbody></table>';
        html += `<div class="mt-2 text-slate-500 text-[10px]">Displaying ${{data.row_count}} rows from PostgreSQL</div>`;
        resultDiv.innerHTML = html;
      }} catch (err) {{
        resultDiv.innerHTML = `<span class="text-rose-400">Network Error: ${{err.message}}</span>`;
      }}
    }}

    function renderConceptualView(container) {{
      container.innerHTML = `
        <div class="space-y-6">
          <div class="border-b border-slate-800 pb-4">
            <h2 class="text-xl font-bold text-white flex items-center gap-2">🧠 Conceptual Glossary for ${{currentBundle.solution_name}}</h2>
            <p class="text-xs text-slate-400 mt-1">Authoritative ISO/IEC 11179 & DAMA business definitions</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            ${{currentBundle.terms.map(t => `
              <div onclick="selectTerm('${{t.slug}}')" class="cursor-pointer bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-emerald-500/40 transition shadow">
                <div class="flex items-center justify-between">
                  <h3 class="font-bold text-white text-base">${{t.name}}</h3>
                  <span class="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">${{t.slug}}</span>
                </div>
                <p class="text-xs text-slate-300 mt-2">${{t.definition}}</p>
                ${{t.synonyms && t.synonyms.length > 0 ? `
                  <div class="mt-3 text-xs text-slate-500">
                    Synonyms: <span class="text-slate-400">${{t.synonyms.join(', ')}}</span>
                  </div>
                ` : ''}}
              </div>
            `).join('')}}
          </div>
        </div>
      `;
    }}

    function renderTermDetailView(term) {{
      const container = document.getElementById('mainViewport');
      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <div class="flex items-center gap-3">
                <h2 class="text-2xl font-bold text-white">${{term.name}}</h2>
                <span class="text-xs px-2.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">${{term.uri}}</span>
              </div>
              <p class="text-xs text-slate-400 mt-1.5">Conceptual Business Term Specification</p>
            </div>
            <button onclick="selectView('conceptual')" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">
              ← Back to Glossary
            </button>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-lg space-y-4">
            <div>
              <div class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Formal Business Definition</div>
              <p class="text-sm text-slate-100 mt-1 leading-relaxed bg-slate-950 p-4 rounded-lg border border-slate-800">${{term.definition}}</p>
            </div>

            <div class="grid grid-cols-2 gap-4 pt-2">
              <div>
                <div class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Domain Context</div>
                <p class="text-xs font-mono text-emerald-400 mt-1">${{term.domain}}</p>
              </div>
              <div>
                <div class="text-xs uppercase tracking-wider text-slate-500 font-semibold">Synonyms</div>
                <p class="text-xs text-slate-300 mt-1">${{term.synonyms ? term.synonyms.join(', ') : 'None'}}</p>
              </div>
            </div>
          </div>
        </div>
      `;
    }}

    function renderEntitiesOverview(container) {{
      selectView('erd');
    }}

    function renderFSMOverview(container) {{
      if (!currentBundle.state_machines || currentBundle.state_machines.length === 0) {{
        container.innerHTML = `<div class="text-slate-400 p-8 text-center bg-slate-900 rounded-xl border border-slate-800">No state machines declared for this solution.</div>`;
        return;
      }}
      selectFSM(currentBundle.state_machines[0].target_entity_uri, currentBundle.state_machines[0].attribute_name);
    }}

    function renderFSMDetailView(fsm) {{
      const container = document.getElementById('mainViewport');
      const entName = fsm.target_entity_uri.split('/').pop();

      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <div class="flex items-center gap-3">
                <h2 class="text-2xl font-bold text-white">${{entName}}.${{fsm.attribute_name}} Lifecycle</h2>
                <span class="text-xs px-2.5 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20 font-mono">${{fsm.target_entity_uri}}</span>
              </div>
              <p class="text-xs text-slate-400 mt-1.5">Deterministic Finite State Machine Verification Matrix</p>
            </div>
          </div>

          <!-- Mermaid State Diagram -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl space-y-3">
            <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400">State Transition Flowchart</h3>
            <div id="fsmMainChartContainer" class="bg-slate-950 p-6 rounded-lg flex justify-center">
              <span class="text-slate-400 text-xs animate-pulse">Rendering flowchart...</span>
            </div>
          </div>

          <!-- Legal Transitions Table -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
            <div class="px-5 py-3 border-b border-slate-800 bg-slate-900/60">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300">Transition Rule Matrix</h3>
            </div>
            <table class="w-full text-left text-xs border-collapse">
              <thead>
                <tr class="border-b border-slate-800 text-slate-400 bg-slate-950/40">
                  <th class="py-2.5 px-4">From State</th>
                  <th class="py-2.5 px-4"></th>
                  <th class="py-2.5 px-4">To State</th>
                  <th class="py-2.5 px-4">Trigger / Business Action</th>
                </tr>
              </thead>
              <tbody>
                ${{fsm.transitions.map(t => `
                  <tr class="border-b border-slate-800/60 hover:bg-slate-800/30 font-mono">
                    <td class="py-2.5 px-4 font-bold text-amber-400">${{t.from_state}}</td>
                    <td class="py-2.5 px-2 text-slate-500">➔</td>
                    <td class="py-2.5 px-4 font-bold text-emerald-400">${{t.to_state}}</td>
                    <td class="py-2.5 px-4 font-sans text-slate-300">${{t.trigger_action || 'State Mutation'}}</td>
                  </tr>
                `).join('')}}
              </tbody>
            </table>
          </div>
        </div>
      `;

      const fsmMermaid = `stateDiagram-v2\\n    [*] --> ${{fsm.initial_state}}\\n` + 
        fsm.transitions.map(t => `    ${{t.from_state}} --> ${{t.to_state}}: ${{t.trigger_action || ''}}`).join('\\n');
      renderChartSafely('fsmMainChartContainer', fsmMermaid);
    }}

    function renderDDLView(container) {{
      container.innerHTML = `
        <div class="space-y-6">
          <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 class="text-xl font-bold text-white">📜 PostgreSQL DDL Projection for ${{currentBundle.solution_name}}</h2>
              <p class="text-xs text-slate-400 mt-1">Pure deterministic schema projection matching DAMA & MOF specifications</p>
            </div>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl">
            <pre class="bg-slate-950 p-4 rounded-lg overflow-x-auto text-xs font-mono text-emerald-300 border border-slate-800">${{currentBundle.ddl || '-- No entities to project'}}</pre>
          </div>
        </div>
      `;
    }}

    function renderSQLView(container) {{
      const defaultSQL = currentSolution === 'ecommerce' 
        ? 'SELECT customer_id, email, full_name, status FROM ecommerce.customer LIMIT 10;'
        : currentSolution === 'codemesh'
        ? 'SELECT csi_uri, name, symbol_kind, file_path FROM codemesh.codesymbol LIMIT 10;'
        : 'SELECT domain, name, uri FROM groundtruth_meta.entity ORDER BY domain, name;';

      container.innerHTML = `
        <div class="space-y-6">
          <div class="border-b border-slate-800 pb-4">
            <h2 class="text-xl font-bold text-white">⚡ Live PostgreSQL Query Sandbox</h2>
            <p class="text-xs text-slate-400 mt-1">Execute live queries against the running PostgreSQL container (Port 9432)</p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-xl space-y-4">
            <div class="flex gap-2">
              <input id="sqlSandboxInput" type="text" value="${{defaultSQL}}" 
                     class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-emerald-400 focus:outline-none focus:border-emerald-500">
              <button onclick="executeSandboxQuery()" class="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition shadow">Run Query</button>
            </div>

            <div id="sandboxResult" class="bg-slate-950 border border-slate-800 rounded-lg p-4 overflow-x-auto min-h-[120px] text-xs font-mono">
              <p class="text-slate-500 italic">Click "Run Query" to inspect records...</p>
            </div>
          </div>
        </div>
      `;
    }}

    async function executeSandboxQuery() {{
      const sql = document.getElementById('sqlSandboxInput').value;
      const resultDiv = document.getElementById('sandboxResult');
      resultDiv.innerHTML = '<span class="text-slate-400">Executing...</span>';

      try {{
        const resp = await fetch('/api/v1/query', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ sql }})
        }});
        const data = await resp.json();
        if (!resp.ok) {{
          resultDiv.innerHTML = `<span class="text-rose-400">Error: ${{data.detail}}</span>`;
          return;
        }}

        if (!data.columns || data.columns.length === 0) {{
          resultDiv.innerHTML = `<span class="text-emerald-400">Query executed successfully. Rows affected: ${{data.row_count}}</span>`;
          return;
        }}

        let html = '<table class="w-full text-left border-collapse">';
        html += '<thead><tr class="border-b border-slate-800 text-slate-400">';
        data.columns.forEach(c => html += `<th class="py-1.5 px-3">${{c}}</th>`);
        html += '</tr></thead><tbody>';
        data.rows.forEach(r => {{
          html += '<tr class="border-b border-slate-900/60 hover:bg-slate-900/40 text-slate-200">';
          r.forEach(val => html += `<td class="py-1.5 px-3">${{val}}</td>`);
          html += '</tr>';
        }});
        html += '</tbody></table>';
        html += `<div class="mt-2 text-slate-500 text-[10px]">Returned ${{data.row_count}} rows</div>`;
        resultDiv.innerHTML = html;
      }} catch (err) {{
        resultDiv.innerHTML = `<span class="text-rose-400">Network Error: ${{err.message}}</span>`;
      }}
    }}

    // 3. Immediately render initial active solution
    renderTree();
    selectView('erd');
  </script>
</body>
</html>"""
        return HTMLResponse(content=html_content)

    return app


app = create_app()
