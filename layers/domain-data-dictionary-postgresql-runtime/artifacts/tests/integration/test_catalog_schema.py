"""PostgreSQL realization, constraint, and round-trip tests."""

import os
from typing import Any

import pytest
from psycopg import AsyncConnection, errors

from domaincatalog_api.settings import Settings

pytestmark = pytest.mark.skipif(
    os.getenv("DOMAINCATALOG_INTEGRATION") != "1",
    reason="set DOMAINCATALOG_INTEGRATION=1 to run database integration tests",
)

Connection = AsyncConnection[tuple[Any, ...]]

OBJECT_IDENTIFIERS = (
    "test:cmof:revision",
    "test:cmof:class",
    "test:property:model",
    "test:property:label",
    "test:datatype:record",
    "test:datatype:text",
    "test:field:name",
    "test:domain",
    "test:status:draft",
    "test:agent-kind:human",
    "test:activity:import",
    "test:model",
)


@pytest.fixture
def settings() -> Settings:
    return Settings.from_environment()


async def insert_catalog_objects(connection: Connection) -> None:
    cursor = connection.cursor()
    await cursor.executemany(
        """
        INSERT INTO catalog.catalog_record (identifier, record_kind)
        VALUES (%s, 'catalog_object')
        """,
        [(identifier,) for identifier in OBJECT_IDENTIFIERS],
    )
    await cursor.executemany(
        """
        INSERT INTO catalog.catalog_object (
            identifier,
            governing_type_identifier,
            governing_definition_revision_identifier
        )
        VALUES (%s, 'test:cmof:class', 'test:cmof:revision')
        """,
        [(identifier,) for identifier in OBJECT_IDENTIFIERS],
    )


async def insert_typed_governance_records(connection: Connection) -> None:
    await connection.execute(
        """
        INSERT INTO catalog.catalog_record (identifier, record_kind)
        VALUES
            ('test:family', 'model_family'),
            ('test:agent', 'responsible_agent'),
            ('test:provenance', 'provenance_record')
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.model_family (
            identifier,
            name,
            purpose,
            business_scope,
            domain_identifier,
            family_status_identifier
        )
        VALUES (
            'test:family',
            'Customer domain models',
            'Explore and refine the customer domain',
            'Customer management',
            'test:domain',
            'test:status:draft'
        )
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.model_family_model_revision (
            model_family_identifier,
            model_revision_identifier
        )
        VALUES ('test:family', 'test:model')
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.responsible_agent (
            identifier,
            name,
            external_identity_reference,
            agent_kind_identifier
        )
        VALUES (
            'test:agent',
            'Domain analyst',
            'urn:test:agent:domain-analyst',
            'test:agent-kind:human'
        )
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.provenance_record (
            identifier,
            recorded_time,
            evidence_digest_algorithm,
            evidence_digest_value,
            rationale,
            activity_kind_identifier
        )
        VALUES (
            'test:provenance',
            '2026-07-26T12:00:00Z',
            'sha256',
            'test-digest',
            'Representative round-trip evidence',
            'test:activity:import'
        )
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.provenance_source_reference (
            provenance_record_identifier,
            source_reference
        )
        VALUES ('test:provenance', 'urn:test:source:domain-workshop')
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.provenance_responsible_agent (
            provenance_record_identifier,
            responsible_agent_identifier
        )
        VALUES ('test:provenance', 'test:agent')
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.provenance_subject (
            provenance_record_identifier,
            subject_identifier
        )
        VALUES ('test:provenance', 'test:model')
        """
    )
    await connection.execute(
        "UPDATE catalog.provenance_record SET sealed = true WHERE identifier = 'test:provenance'"
    )


async def insert_reflective_content(connection: Connection) -> None:
    await connection.execute(
        """
        INSERT INTO catalog.property_occurrence (
            subject_identifier,
            property_definition_identifier,
            position,
            payload_kind,
            reference_target_identifier
        )
        VALUES (
            'test:domain',
            'test:property:model',
            0,
            'reference',
            'test:model'
        )
        """
    )
    await connection.execute(
        """
        INSERT INTO catalog.property_occurrence (
            subject_identifier,
            property_definition_identifier,
            position,
            payload_kind
        )
        VALUES ('test:domain', 'test:property:label', 0, 'value')
        """
    )
    root_cursor = await connection.execute(
        """
        INSERT INTO catalog.value_node (
            subject_identifier,
            property_definition_identifier,
            occurrence_position,
            position,
            role,
            datatype_definition_identifier
        )
        VALUES (
            'test:domain',
            'test:property:label',
            0,
            0,
            'root',
            'test:datatype:record'
        )
        RETURNING value_node_identifier
        """
    )
    root_row = await root_cursor.fetchone()
    assert root_row is not None
    root_identifier = root_row[0]
    await connection.execute(
        """
        INSERT INTO catalog.value_node (
            subject_identifier,
            property_definition_identifier,
            occurrence_position,
            parent_value_node_identifier,
            position,
            role,
            lexical_value,
            datatype_definition_identifier,
            field_definition_identifier
        )
        VALUES (
            'test:domain',
            'test:property:label',
            0,
            %s,
            0,
            'recordField',
            'Customer',
            'test:datatype:text',
            'test:field:name'
        )
        """,
        (root_identifier,),
    )


@pytest.mark.asyncio
async def test_catalog_inventory_is_complete_and_uses_core_postgresql(
    settings: Settings,
) -> None:
    async with await AsyncConnection.connect(settings.database_conninfo) as connection:
        relation_cursor = await connection.execute(
            """
            SELECT object_name
              FROM catalog.deployed_object_inventory
             WHERE object_kind = 'relation'
               AND detail IN ('r', 'p')
            """
        )
        relations = {row[0] async for row in relation_cursor}
        extension_cursor = await connection.execute(
            "SELECT extname FROM pg_catalog.pg_extension ORDER BY extname"
        )
        extensions = [row[0] async for row in extension_cursor]

    assert {
        "catalog_object",
        "model_family",
        "responsible_agent",
        "provenance_record",
        "property_occurrence",
        "value_node",
    } <= relations
    assert extensions == ["plpgsql"]


@pytest.mark.asyncio
async def test_six_authorities_round_trip_without_semantic_loss(settings: Settings) -> None:
    async with (
        await AsyncConnection.connect(settings.database_conninfo) as connection,
        connection.transaction(force_rollback=True),
    ):
        await insert_catalog_objects(connection)
        await insert_typed_governance_records(connection)
        await insert_reflective_content(connection)
        await connection.execute("SET CONSTRAINTS ALL IMMEDIATE")

        family_cursor = await connection.execute(
            """
                SELECT
                    family.identifier,
                    family.name,
                    family.purpose,
                    family.business_scope,
                    family.domain_identifier,
                    family.family_status_identifier,
                    member.model_revision_identifier
                FROM catalog.model_family AS family
                JOIN catalog.model_family_model_revision AS member
                  ON member.model_family_identifier = family.identifier
                WHERE family.identifier = 'test:family'
                """
        )
        family = await family_cursor.fetchone()

        provenance_cursor = await connection.execute(
            """
                SELECT
                    provenance.identifier,
                    provenance.sealed,
                    count(DISTINCT agent.responsible_agent_identifier),
                    count(DISTINCT subject.subject_identifier)
                FROM catalog.provenance_record AS provenance
                JOIN catalog.provenance_responsible_agent AS agent
                  ON agent.provenance_record_identifier = provenance.identifier
                JOIN catalog.provenance_subject AS subject
                  ON subject.provenance_record_identifier = provenance.identifier
                WHERE provenance.identifier = 'test:provenance'
                GROUP BY provenance.identifier, provenance.sealed
                """
        )
        provenance = await provenance_cursor.fetchone()

        occurrence_cursor = await connection.execute(
            """
                SELECT payload_kind::text, reference_target_identifier
                  FROM catalog.property_occurrence
                 WHERE subject_identifier = 'test:domain'
                 ORDER BY property_definition_identifier
                """
        )
        occurrences = [row async for row in occurrence_cursor]

        path_cursor = await connection.execute(
            """
                SELECT value_path, lexical_value
                  FROM catalog.value_node_with_path
                 WHERE subject_identifier = 'test:domain'
                   AND property_definition_identifier = 'test:property:label'
                 ORDER BY value_path
                """
        )
        paths = [row async for row in path_cursor]

        agent_cursor = await connection.execute(
            """
                SELECT name, external_identity_reference, agent_kind_identifier
                  FROM catalog.responsible_agent
                 WHERE identifier = 'test:agent'
                """
        )
        agent = await agent_cursor.fetchone()

    field_hex = b"test:field:name".hex()
    assert family == (
        "test:family",
        "Customer domain models",
        "Explore and refine the customer domain",
        "Customer management",
        "test:domain",
        "test:status:draft",
        "test:model",
    )
    assert agent == (
        "Domain analyst",
        "urn:test:agent:domain-analyst",
        "test:agent-kind:human",
    )
    assert provenance == ("test:provenance", True, 1, 1)
    assert occurrences == [("value", None), ("reference", "test:model")]
    assert paths == [
        ("$", None),
        (f"$/recordField[0]{{{field_hex}}}", "Customer"),
    ]


@pytest.mark.asyncio
async def test_deferred_constraints_reject_incomplete_value_and_provenance(
    settings: Settings,
) -> None:
    async with await AsyncConnection.connect(settings.database_conninfo) as connection:
        async with connection.transaction(force_rollback=True):
            await insert_catalog_objects(connection)
            await connection.execute(
                """
                INSERT INTO catalog.property_occurrence (
                    subject_identifier,
                    property_definition_identifier,
                    position,
                    payload_kind
                )
                VALUES ('test:domain', 'test:property:label', 0, 'value')
                """
            )

            with pytest.raises(errors.CheckViolation, match="exactly one value root"):
                async with connection.transaction():
                    await connection.execute("SET CONSTRAINTS ALL IMMEDIATE")

        async with connection.transaction(force_rollback=True):
            await insert_catalog_objects(connection)
            await connection.execute(
                """
                INSERT INTO catalog.catalog_record (identifier, record_kind)
                VALUES ('test:provenance', 'provenance_record')
                """
            )
            await connection.execute(
                """
                INSERT INTO catalog.provenance_record (
                    identifier,
                    recorded_time,
                    activity_kind_identifier,
                    sealed
                )
                VALUES (
                    'test:provenance',
                    '2026-07-26T12:00:00Z',
                    'test:activity:import',
                    true
                )
                """
            )

            with pytest.raises(errors.CheckViolation, match="at least one agent and subject"):
                async with connection.transaction():
                    await connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


@pytest.mark.asyncio
async def test_deferred_constraints_reject_value_tree_cycles(settings: Settings) -> None:
    async with (
        await AsyncConnection.connect(settings.database_conninfo) as connection,
        connection.transaction(force_rollback=True),
    ):
        await insert_catalog_objects(connection)
        await connection.execute(
            """
                INSERT INTO catalog.property_occurrence (
                    subject_identifier,
                    property_definition_identifier,
                    position,
                    payload_kind
                )
                VALUES ('test:domain', 'test:property:label', 0, 'value')
                """
        )
        root_cursor = await connection.execute(
            """
                INSERT INTO catalog.value_node (
                    subject_identifier,
                    property_definition_identifier,
                    occurrence_position,
                    position,
                    role,
                    datatype_definition_identifier
                )
                VALUES (
                    'test:domain',
                    'test:property:label',
                    0,
                    0,
                    'root',
                    'test:datatype:record'
                )
                RETURNING value_node_identifier
                """
        )
        root = await root_cursor.fetchone()
        assert root is not None
        child_cursor = await connection.execute(
            """
                INSERT INTO catalog.value_node (
                    subject_identifier,
                    property_definition_identifier,
                    occurrence_position,
                    parent_value_node_identifier,
                    position,
                    role,
                    datatype_definition_identifier
                )
                VALUES
                    (
                        'test:domain', 'test:property:label', 0, %s, 0,
                        'collectionItem', 'test:datatype:record'
                    ),
                    (
                        'test:domain', 'test:property:label', 0, %s, 1,
                        'collectionItem', 'test:datatype:record'
                    )
                RETURNING value_node_identifier
                """,
            (root[0], root[0]),
        )
        children = [row[0] async for row in child_cursor]
        await connection.execute(
            """
                UPDATE catalog.value_node
                   SET parent_value_node_identifier = CASE value_node_identifier
                       WHEN %s THEN %s
                       WHEN %s THEN %s
                   END
                 WHERE value_node_identifier IN (%s, %s)
                """,
            (children[0], children[1], children[1], children[0], *children),
        )

        with pytest.raises(errors.CheckViolation, match="contains a cycle"):
            async with connection.transaction():
                await connection.execute("SET CONSTRAINTS ALL IMMEDIATE")


@pytest.mark.asyncio
async def test_sealed_provenance_is_immutable(settings: Settings) -> None:
    async with (
        await AsyncConnection.connect(settings.database_conninfo) as connection,
        connection.transaction(force_rollback=True),
    ):
        await insert_catalog_objects(connection)
        await insert_typed_governance_records(connection)
        await connection.execute("SET CONSTRAINTS ALL IMMEDIATE")

        with pytest.raises(errors.CheckViolation, match="is immutable"):
            async with connection.transaction():
                await connection.execute(
                    """
                        UPDATE catalog.provenance_record
                           SET rationale = 'impermissible rewrite'
                         WHERE identifier = 'test:provenance'
                        """
                )
