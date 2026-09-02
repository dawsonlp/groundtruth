"""Finite State Machine Verification and Transition Engine for Logical Entities."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set, Tuple


class IllegalStateTransitionError(Exception):
    """Raised when an attempted state change is not in the declared legal transition matrix (LOGICAL_003)."""
    def __init__(self, message: str, from_state: str, to_state: str, legal_next_states: List[str]):
        super().__init__(message)
        self.from_state = from_state
        self.to_state = to_state
        self.legal_next_states = legal_next_states
        self.domain_error_code = "LOGICAL_003"


@dataclass
class StateTransition:
    """A valid directed edge in a lifecycle state machine."""
    from_state: str
    to_state: str
    description: str = ""
    trigger_action: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "description": self.description,
            "trigger_action": self.trigger_action,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StateTransition":
        return cls(
            from_state=data["from_state"],
            to_state=data["to_state"],
            description=data.get("description", ""),
            trigger_action=data.get("trigger_action", ""),
        )


@dataclass
class FiniteStateMachine:
    """Encapsulates legal lifecycle states and transition matrices for a logical entity attribute."""
    target_entity_uri: str
    attribute_name: str
    states: List[str]
    transitions: List[StateTransition]
    initial_state: str

    def __post_init__(self):
        # Validate that states and transitions are consistent
        transition_states = {t.from_state for t in self.transitions} | {t.to_state for t in self.transitions}
        for s in transition_states:
            if s not in self.states:
                self.states.append(s)

    @property
    def legal_transitions(self) -> Set[Tuple[str, str]]:
        return {(t.from_state, t.to_state) for t in self.transitions}

    def verify_transition(self, from_state: str, to_state: str) -> bool:
        """Verify state change validity satisfying req://logical/verify-state-transition."""
        # Precondition 1: Current state must be in declared states
        if from_state not in self.states:
            raise ValueError(f"State '{from_state}' is not a recognized state in state machine: {self.states}")

        if to_state not in self.states:
            raise ValueError(f"Target state '{to_state}' is not a recognized state in state machine: {self.states}")

        # Check legal transition
        if (from_state, to_state) not in self.legal_transitions:
            legal_next = [t.to_state for t in self.transitions if t.from_state == from_state]
            raise IllegalStateTransitionError(
                f"Illegal state transition from '{from_state}' to '{to_state}'. Legal next states: {legal_next}",
                from_state=from_state,
                to_state=to_state,
                legal_next_states=legal_next,
            )

        return True

    def get_legal_next_states(self, current_state: str) -> List[str]:
        return [t.to_state for t in self.transitions if t.from_state == current_state]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_entity_uri": self.target_entity_uri,
            "attribute_name": self.attribute_name,
            "states": self.states,
            "initial_state": self.initial_state,
            "transitions": [t.to_dict() for t in self.transitions],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FiniteStateMachine":
        return cls(
            target_entity_uri=data["target_entity_uri"],
            attribute_name=data["attribute_name"],
            states=data.get("states", []),
            initial_state=data.get("initial_state", ""),
            transitions=[StateTransition.from_dict(t) for t in data.get("transitions", [])],
        )
