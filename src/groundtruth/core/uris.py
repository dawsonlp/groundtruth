"""Canonical data:// Option B URI parser and addressing grammar for GroundTruth.

Grammar:
  data://[tenant:][solution]/[tier]/[entity_or_term][@version][.attribute]
  or legacy shorthand:
  data://[tier]/[domain]/[entity][.attribute]
  data://conceptual/[term-slug]
"""

from dataclasses import dataclass
from enum import Enum
import re
from typing import Optional, Tuple


class DataTier(str, Enum):
    """The four architectural tiers of GroundTruth data addressing."""
    CONCEPTUAL = "conceptual"
    LOGICAL = "logical"
    PHYSICAL = "physical"
    LINEAGE = "lineage"
    GOVERNANCE = "governance"


OPTION_B_DATA_PATTERN = re.compile(
    r"^data://"
    r"(?:(?P<tenant>[a-z0-9_-]+):)?"
    r"(?:(?P<solution>[a-z0-9_-]+)/)?"
    r"(?P<tier>conceptual|logical|physical|lineage|governance)/"
    r"(?P<path>[a-zA-Z0-9_/-]+?)"
    r"(?:\.(?P<attribute>[a-zA-Z0-9_-]+))?"
    r"(?:@(?P<version>[a-zA-Z0-9_.-]+))?"
    r"(?:\.(?P<attribute2>[a-zA-Z0-9_-]+))?$"
)


@dataclass(frozen=True)
class DataURI:
    tier: DataTier
    path: str
    attribute: Optional[str] = None
    tenant: Optional[str] = None
    solution: Optional[str] = None
    version: Optional[str] = None
    raw_uri: str = ""

    def __str__(self) -> str:
        return self.raw_uri or self.to_canonical()

    def to_canonical(self, default_tenant: str = "tripartite", default_version: Optional[str] = None) -> str:
        tenant_part = f"{self.tenant or default_tenant}:"
        sol_part = f"{self.solution}/" if self.solution else ""
        attr_part = f".{self.attribute}" if self.attribute else ""
        ver_part = f"@{self.version}" if self.version else (f"@{default_version}" if default_version else "")
        return f"data://{tenant_part}{sol_part}{self.tier.value}/{self.path}{attr_part}{ver_part}"

    def to_coordinate_tuple(self, default_tenant: str = "tripartite") -> Tuple[str, str, str, str, str]:
        """Return 5-tuple: (scheme, tenant, solution, version, path)."""
        tenant_val = self.tenant or default_tenant
        sol_val = self.solution or (self.path.split("/")[0] if "/" in self.path else "general")
        version_val = self.version or "latest"
        path_val = f"{self.path}.{self.attribute}" if self.attribute else self.path
        return ("data", tenant_val, sol_val, version_val, path_val)

    @classmethod
    def parse(cls, uri: str) -> "DataURI":
        """Parse a canonical Option B or legacy data:// URI string."""
        if not uri.startswith("data://"):
            raise ValueError(f"Invalid GroundTruth URI scheme (must start with 'data://'): {uri}")

        match = OPTION_B_DATA_PATTERN.match(uri.strip())
        if match:
            tenant = match.group("tenant")
            solution = match.group("solution")
            tier_str = match.group("tier")
            path = match.group("path")
            version = match.group("version")
            attr = match.group("attribute") or match.group("attribute2")
            tier = DataTier(tier_str)
            return cls(
                tier=tier,
                path=path,
                attribute=attr,
                tenant=tenant,
                solution=solution,
                version=version,
                raw_uri=uri,
            )


        # Legacy fallback parser
        stripped = uri[len("data://"):]
        parts = stripped.split("/", 1)
        if len(parts) < 2:
            raise ValueError(f"Invalid GroundTruth URI structure (missing tier or path): {uri}")

        tier_str, rest = parts[0], parts[1]
        try:
            tier = DataTier(tier_str)
        except ValueError:
            raise ValueError(f"Unknown data tier '{tier_str}' in URI '{uri}'. Allowed: {[t.value for t in DataTier]}")

        attr = None
        if tier == DataTier.LOGICAL and "." in rest:
            entity_path, attr = rest.rsplit(".", 1)
            return cls(tier=tier, path=entity_path, attribute=attr, raw_uri=uri)

        return cls(tier=tier, path=rest, attribute=None, raw_uri=uri)

    @classmethod
    def conceptual(cls, term_slug: str, tenant: Optional[str] = None, version: Optional[str] = None) -> "DataURI":
        tenant_part = f"{tenant}:" if tenant else ""
        ver_part = f"@{version}" if version else ""
        raw = f"data://{tenant_part}conceptual/{term_slug}{ver_part}"
        return cls(tier=DataTier.CONCEPTUAL, path=term_slug, attribute=None, tenant=tenant, version=version, raw_uri=raw)

    @classmethod
    def logical(
        cls,
        domain: str,
        entity_name: str,
        attribute: Optional[str] = None,
        tenant: Optional[str] = None,
        version: Optional[str] = None,
    ) -> "DataURI":
        path = f"{domain}/{entity_name}" if not domain or domain in entity_name else f"{domain}/{entity_name}"
        tenant_part = f"{tenant}:" if tenant else ""
        ver_part = f"@{version}" if version else ""
        attr_part = f".{attribute}" if attribute else ""
        raw = f"data://{tenant_part}logical/{path}{ver_part}{attr_part}"
        return cls(
            tier=DataTier.LOGICAL,
            path=path,
            attribute=attribute,
            tenant=tenant,
            solution=domain,
            version=version,
            raw_uri=raw,
        )

    @classmethod
    def physical(cls, target: str, schema: str, table_name: str, tenant: Optional[str] = None) -> "DataURI":
        path = f"{target}/{schema}/{table_name}"
        tenant_part = f"{tenant}:" if tenant else ""
        raw = f"data://{tenant_part}physical/{path}"
        return cls(tier=DataTier.PHYSICAL, path=path, attribute=None, tenant=tenant, raw_uri=raw)


def parse_data_uri(uri: str) -> DataURI:
    """Convenience helper to parse a data:// URI."""
    return DataURI.parse(uri)
