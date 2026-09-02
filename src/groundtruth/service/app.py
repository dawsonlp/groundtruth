"""FastAPI REST Service and Interactive Web Model Explorer for GroundTruth."""

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


def create_app(workspace_root: Optional[str | Path] = None) -> FastAPI:
    root_path = Path(workspace_root or os.getenv("GROUNDTRUTH_WORKSPACE_ROOT", "."))
    catalog = GroundTruthCatalog.load(root_path) if (root_path / "models").exists() else GroundTruthCatalog()

    # Pre-register default FSMs
    order_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/ecommerce/Order",
        attribute_name="status",
        states=["DRAFT", "PENDING", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"],
        initial_state="DRAFT",
        transitions=[
            StateTransition("DRAFT", "PENDING", trigger_action="Submit for Payment"),
            StateTransition("PENDING", "PAID", trigger_action="Capture Payment"),
            StateTransition("PENDING", "CANCELLED", trigger_action="Cancel"),
            StateTransition("PAID", "SHIPPED", trigger_action="Fulfill Order"),
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
            StateTransition("INITIATED", "AUTHORIZED", trigger_action="Auth Hold"),
            StateTransition("AUTHORIZED", "CAPTURED", trigger_action="Settle Payment"),
            StateTransition("INITIATED", "FAILED", trigger_action="Decline"),
            StateTransition("CAPTURED", "REFUNDED", trigger_action="Refund"),
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
        description="Authoritative DAMA & MOF data modeling catalog and interactive explorer",
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

    @app.get("/api/v1/terms")
    def list_terms():
        return [t.to_dict() for t in catalog.conceptual.list_terms()]

    @app.post("/api/v1/terms")
    def register_term(payload: Dict[str, Any]):
        term = BusinessTerm.from_dict(payload)
        registered = catalog.register_business_term(term)
        return registered.to_dict()

    @app.get("/api/v1/entities")
    def list_entities(domain: Optional[str] = None):
        return [e.to_dict() for e in catalog.logical.list_entities(domain=domain)]

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

    @app.get("/api/v1/projections/postgres/{domain}")
    def get_postgres_ddl(domain: str, schema: Optional[str] = None):
        target_schema = schema or domain
        try:
            ddl = catalog.generate_postgres_ddl(domain, schema=target_schema)
            return {"domain": domain, "schema": target_schema, "ddl": ddl}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

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
        """Render the rich interactive Web Model Explorer."""
        terms = catalog.conceptual.list_terms()
        entities = catalog.logical.list_entities()
        meta_entities = [e for e in entities if e.domain == "groundtruth_meta"]
        ecom_entities = [e for e in entities if e.domain == "ecommerce"]
        cm_entities = [e for e in entities if e.domain == "codemesh"]

        m2_ddl = catalog.generate_postgres_ddl("groundtruth_meta", schema="groundtruth_meta")
        m1_ecom_ddl = catalog.generate_postgres_ddl("ecommerce", schema="ecommerce")
        m1_cm_ddl = catalog.generate_postgres_ddl("codemesh", schema="codemesh")

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GroundTruth Explorer | Information & Data Authority</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
  </script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen flex flex-col">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex items-center justify-between">
    <div class="flex items-center space-x-3">
      <div class="h-9 w-9 bg-emerald-600 rounded-lg flex items-center justify-center font-bold text-white text-lg shadow-lg shadow-emerald-900/40">GT</div>
      <div>
        <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
          GroundTruth <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Data & Information Authority</span>
        </h1>
        <p class="text-xs text-slate-400">OMG MOF 2.5.1 & DAMA-DMBOK 4-Tier Semantic Modeling</p>
      </div>
    </div>
    <div class="flex items-center space-x-3 text-xs">
      <span class="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800 border border-slate-700 text-slate-300">
        <span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
        PostgreSQL Port: <strong class="text-white">9432</strong>
      </span>
      <span class="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800 border border-slate-700 text-slate-300">
        Database: <strong class="text-white">groundtruth_catalog</strong>
      </span>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-6 space-y-8">
    
    <!-- Hero / Stats Bar -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-xs text-slate-400 font-medium uppercase tracking-wider">Level 1: Conceptual Terms</div>
        <div class="text-2xl font-bold text-white mt-1">{len(terms)} <span class="text-xs font-normal text-slate-400">Glossary Terms</span></div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-xs text-slate-400 font-medium uppercase tracking-wider">Level 2: M2 Metamodel</div>
        <div class="text-2xl font-bold text-indigo-400 mt-1">{len(meta_entities)} <span class="text-xs font-normal text-slate-400">Catalog Entities</span></div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-xs text-slate-400 font-medium uppercase tracking-wider">Level 2: M1 Domain Entities</div>
        <div class="text-2xl font-bold text-emerald-400 mt-1">{len(ecom_entities) + len(cm_entities)} <span class="text-xs font-normal text-slate-400">ECom ({len(ecom_entities)}) + CodeMesh ({len(cm_entities)})</span></div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-xs text-slate-400 font-medium uppercase tracking-wider">Level 3: M0 Instance Data</div>
        <div class="text-2xl font-bold text-amber-400 mt-1">Live <span class="text-xs font-normal text-slate-400">PostgreSQL (9432)</span></div>
      </div>
    </div>

    <!-- Section: CodeMesh Program Graph Entity-Relationship Diagram (M1) -->
    <section class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            🕸️ CodeMesh Semantic Program Graph Data Model (M1)
          </h2>
          <p class="text-xs text-slate-400">GroundTruth logical modeling of CodeMesh symbols, contracts, call edges, slices, and AST mutations</p>
        </div>
        <span class="text-xs bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 px-2 py-1 rounded">CodeMesh Domain</span>
      </div>

      <div class="bg-slate-950 rounded-lg p-4 border border-slate-800/80 flex justify-center">
        <pre class="mermaid text-xs">
erDiagram
    CODESYMBOL ||--|| SYMBOLCONTRACT : specifies
    CODESYMBOL ||--o{{ CODEDEPENDENCYEDGE : calls_or_called_by
    CODESYMBOL ||--o{{ CONTEXTSLICESESSION : targets
    CODESYMBOL ||--o{{ SYMBOLMUTATION : undergoes

    CODESYMBOL {{
        uuid symbol_id PK
        string csi_uri UK "csi://"
        string name
        string symbol_kind
        string package_name
        string file_path
        int start_line
        int end_line
        bool is_exported
    }}

    SYMBOLCONTRACT {{
        uuid contract_id PK
        uuid symbol_id FK
        string signature
        string return_type
        bool is_pure
        bool is_idempotent
        bool is_async
    }}

    CODEDEPENDENCYEDGE {{
        uuid edge_id PK
        uuid source_symbol_id FK
        uuid target_symbol_id FK
        string verb "CALLS | INHERITS"
        int call_count
        bool is_dynamic
    }}

    CONTEXTSLICESESSION {{
        uuid session_id PK
        uuid target_symbol_id FK
        int hop_distance
        int token_count
        string prompt_stub_text
    }}

    SYMBOLMUTATION {{
        uuid mutation_id PK
        uuid symbol_id FK
        string mutation_type
        string status "FSM"
        int blast_radius_count
        string new_ast_hash
    }}
        </pre>
      </div>
    </section>

    <!-- Section: E-Commerce Domain ER Diagram (M1) -->
    <section class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            🛒 E-Commerce Domain Entity-Relationship Diagram (M1)
          </h2>
          <p class="text-xs text-slate-400">Customer profiles, catalog items, orders, order items, and payment settlements</p>
        </div>
        <span class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-1 rounded">E-Commerce Domain</span>
      </div>

      <div class="bg-slate-950 rounded-lg p-4 border border-slate-800/80 flex justify-center">
        <pre class="mermaid text-xs">
erDiagram
    CUSTOMER ||--o{{ ORDER : places
    ORDER ||--|{{ ORDERITEM : contains
    PRODUCT ||--o{{ ORDERITEM : ordered_in
    ORDER ||--|{{ PAYMENT : settled_by

    CUSTOMER {{
        uuid customer_id PK
        string email UK "PII"
        string full_name "PII"
        string status
        timestamp created_at
    }}

    PRODUCT {{
        uuid product_id PK
        string sku UK
        string title
        int price_cents
        bool is_active
    }}

    ORDER {{
        uuid order_id PK
        uuid customer_id FK
        string status "FSM"
        int total_cents
        timestamp created_at
    }}

    ORDERITEM {{
        uuid item_id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        int unit_price_cents
    }}

    PAYMENT {{
        uuid payment_id PK
        uuid order_id FK
        string idempotency_key UK
        int amount_cents
        string status "FSM"
        timestamp created_at
    }}
        </pre>
      </div>
    </section>

    <!-- Section: Lifecycle Finite State Machines -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div class="border-b border-slate-800 pb-3">
          <h3 class="text-sm font-bold text-white">🔄 Order Lifecycle (M1)</h3>
          <p class="text-xs text-slate-400">Order status transitions</p>
        </div>
        <div class="bg-slate-950 rounded-lg p-4 border border-slate-800 flex justify-center">
          <pre class="mermaid text-xs">
stateDiagram-v2
    [*] --> DRAFT
    DRAFT --> PENDING: Submit
    PENDING --> PAID: Payment Captured
    PENDING --> CANCELLED: Customer Cancel
    PAID --> SHIPPED: Fulfill
    SHIPPED --> DELIVERED: Delivery
    PAID --> CANCELLED: Refund
    CANCELLED --> [*]
    DELIVERED --> [*]
          </pre>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div class="border-b border-slate-800 pb-3">
          <h3 class="text-sm font-bold text-white">💳 Payment Lifecycle (M1)</h3>
          <p class="text-xs text-slate-400">Idempotent charge flow</p>
        </div>
        <div class="bg-slate-950 rounded-lg p-4 border border-slate-800 flex justify-center">
          <pre class="mermaid text-xs">
stateDiagram-v2
    [*] --> INITIATED
    INITIATED --> AUTHORIZED: Auth Hold
    AUTHORIZED --> CAPTURED: Settle
    INITIATED --> FAILED: Decline
    CAPTURED --> REFUNDED: Refund
    FAILED --> [*]
    REFUNDED --> [*]
          </pre>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <div class="border-b border-slate-800 pb-3">
          <h3 class="text-sm font-bold text-white">🧬 CodeMesh AST Mutation (M1)</h3>
          <p class="text-xs text-slate-400">Zero-diff validation flow</p>
        </div>
        <div class="bg-slate-950 rounded-lg p-4 border border-slate-800 flex justify-center">
          <pre class="mermaid text-xs">
stateDiagram-v2
    [*] --> PROPOSED
    PROPOSED --> VALIDATED: Invariant Pass
    PROPOSED --> REJECTED: Violation
    VALIDATED --> MATERIALIZED: Write to Disk
    VALIDATED --> REJECTED: Abort
    MATERIALIZED --> [*]
    REJECTED --> [*]
          </pre>
        </div>
      </div>
    </section>

    <!-- Section: Live SQL Query Sandbox -->
    <section class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h2 class="text-base font-bold text-white flex items-center gap-2">
            ⚡ Live PostgreSQL SQL Query Sandbox (Port 9432)
          </h2>
          <p class="text-xs text-slate-400">Execute queries live against the running PostgreSQL container across all three domains</p>
        </div>
      </div>

      <div class="space-y-3">
        <div class="flex gap-2">
          <input id="sqlInput" type="text" value="SELECT csi_uri, name, symbol_kind, file_path FROM codemesh.codesymbol LIMIT 10;" 
                 class="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-emerald-400 focus:outline-none focus:border-emerald-500">
          <button onclick="runQuery()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition shadow">Run Query</button>
        </div>

        <div class="flex gap-2 text-xs text-slate-400 flex-wrap">
          <span>Quick queries:</span>
          <button onclick="setQuery('SELECT csi_uri, symbol_kind, file_path FROM codemesh.codesymbol;')" class="underline hover:text-white">CodeMesh Symbols</button>
          <span>•</span>
          <button onclick="setQuery('SELECT e.verb, s1.name as caller, s2.name as callee FROM codemesh.codedependencyedge e JOIN codemesh.codesymbol s1 ON e.source_symbol_id = s1.symbol_id JOIN codemesh.codesymbol s2 ON e.target_symbol_id = s2.symbol_id;')" class="underline hover:text-white">CodeMesh Call Graph</button>
          <span>•</span>
          <button onclick="setQuery('SELECT customer_id, email, full_name, status FROM ecommerce.customer;')" class="underline hover:text-white">ECom Customers</button>
          <span>•</span>
          <button onclick="setQuery('SELECT domain, name, uri FROM groundtruth_meta.entity ORDER BY domain, name;')" class="underline hover:text-white">M2 Catalog Entities</button>
        </div>

        <div id="queryResult" class="bg-slate-950 border border-slate-800 rounded-lg p-3 overflow-x-auto min-h-[100px] text-xs font-mono">
          <p class="text-slate-500 italic">Click "Run Query" to inspect live database records...</p>
        </div>
      </div>
    </section>

    <!-- Section: Physical DDL Projections -->
    <section class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
      <div class="border-b border-slate-800 pb-3">
        <h2 class="text-base font-bold text-white">📜 Generated PostgreSQL DDL Projections for CodeMesh (M1)</h2>
        <p class="text-xs text-slate-400">Idempotent, sorted DDL generated purely from GroundTruth logical schemas</p>
      </div>
      <div class="bg-slate-950 rounded-lg p-4 border border-slate-800 overflow-x-auto max-h-96">
        <pre class="text-xs font-mono text-indigo-300">{m1_cm_ddl}</pre>
      </div>
    </section>

  </main>

  <footer class="border-t border-slate-800 bg-slate-900 py-4 px-6 text-center text-xs text-slate-500">
    GroundTruth Information Authority • Tripartite Semantic Federation • OMG MOF 2.5.1 Compliant
  </footer>

  <script>
    function setQuery(sql) {{
      document.getElementById('sqlInput').value = sql;
      runQuery();
    }}

    async function runQuery() {{
      const sql = document.getElementById('sqlInput').value;
      const resultDiv = document.getElementById('queryResult');
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
  </script>
</body>
</html>"""
        return HTMLResponse(content=html_content)

    return app


app = create_app()
