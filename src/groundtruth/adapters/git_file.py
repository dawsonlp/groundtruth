"""Git-native YAML and Markdown adapter for GroundTruth models."""

from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

from groundtruth.adapters.base import DataRepository
from groundtruth.conceptual.catalog import ConceptualCatalog
from groundtruth.conceptual.models import BusinessTerm, PropertyConcept
from groundtruth.logical.engine import LogicalSchemaEngine
from groundtruth.logical.entities import LogicalEntity


class GitFileDataAdapter(DataRepository):
    """File-based persistence adapter for GroundTruth domain models."""

    def __init__(self, root_dir: str | Path):
        self.root_dir = Path(root_dir)
        self.models_dir = self.root_dir / "models"
        self.conceptual_dir = self.models_dir / "conceptual"
        self.logical_dir = self.models_dir / "logical"

    def save_term(self, term: BusinessTerm) -> None:
        self.conceptual_dir.mkdir(parents=True, exist_ok=True)
        path = self.conceptual_dir / f"{term.slug}.yaml"
        with open(path, "w") as f:
            yaml.safe_dump(term.to_dict(), f, sort_keys=False)

    def get_term(self, slug: str) -> Optional[BusinessTerm]:
        path = self.conceptual_dir / f"{slug}.yaml"
        if not path.exists():
            return None
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return BusinessTerm.from_dict(data) if data else None

    def save_entity(self, entity: LogicalEntity) -> None:
        domain_dir = self.logical_dir / entity.domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        path = domain_dir / f"{entity.name}.yaml"
        with open(path, "w") as f:
            yaml.safe_dump(entity.to_dict(), f, sort_keys=False)

    def get_entity(self, uri: str) -> Optional[LogicalEntity]:
        # Parse uri: data://logical/<domain>/<name>
        parts = uri.replace("data://logical/", "").split("/")
        if len(parts) < 2:
            return None
        domain, name = parts[0], parts[1]
        path = self.logical_dir / domain / f"{name}.yaml"
        if not path.exists():
            return None
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            return LogicalEntity.from_dict(data) if data else None

    def list_entities(self, domain: Optional[str] = None) -> List[LogicalEntity]:
        entities = []
        if not self.logical_dir.exists():
            return []
        for path in self.logical_dir.rglob("*.yaml"):
            with open(path, "r") as f:
                data = yaml.safe_load(f)
                if data:
                    entity = LogicalEntity.from_dict(data)
                    if not domain or entity.domain == domain:
                        entities.append(entity)
        return entities

    def load_into(self, conceptual_catalog: ConceptualCatalog, logical_engine: LogicalSchemaEngine) -> None:
        """Scan models directory and populate catalogs."""
        if self.conceptual_dir.exists():
            for path in self.conceptual_dir.glob("*.yaml"):
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                    if not data:
                        continue
                    if isinstance(data, dict) and "terms" in data:
                        for item in data["terms"]:
                            term = BusinessTerm.from_dict(item)
                            conceptual_catalog._terms[term.slug] = term
                    elif isinstance(data, list):
                        for item in data:
                            term = BusinessTerm.from_dict(item)
                            conceptual_catalog._terms[term.slug] = term
                    elif isinstance(data, dict) and "slug" in data:
                        term = BusinessTerm.from_dict(data)
                        conceptual_catalog._terms[term.slug] = term

        if self.logical_dir.exists():
            for path in self.logical_dir.rglob("*.yaml"):
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                    if not data:
                        continue
                    if isinstance(data, dict) and "entities" in data:
                        for item in data["entities"]:
                            entity = LogicalEntity.from_dict(item)
                            logical_engine._entities[entity.uri] = entity
                    elif isinstance(data, list):
                        for item in data:
                            entity = LogicalEntity.from_dict(item)
                            logical_engine._entities[entity.uri] = entity
                    elif isinstance(data, dict) and "name" in data:
                        entity = LogicalEntity.from_dict(data)
                        logical_engine._entities[entity.uri] = entity


