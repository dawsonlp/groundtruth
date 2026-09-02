"""Data Privacy Classification and Compliance Enforcement for GroundTruth."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from groundtruth.logical.entities import LogicalAttribute, LogicalEntity


class UnclassifiedSensitiveDataError(Exception):
    """Raised when a sensitive attribute lacks explicit privacy classification (GOVERNANCE_001)."""
    def __init__(self, message: str, entity_uri: str, attribute_name: str):
        super().__init__(message)
        self.entity_uri = entity_uri
        self.attribute_name = attribute_name
        self.domain_error_code = "GOVERNANCE_001"


class PrivacyClassification(str, Enum):
    """Standard enterprise data classifications."""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED_PII = "PII"
    FINANCIAL = "FINANCIAL"


@dataclass
class ComplianceCertificate:
    """Audit certificate proving data privacy and masking conformance."""
    entity_uri: str
    is_valid: bool
    classified_attributes: List[str]
    pii_attributes: List[str]
    masking_rules: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entity_uri": self.entity_uri,
            "is_valid": self.is_valid,
            "classified_attributes": self.classified_attributes,
            "pii_attributes": self.pii_attributes,
            "masking_rules": self.masking_rules,
        }


class PrivacyClassifier:
    """Enforces privacy tags and generates compliance audit certificates."""

    @classmethod
    def enforce_privacy_tagging(cls, entity: LogicalEntity) -> ComplianceCertificate:
        """Enforce privacy classification metadata satisfying req://governance/enforce-privacy-tagging."""
        classified_attrs = []
        pii_attrs = []
        masking_rules = {}

        for attr in entity.attributes:
            has_tag = bool(attr.tags) or any(c.value in attr.tags for c in PrivacyClassification)

            # Precondition: If marked sensitive, MUST have explicit classification tag
            if attr.is_sensitive and not has_tag:
                raise UnclassifiedSensitiveDataError(
                    f"Attribute '{attr.name}' in entity '{entity.uri}' is marked sensitive but lacks a privacy classification tag (e.g. 'PII', 'CONFIDENTIAL')",
                    entity_uri=entity.uri,
                    attribute_name=attr.name,
                )

            if has_tag:
                classified_attrs.append(attr.name)

            if "PII" in attr.tags or attr.name.lower() in ("email", "ssn", "phone", "first_name", "last_name"):
                pii_attrs.append(attr.name)
                masking_rules[attr.name] = f"sha256_hash({attr.name})"

        return ComplianceCertificate(
            entity_uri=entity.uri,
            is_valid=True,
            classified_attributes=classified_attrs,
            pii_attributes=pii_attrs,
            masking_rules=masking_rules,
        )

