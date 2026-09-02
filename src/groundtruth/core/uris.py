"""Canonical data:// URI parser and addressing grammar for GroundTruth."""

from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional


class DataTier(str, Enum):
    """The four architectural tiers of GroundTruth data addressing."""
    CONCEPTUAL = "conceptual"
    LOGICAL = "logical"
    PHYSICAL = "physical"
    LINEAGE = "lineage"
    GOVERNANCE = "governance"


@dataclass(frozen=True)
class DataURI:
    """Canonical data:// URI representation in GroundTruth.
    
    Format:
      data://conceptual/<term-slug>
      data://conceptual/properties/<property-slug>
      data://logical/<domain>/<EntityName>
      data://logical/<domain>/<EntityName>.<attribute>
      data://physical/<target>/<schema>/<table_name>
      data://lineage/<pipeline>/<transform_id>
      data://governance/<policy_slug>
    """
    tier: DataTier
    path: str
    attribute: Optional[str] = None
    raw_uri: str = ""

    def __str__(self) -> str:
        return self.raw_uri

    @classmethod
    def parse(cls, uri: str) -> "DataURI":
        """Parse a canonical data:// URI string."""
        if not uri.startswith("data://"):
            raise ValueError(f"Invalid GroundTruth URI scheme (must start with 'data://'): {uri}")

        stripped = uri[len("data://"):]
        parts = stripped.split("/", 1)
        if len(parts) < 2:
            raise ValueError(f"Invalid GroundTruth URI structure (missing tier or path): {uri}")

        tier_str, rest = parts[0], parts[1]
        try:
            tier = DataTier(tier_str)
        except ValueError:
            raise ValueError(f"Unknown data tier '{tier_str}' in URI '{uri}'. Allowed: {[t.value for t in DataTier]}")

        # Check for attribute specification in logical or conceptual tier (e.g. Order.status)
        attr = None
        if tier == DataTier.LOGICAL and "." in rest:
            entity_path, attr = rest.rsplit(".", 1)
            return cls(tier=tier, path=entity_path, attribute=attr, raw_uri=uri)

        return cls(tier=tier, path=rest, attribute=None, raw_uri=uri)

    @classmethod
    def conceptual(cls, term_slug: str) -> "DataURI":
        raw = f"data://conceptual/{term_slug}"
        return cls(tier=DataTier.CONCEPTUAL, path=term_slug, attribute=None, raw_uri=raw)

    @classmethod
    def logical(cls, domain: str, entity_name: str, attribute: Optional[str] = None) -> "DataURI":
        path = f"{domain}/{entity_name}"
        raw = f"data://logical/{path}" + (f".{attribute}" if attribute else "")
        return cls(tier=DataTier.LOGICAL, path=path, attribute=attribute, raw_uri=raw)

    @classmethod
    def physical(cls, target: str, schema: str, table_name: str) -> "DataURI":
        path = f"{target}/{schema}/{table_name}"
        raw = f"data://physical/{path}"
        return cls(tier=DataTier.PHYSICAL, path=path, attribute=None, raw_uri=raw)


def parse_data_uri(uri: str) -> DataURI:
    """Convenience helper to parse a data:// URI."""
    return DataURI.parse(uri)
