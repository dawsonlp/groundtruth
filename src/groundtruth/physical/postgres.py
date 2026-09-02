"""Deterministic PostgreSQL Physical DDL Projection Engine for GroundTruth."""

from typing import List, Optional

from groundtruth.logical.entities import LogicalEntity, Relation


class UnsupportedTypeMappingError(Exception):
    """Raised when an abstract logical type cannot be mapped to PostgreSQL dialect (PHYSICAL_001)."""
    def __init__(self, message: str, attribute_name: str, type_name: str):
        super().__init__(message)
        self.attribute_name = attribute_name
        self.type_name = type_name
        self.domain_error_code = "PHYSICAL_001"


class PostgresProjectionEngine:
    """Pure functional generator mapping DAMA logical entities to deterministic PostgreSQL DDL."""

    @classmethod
    def to_create_table_ddl(cls, entity: LogicalEntity, schema: str = "public") -> str:
        """Generate deterministic CREATE TABLE DDL satisfying req://physical/generate-ddl-projection."""
        table_name = entity.name.lower()
        full_table_name = f"{schema}.{table_name}"

        # 1. Sort columns deterministically: PKs first in order, then regular attributes
        pk_attrs = [a for a in entity.attributes if a.is_primary_key]
        non_pk_attrs = [a for a in entity.attributes if not a.is_primary_key]
        ordered_attrs = pk_attrs + non_pk_attrs

        col_defs = []
        for attr in ordered_attrs:
            try:
                pg_type = attr.data_type.to_postgres_sql()
            except Exception as e:
                raise UnsupportedTypeMappingError(
                    f"Failed to map attribute '{attr.name}' data type: {e}",
                    attribute_name=attr.name,
                    type_name=str(attr.data_type),
                )

            null_clause = " NOT NULL" if not attr.is_nullable or attr.is_primary_key else ""
            default_clause = f" DEFAULT {attr.default_value}" if attr.default_value else ""
            col_defs.append(f"    {attr.name.lower()} {pg_type}{null_clause}{default_clause}")

        # 2. Add Primary Key constraint
        if pk_attrs:
            pk_col_names = ", ".join([a.name.lower() for a in pk_attrs])
            col_defs.append(f"    CONSTRAINT pk_{table_name} PRIMARY KEY ({pk_col_names})")

        # 3. Add Foreign Key constraints
        for rel in entity.relations:
            # target entity table name
            target_table = rel.target_entity_uri.split("/")[-1].lower()
            fk_name = f"fk_{table_name}_{rel.source_attribute.lower()}"
            col_defs.append(
                f"    CONSTRAINT {fk_name} FOREIGN KEY ({rel.source_attribute.lower()}) REFERENCES {schema}.{target_table} ({rel.target_attribute.lower()})"
            )

        ddl_body = ",\n".join(col_defs)
        create_table = f"CREATE TABLE IF NOT EXISTS {full_table_name} (\n{ddl_body}\n);"

        # 4. Generate comments and unique indexes
        extra_statements = []
        if entity.description:
            clean_desc = entity.description.replace("'", "''")
            extra_statements.append(f"COMMENT ON TABLE {full_table_name} IS '{clean_desc}';")

        for attr in ordered_attrs:
            if attr.description:
                clean_attr_desc = attr.description.replace("'", "''")
                extra_statements.append(f"COMMENT ON COLUMN {full_table_name}.{attr.name.lower()} IS '{clean_attr_desc}';")
            if attr.is_unique and not attr.is_primary_key:
                extra_statements.append(
                    f"CREATE UNIQUE INDEX IF NOT EXISTS uq_{table_name}_{attr.name.lower()} ON {full_table_name} ({attr.name.lower()});"
                )

        if extra_statements:
            return create_table + "\n\n" + "\n".join(extra_statements)
        return create_table

    @classmethod
    def generate_schema_ddl(cls, entities: List[LogicalEntity], schema: str = "public") -> str:
        """Generate full schema DDL for a collection of logical entities sorted by name."""
        schema_header = f"CREATE SCHEMA IF NOT EXISTS {schema};\n\n"
        sorted_entities = sorted(entities, key=lambda e: e.name)
        tables_ddl = "\n\n".join([cls.to_create_table_ddl(e, schema) for e in sorted_entities])
        return schema_header + tables_ddl
