"""FastAPI Service and Solution-Scoped Model Explorer for GroundTruth.

Strictly adheres to ADR 0002:
1. Data Domain First (Conceptual ontologies, logical schemas, code tables, and junction relations)
2. Equalized Capability API (Transactional, intent-driven operations)
3. Zero-Logic Access Layer (Ultra-thin presentation, crisp Light Theme, no dark mode)
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from groundtruth.api import GroundTruthCatalog
from groundtruth.core.uris import DataURI
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity
from groundtruth.logical.state_machine import FiniteStateMachine, StateTransition
from groundtruth.physical.postgres import PostgresProjectionEngine



import re


def generate_solution_erd(entities: List[LogicalEntity]) -> str:
    """Generate Mermaid ER diagram markup for a specific collection of entities."""
    if not entities:
        return "erDiagram\n    EMPTY_DOMAIN {\n        string notice\n    }"

    lines = ["erDiagram"]
    entity_names = {e.name.lower(): e.name for e in entities}

    # Add relations
    for entity in entities:
        source_name = re.sub(r'[^a-zA-Z0-9_]', '', entity.name).upper()
        for rel in entity.relations:
            target_raw = rel.target_entity_uri.split("/")[-1].lower()
            if target_raw in entity_names:
                target_name = re.sub(r'[^a-zA-Z0-9_]', '', entity_names[target_raw]).upper()
                verb = re.sub(r'[^a-zA-Z0-9_]', '_', rel.name)
                lines.append(f"    {target_name} ||--o{{ {source_name} : {verb}")

    # Add entity definitions
    for entity in entities:
        sanitized_entity = re.sub(r'[^a-zA-Z0-9_]', '', entity.name).upper()
        lines.append(f"    {sanitized_entity} {{")
        for attr in entity.attributes:
            raw_type = attr.data_type.primitive.value.lower()
            type_str = re.sub(r'[^a-zA-Z0-9_]', '', raw_type) or "string"
            attr_name = re.sub(r'[^a-zA-Z0-9_]', '', attr.name)
            pk_str = " PK" if attr.is_primary_key else ""
            fk_str = " FK" if any(r.source_attribute == attr.name for r in entity.relations) else ""
            key_marker = pk_str or fk_str
            lines.append(f"        {type_str} {attr_name}{key_marker}")
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

    capability_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/northstar/Capability",
        attribute_name="lifecycle",
        states=["DRAFT", "PROPOSED", "ACTIVE", "DEPRECATED", "RETIRED"],
        initial_state="DRAFT",
        transitions=[
            StateTransition("DRAFT", "PROPOSED", trigger_action="Submit for Review"),
            StateTransition("PROPOSED", "ACTIVE", trigger_action="Approve Contract"),
            StateTransition("PROPOSED", "DRAFT", trigger_action="Request Changes"),
            StateTransition("ACTIVE", "DEPRECATED", trigger_action="Mark Deprecated"),
            StateTransition("DEPRECATED", "RETIRED", trigger_action="Retire Capability"),
        ],
    )
    catalog.register_state_machine(capability_fsm)

    decision_fsm = FiniteStateMachine(
        target_entity_uri="data://logical/northstar/Decision",
        attribute_name="status",
        states=["PROPOSED", "ACCEPTED", "REJECTED", "SUPERSEDED"],
        initial_state="PROPOSED",
        transitions=[
            StateTransition("PROPOSED", "ACCEPTED", trigger_action="Architect Sign-off"),
            StateTransition("PROPOSED", "REJECTED", trigger_action="Decline Decision"),
            StateTransition("ACCEPTED", "SUPERSEDED", trigger_action="New ADR Supersedes"),
        ],
    )
    catalog.register_state_machine(decision_fsm)

    app = FastAPI(
        title="GroundTruth Data & Information Authority",
        description="ADR 0002 Three-Tier Decomposition: Data Domain First, Equalized Capability API, Zero-Logic UI",
        version="0.2.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.catalog = catalog

    # =========================================================================
    # LAYER 2: EQUALIZED CAPABILITY API (For Automations, AI Agents & Human UI)
    # =========================================================================

    @app.get("/health")
    def health_capability():
        return {
            "status": "ok",
            "service": "groundtruth",
            "terms_count": len(catalog.conceptual.list_terms()),
            "entities_count": len(catalog.logical.list_entities()),
        }

    @app.get("/api/v1/capabilities/tenants")
    def list_tenants_and_solutions_capability():
        """Capability: Discover all available tenants, solutions, and domain packages."""
        entities = catalog.logical.list_entities()
        terms = catalog.conceptual.list_terms()
        domains = sorted(list({e.domain for e in entities} | {t.domain for t in terms}))

        solutions = []
        for d in domains:
            d_entities = [e for e in entities if e.domain == d]
            d_terms = [t for t in terms if t.domain == d]
            solutions.append({
                "solution_slug": d,
                "display_name": {
                    "ecommerce": "🛒 E-Commerce & Payments Domain",
                    "codemesh": "🕸️ CodeMesh Program Graph Engine",
                    "northstar": "🧭 Northstar Intent Authority",
                    "groundtruth": "🏛️ GroundTruth Metamodel",
                    "groundtruth_meta": "🏛️ GroundTruth Metamodel",
                }.get(d, f"📦 {d.capitalize()} Solution"),
                "entity_count": len(d_entities),
                "term_count": len(d_terms),
            })

        return {
            "tenants": [
                {
                    "tenant_id": "00000000-0000-0000-0000-000000000001",
                    "slug": "tripartite",
                    "name": "Tripartite Enterprise",
                    "solutions": solutions,
                }
            ]
        }

    @app.get("/api/v1/tenants")
    def list_tenants_endpoint():
        """Capability: Discover all available tenant partitions."""
        return list_tenants_and_solutions_capability()

    @app.get("/api/v1/tenants/{tenant_slug}/solutions")
    def list_tenant_solutions_capability(tenant_slug: str):
        """Capability: Discover all solutions partitioned under a specific tenant."""
        data = list_tenants_and_solutions_capability()
        for t in data["tenants"]:
            if t["slug"] == tenant_slug:
                return {"tenant": tenant_slug, "solutions": t["solutions"]}
        return {"tenant": tenant_slug, "solutions": []}

    @app.get("/api/v1/tenants/{tenant_slug}/solutions/{solution_slug}")
    def get_tenant_solution_bundle_capability(tenant_slug: str, solution_slug: str):
        """Capability: Retrieve complete conceptual, logical, and physical models scoped by tenant."""
        bundle = get_solution_bundle_capability(solution_slug)
        bundle["tenant_slug"] = tenant_slug
        return bundle

    @app.get("/api/v1/capabilities/solutions/{solution_slug}")
    def get_solution_bundle_capability(solution_slug: str):
        """Capability: Retrieve complete conceptual, logical, and physical models for a solution (legacy)."""
        all_entities = catalog.logical.list_entities()
        all_terms = catalog.conceptual.list_terms()

        # Resolve domain aliases
        match_domains = [solution_slug]
        if solution_slug in ("groundtruth", "groundtruth_meta"):
            match_domains = ["groundtruth", "groundtruth_meta"]

        d_entities = [e for e in all_entities if e.domain in match_domains]
        d_terms = [t for t in all_terms if t.domain in match_domains]

        d_fsms = []
        for key, fsm in catalog.logical._state_machines.items():
            if any(fsm.target_entity_uri.startswith(f"data://logical/{d}/") for d in match_domains):
                d_fsms.append(fsm.to_dict())

        ddl = PostgresProjectionEngine.generate_schema_ddl(d_entities, schema=solution_slug) if d_entities else ""
        erd_mermaid = generate_solution_erd(d_entities)

        return {
            "tenant_slug": "tripartite",
            "solution_slug": solution_slug,
            "display_name": {
                "ecommerce": "🛒 E-Commerce & Payments Domain",
                "codemesh": "🕸️ CodeMesh Program Graph Engine",
                "northstar": "🧭 Northstar Intent Authority",
                "groundtruth": "🏛️ GroundTruth Metamodel",
                "groundtruth_meta": "🏛️ GroundTruth Metamodel",
                "portal": "🖥️ Tripartite Portal & Presentation Authority",
            }.get(solution_slug, f"📦 {solution_slug.capitalize()} Solution"),
            "terms": [t.to_dict() for t in d_terms],
            "entities": [e.to_dict() for e in d_entities],
            "state_machines": d_fsms,
            "ddl": ddl,
            "erd_mermaid": erd_mermaid,
        }




    @app.get("/api/v1/terms")
    def list_terms(domain: Optional[str] = None):
        """Capability: List registered conceptual business terms."""
        terms = catalog.conceptual.list_terms()
        if domain:
            terms = [t for t in terms if t.domain == domain]
        return [t.to_dict() for t in terms]

    @app.get("/api/v1/terms/{term_slug:path}")
    def get_term(term_slug: str):
        """Capability: Retrieve conceptual business term by slug or URI."""
        clean = term_slug.strip("/").lower()
        for t in catalog.conceptual.list_terms():
            if t.slug.lower() == clean or t.uri.lower() == clean or t.uri.lower().endswith(f"/{clean}"):
                return t.to_dict()
        raise HTTPException(status_code=404, detail=f"Business term '{term_slug}' not found")

    @app.post("/api/v1/terms")
    def register_term(payload: Dict[str, Any]):
        """Capability: Register a new ISO/IEC 11179 conceptual business term."""
        try:
            term = BusinessTerm.from_dict(payload)
            registered = catalog.register_business_term(term)
            return registered.to_dict()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/entities")
    def list_entities(domain: Optional[str] = None):
        """Capability: List normalized logical entity schemas."""
        return [e.to_dict() for e in catalog.logical.list_entities(domain=domain)]

    @app.get("/api/v1/entities/{entity_name:path}")
    def get_entity(entity_name: str, domain: Optional[str] = None):
        """Capability: Retrieve full logical entity schema."""
        clean = entity_name.strip("/").lower()
        for e in catalog.logical.list_entities(domain=domain):
            if e.name.lower() == clean or e.uri.lower() == clean or e.uri.lower().endswith(f"/{clean}"):
                return e.to_dict()
        raise HTTPException(status_code=404, detail=f"Logical entity '{entity_name}' not found")


    @app.post("/api/v1/entities")
    def define_entity(payload: Dict[str, Any]):
        """Capability: Define and validate a new logical relational entity schema."""
        try:
            entity = LogicalEntity.from_dict(payload)
            defined = catalog.define_logical_entity(entity)
            return defined.to_dict()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/state-machines")
    def list_state_machines():
        """Capability: List all governing finite state machines."""
        return [f.to_dict() for f in catalog.logical.list_state_machines()]

    @app.post("/api/v1/state-machines/validate-transition")
    def validate_state_transition(payload: Dict[str, str]):
        """Capability: Validate whether a state transition is legal under declared FSM rules."""
        target_entity_uri = payload.get("target_entity_uri")
        attribute_name = payload.get("attribute_name", "status")
        from_state = payload.get("from_state")
        to_state = payload.get("to_state")

        if not target_entity_uri or not from_state or not to_state:
            raise HTTPException(status_code=400, detail="target_entity_uri, from_state, and to_state are required")

        fsm = catalog.logical.get_state_machine(target_entity_uri, attribute_name=attribute_name)
        if not fsm:
            raise HTTPException(status_code=404, detail=f"No FSM declared for {target_entity_uri}.{attribute_name}")

        try:
            fsm.verify_transition(from_state, to_state)
            return {
                "target_entity_uri": target_entity_uri,
                "attribute_name": attribute_name,
                "from_state": from_state,
                "to_state": to_state,
                "is_valid": True,
                "initial_state": fsm.initial_state,
            }
        except Exception as e:
            return {
                "target_entity_uri": target_entity_uri,
                "attribute_name": attribute_name,
                "from_state": from_state,
                "to_state": to_state,
                "is_valid": False,
                "error": str(e),
                "legal_next_states": fsm.get_legal_next_states(from_state) if from_state in fsm.states else [],
                "initial_state": fsm.initial_state,
            }


    @app.get("/api/v1/projections/schema/{domain}")
    @app.get("/api/v1/projections/postgres/{domain}")
    def get_schema_projection_ddl(domain: str, schema: Optional[str] = None):
        """Capability: Generate physical schema projection (DDL) for a target domain."""
        target_schema = schema or domain
        try:
            ddl = catalog.generate_postgres_ddl(domain, schema=target_schema)
            return {"domain": domain, "schema": target_schema, "ddl": ddl}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.post("/api/v1/uris/resolve")
    def resolve_canonical_data_uri(payload: Dict[str, Any]):
        """Capability: Parse, validate, and resolve any GroundTruth URI into 5-tuple coordinates."""
        raw_uri = payload.get("uri")
        default_tenant = payload.get("default_tenant", "tripartite")
        if not raw_uri:
            raise HTTPException(status_code=400, detail="uri is required in payload")
        try:
            parsed = DataURI.parse(raw_uri)
            coords = parsed.to_coordinate_tuple(default_tenant=default_tenant)
            return {
                "raw_uri": raw_uri,
                "is_valid": True,
                "canonical_uri": parsed.to_canonical(default_tenant=default_tenant),
                "coordinates": {
                    "scheme": coords[0],
                    "tenant": coords[1],
                    "solution": coords[2],
                    "version": coords[3],
                    "local_path": coords[4],
                },
                "tier": parsed.tier.value,
                "attribute": parsed.attribute,
            }
        except Exception as e:
            return {
                "raw_uri": raw_uri,
                "is_valid": False,
                "error": str(e),
            }


    # =========================================================================
    # PURE JSON CAPABILITY API SERVICE INDEX (Zero Presentation HTML)
    # =========================================================================

    @app.get("/")
    def root_index():
        """Pure data capability service index and discovery metadata."""
        return {
            "service": "GroundTruth Data & Information Authority",
            "version": "0.2.0",
            "authority": "Data Authority (Conceptual, Logical, Physical)",
            "docs": "/docs",
            "openapi": "/openapi.json",
            "tenants": "/api/v1/capabilities/tenants",
            "terms": "/api/v1/terms",
            "entities": "/api/v1/entities",
            "state_machines": "/api/v1/state-machines",
            "health": "/health",
        }

    return app


app = create_app()


