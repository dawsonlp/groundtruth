"""Abstract storage repository ports for GroundTruth data models."""

from abc import ABC, abstractmethod
from typing import List, Optional

from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.entities import LogicalEntity


class DataRepository(ABC):
    """Abstract port for persisting and querying GroundTruth data models."""

    @abstractmethod
    def save_term(self, term: BusinessTerm) -> None:
        """Save a conceptual business term."""
        pass

    @abstractmethod
    def get_term(self, slug: str) -> Optional[BusinessTerm]:
        """Retrieve a conceptual term."""
        pass

    @abstractmethod
    def save_entity(self, entity: LogicalEntity) -> None:
        """Save a logical entity."""
        pass

    @abstractmethod
    def get_entity(self, uri: str) -> Optional[LogicalEntity]:
        """Retrieve a logical entity."""
        pass

    @abstractmethod
    def list_entities(self, domain: Optional[str] = None) -> List[LogicalEntity]:
        """List logical entities."""
        pass

