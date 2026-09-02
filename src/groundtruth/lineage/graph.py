"""Column-Level Data Provenance and Transform Lineage Graph for GroundTruth."""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


class UnknownAttributeError(Exception):
    """Raised when querying lineage for an unknown attribute URI (LINEAGE_001)."""
    def __init__(self, message: str, attribute_uri: str):
        super().__init__(message)
        self.attribute_uri = attribute_uri
        self.domain_error_code = "LINEAGE_001"


@dataclass
class ProvenanceEdge:
    """A directed edge in the data lineage DAG."""
    source_uri: str
    target_uri: str
    transform_name: str = "direct_copy"
    expression: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_uri": self.source_uri,
            "target_uri": self.target_uri,
            "transform_name": self.transform_name,
            "expression": self.expression,
        }


class LineageGraph:
    """Directed Acyclic Graph (DAG) for column-level data provenance."""

    def __init__(self):
        self._outgoing: Dict[str, List[ProvenanceEdge]] = defaultdict(list)
        self._incoming: Dict[str, List[ProvenanceEdge]] = defaultdict(list)
        self._registered_vertices: Set[str] = set()

    def register_vertex(self, uri: str) -> None:
        self._registered_vertices.add(uri)

    def add_lineage(self, source_uri: str, target_uri: str, transform_name: str = "direct_copy", expression: str = "") -> ProvenanceEdge:
        """Register a transformation edge from source column to target column."""
        edge = ProvenanceEdge(
            source_uri=source_uri,
            target_uri=target_uri,
            transform_name=transform_name,
            expression=expression,
        )
        self._outgoing[source_uri].append(edge)
        self._incoming[target_uri].append(edge)
        self._registered_vertices.add(source_uri)
        self._registered_vertices.add(target_uri)
        return edge

    def trace_column(self, attribute_uri: str) -> Dict[str, Any]:
        """Traverse upstream and downstream provenance satisfying req://lineage/trace-column-provenance."""
        if attribute_uri not in self._registered_vertices:
            raise UnknownAttributeError(
                f"Attribute URI '{attribute_uri}' not found in lineage graph",
                attribute_uri=attribute_uri,
            )

        upstream = self._trace_direction(attribute_uri, is_upstream=True)
        downstream = self._trace_direction(attribute_uri, is_upstream=False)

        return {
            "target_attribute_uri": attribute_uri,
            "upstream_sources": list(upstream),
            "downstream_targets": list(downstream),
            "total_lineage_hops": len(upstream) + len(downstream),
        }

    def _trace_direction(self, start_uri: str, is_upstream: bool) -> Set[str]:
        visited: Set[str] = set()
        queue = [start_uri]

        while queue:
            curr = queue.pop(0)
            edges = self._incoming.get(curr, []) if is_upstream else self._outgoing.get(curr, [])
            for edge in edges:
                next_node = edge.source_uri if is_upstream else edge.target_uri
                if next_node not in visited and next_node != start_uri:
                    visited.add(next_node)
                    queue.append(next_node)

        return visited

