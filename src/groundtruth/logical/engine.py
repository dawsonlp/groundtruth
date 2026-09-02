"""Logical Schema Compilation, State Verification & Integrity Engine for GroundTruth."""

from typing import Any, Dict, List, Optional

from groundtruth.conceptual.catalog import ConceptualCatalog
from groundtruth.logical.entities import LogicalEntity
from groundtruth.logical.state_machine import FiniteStateMachine, IllegalStateTransitionError


class MissingPrimaryKeyError(Exception):
    """Raised when defining a logical entity without declaring a primary key (LOGICAL_001)."""
    def __init__(self, message: str, entity_name: str):
        super().__init__(message)
        self.entity_name = entity_name
        self.domain_error_code = "LOGICAL_001"


class UnmappedConceptualTermError(Exception):
    """Raised when a logical entity references a non-existent conceptual term (LOGICAL_002)."""
    def __init__(self, message: str, term_ref: str):
        super().__init__(message)
        self.term_ref = term_ref
        self.domain_error_code = "LOGICAL_002"


class LogicalSchemaEngine:
    """Core engine for defining DAMA logical schemas and verifying relational integrity."""

    def __init__(self, conceptual_catalog: Optional[ConceptualCatalog] = None):
        self.conceptual_catalog = conceptual_catalog
        self._entities: Dict[str, LogicalEntity] = {}
        self._state_machines: Dict[str, FiniteStateMachine] = {}

    def define_entity(self, entity: LogicalEntity) -> LogicalEntity:
        """Define and validate a logical entity satisfying req://logical/define-entity-schema."""
        # Precondition 1: Conceptual term reference must exist if conceptual catalog is attached
        if self.conceptual_catalog and entity.conceptual_term_ref:
            term = self.conceptual_catalog.get_term(entity.conceptual_term_ref)
            if not term:
                raise UnmappedConceptualTermError(
                    f"Referenced conceptual term '{entity.conceptual_term_ref}' does not exist in conceptual catalog",
                    term_ref=entity.conceptual_term_ref,
                )

        # Precondition 2: Must declare at least one primary key (Failure Mode LOGICAL_001)
        if not entity.primary_keys:
            raise MissingPrimaryKeyError(
                f"Logical entity '{entity.name}' must declare at least one primary key attribute",
                entity_name=entity.name,
            )

        self._entities[entity.uri] = entity
        return entity

    def register_state_machine(self, fsm: FiniteStateMachine) -> FiniteStateMachine:
        """Attach a finite state machine to an entity attribute."""
        key = f"{fsm.target_entity_uri}.{fsm.attribute_name}"
        self._state_machines[key] = fsm
        return fsm

    def verify_state_transition(self, entity_uri: str, attribute_name: str, from_state: str, to_state: str) -> bool:
        """Verify state change validity satisfying req://logical/verify-state-transition."""
        key = f"{entity_uri}.{attribute_name}"
        fsm = self._state_machines.get(key)
        if not fsm:
            raise ValueError(f"No finite state machine declared on '{key}'")

        return fsm.verify_transition(from_state, to_state)

    def get_entity(self, uri: str) -> Optional[LogicalEntity]:
        return self._entities.get(uri)

    def get_state_machine(self, entity_uri: str, attribute_name: str) -> Optional[FiniteStateMachine]:
        key = f"{entity_uri}.{attribute_name}"
        return self._state_machines.get(key)

    def list_entities(self, domain: Optional[str] = None) -> List[LogicalEntity]:
        if domain:
            return [e for e in self._entities.values() if e.domain == domain]
        return list(self._entities.values())

