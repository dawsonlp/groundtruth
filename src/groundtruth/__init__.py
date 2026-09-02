"""GroundTruth: The Information & Data Authority for the Tripartite Federation."""

from groundtruth.adapters import DataRepository, GitFileDataAdapter, SQLiteDataAdapter
from groundtruth.api import GroundTruthCatalog
from groundtruth.conceptual import (
    BusinessTerm,
    ConceptualCatalog,
    DataElementConcept,
    DuplicateTermError,
    InvalidPropertyConceptError,
    PropertyConcept,
    RECOGNIZED_PROPERTY_CONCEPTS,
)
from groundtruth.core import (
    AuthorityTier,
    DataProvenance,
    DataTier,
    DataType,
    DataURI,
    LifecycleState,
    MetaLevel,
    PrimitiveType,
    parse_data_uri,
)
from groundtruth.governance import (
    ComplianceCertificate,
    PrivacyClassification,
    PrivacyClassifier,
    UnclassifiedSensitiveDataError,
)
from groundtruth.lineage import (
    LineageGraph,
    ProvenanceEdge,
    UnknownAttributeError,
)
from groundtruth.logical import (
    FiniteStateMachine,
    IllegalStateTransitionError,
    LogicalAttribute,
    LogicalEntity,
    LogicalSchemaEngine,
    MissingPrimaryKeyError,
    Relation,
    RelationshipType,
    StateTransition,
    UnmappedConceptualTermError,
)
from groundtruth.physical import (
    PostgresProjectionEngine,
    UnsupportedTypeMappingError,
)

__version__ = "0.1.0"

__all__ = [
    "GroundTruthCatalog",
    # Core
    "DataURI",
    "DataTier",
    "parse_data_uri",
    "DataType",
    "PrimitiveType",
    "MetaLevel",
    "AuthorityTier",
    "LifecycleState",
    "DataProvenance",
    # Conceptual
    "BusinessTerm",
    "PropertyConcept",
    "DataElementConcept",
    "ConceptualCatalog",
    "DuplicateTermError",
    "InvalidPropertyConceptError",
    "RECOGNIZED_PROPERTY_CONCEPTS",
    # Logical
    "LogicalEntity",
    "LogicalAttribute",
    "Relation",
    "RelationshipType",
    "FiniteStateMachine",
    "StateTransition",
    "LogicalSchemaEngine",
    "IllegalStateTransitionError",
    "MissingPrimaryKeyError",
    "UnmappedConceptualTermError",
    # Physical
    "PostgresProjectionEngine",
    "UnsupportedTypeMappingError",
    # Lineage
    "LineageGraph",
    "ProvenanceEdge",
    "UnknownAttributeError",
    # Governance
    "PrivacyClassifier",
    "ComplianceCertificate",
    "PrivacyClassification",
    "UnclassifiedSensitiveDataError",
    # Adapters
    "DataRepository",
    "GitFileDataAdapter",
    "SQLiteDataAdapter",
]

