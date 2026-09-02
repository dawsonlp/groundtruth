"""FastAPI REST Service for GroundTruth Information & Data Authority."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from groundtruth.api import GroundTruthCatalog
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.entities import LogicalAttribute, LogicalEntity
from groundtruth.logical.state_machine import FiniteStateMachine, StateTransition


def create_app(workspace_root: Optional[str | Path] = None) -> FastAPI:
    root_path = Path(workspace_root or os.getenv("GROUNDTRUTH_WORKSPACE_ROOT", "."))
    catalog = GroundTruthCatalog.load(root_path) if (root_path / "models").exists() else GroundTruthCatalog()

    app = FastAPI(
        title="GroundTruth Data & Information Authority",
        description="Authoritative DAMA & MOF data modeling catalog for Tripartite Semantic Federation",
        version="0.1.0",
    )
    app.state.catalog = catalog

    class TransitionCheckPayload(BaseModel):
        entity_uri: str
        attribute_name: str
        from_state: str
        to_state: str

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
    def verify_state_transition(payload: TransitionCheckPayload):
        try:
            valid = catalog.verify_state_transition(
                payload.entity_uri, payload.attribute_name, payload.from_state, payload.to_state
            )
            return {"valid": valid, "from_state": payload.from_state, "to_state": payload.to_state}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/v1/projections/postgres/{entity_uri:path}")
    def get_postgres_ddl(entity_uri: str, schema: str = "public"):
        try:
            ddl = catalog.generate_postgres_ddl(entity_uri, schema=schema)
            return {"entity_uri": entity_uri, "ddl": ddl}
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/v1/governance/certificate/{entity_uri:path}")
    def get_compliance_certificate(entity_uri: str):
        try:
            cert = catalog.enforce_privacy_classification(entity_uri)
            return cert.to_dict()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    return app


app = create_app()
