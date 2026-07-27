CREATE SCHEMA catalog;

COMMENT ON SCHEMA catalog IS
    'PostgreSQL realization of CAT-LOG/domain-data-dictionary@1 revision 5728636';

CREATE DOMAIN catalog.catalog_identifier AS text
    CHECK (VALUE <> '' AND VALUE = btrim(VALUE));

CREATE TYPE catalog.catalog_record_kind AS ENUM (
    'catalog_object',
    'model_family',
    'responsible_agent',
    'provenance_record'
);

CREATE TYPE catalog.occurrence_payload_kind AS ENUM ('reference', 'value');

CREATE TYPE catalog.value_role AS ENUM (
    'root',
    'recordField',
    'collectionItem',
    'mapEntry',
    'mapKey',
    'mapValue',
    'choiceAlternative'
);

CREATE TABLE catalog.catalog_record (
    identifier catalog.catalog_identifier PRIMARY KEY,
    record_kind catalog.catalog_record_kind NOT NULL,
    CONSTRAINT uq_catalog_record_identifier_kind UNIQUE (identifier, record_kind)
);

COMMENT ON TABLE catalog.catalog_record IS
    'Physical identity registry enforcing one CatalogIdentifier namespace; not a separate logical authority';

CREATE TABLE catalog.catalog_object (
    identifier catalog.catalog_identifier PRIMARY KEY,
    record_kind catalog.catalog_record_kind NOT NULL DEFAULT 'catalog_object',
    governing_type_identifier catalog.catalog_identifier NOT NULL,
    governing_definition_revision_identifier catalog.catalog_identifier NOT NULL,
    CONSTRAINT ck_catalog_object_record_kind
        CHECK (record_kind = 'catalog_object'),
    CONSTRAINT fk_catalog_object_record
        FOREIGN KEY (identifier, record_kind)
        REFERENCES catalog.catalog_record (identifier, record_kind)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_catalog_object_governing_type
        FOREIGN KEY (governing_type_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_catalog_object_definition_revision
        FOREIGN KEY (governing_definition_revision_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.model_family (
    identifier catalog.catalog_identifier PRIMARY KEY,
    record_kind catalog.catalog_record_kind NOT NULL DEFAULT 'model_family',
    name text NOT NULL CHECK (name <> ''),
    purpose text NOT NULL CHECK (purpose <> ''),
    business_scope text NOT NULL CHECK (business_scope <> ''),
    domain_identifier catalog.catalog_identifier NOT NULL,
    family_status_identifier catalog.catalog_identifier NOT NULL,
    CONSTRAINT ck_model_family_record_kind
        CHECK (record_kind = 'model_family'),
    CONSTRAINT fk_model_family_record
        FOREIGN KEY (identifier, record_kind)
        REFERENCES catalog.catalog_record (identifier, record_kind)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_model_family_domain
        FOREIGN KEY (domain_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_model_family_status
        FOREIGN KEY (family_status_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.model_family_model_revision (
    model_family_identifier catalog.catalog_identifier NOT NULL,
    model_revision_identifier catalog.catalog_identifier NOT NULL,
    PRIMARY KEY (model_family_identifier, model_revision_identifier),
    CONSTRAINT uq_model_revision_family UNIQUE (model_revision_identifier),
    CONSTRAINT fk_model_family_member_family
        FOREIGN KEY (model_family_identifier)
        REFERENCES catalog.model_family (identifier)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_model_family_member_revision
        FOREIGN KEY (model_revision_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.responsible_agent (
    identifier catalog.catalog_identifier PRIMARY KEY,
    record_kind catalog.catalog_record_kind NOT NULL DEFAULT 'responsible_agent',
    name text NOT NULL CHECK (name <> ''),
    external_identity_reference text,
    agent_kind_identifier catalog.catalog_identifier NOT NULL,
    CONSTRAINT ck_responsible_agent_record_kind
        CHECK (record_kind = 'responsible_agent'),
    CONSTRAINT ck_responsible_agent_external_identity
        CHECK (external_identity_reference IS NULL OR external_identity_reference <> ''),
    CONSTRAINT fk_responsible_agent_record
        FOREIGN KEY (identifier, record_kind)
        REFERENCES catalog.catalog_record (identifier, record_kind)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_responsible_agent_kind
        FOREIGN KEY (agent_kind_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.provenance_record (
    identifier catalog.catalog_identifier PRIMARY KEY,
    record_kind catalog.catalog_record_kind NOT NULL DEFAULT 'provenance_record',
    recorded_time timestamp with time zone NOT NULL,
    evidence_digest_algorithm text,
    evidence_digest_value text,
    rationale text,
    activity_kind_identifier catalog.catalog_identifier NOT NULL,
    sealed boolean NOT NULL DEFAULT false,
    CONSTRAINT ck_provenance_record_kind
        CHECK (record_kind = 'provenance_record'),
    CONSTRAINT ck_provenance_evidence_digest_pair
        CHECK (
            (evidence_digest_algorithm IS NULL) =
            (evidence_digest_value IS NULL)
        ),
    CONSTRAINT ck_provenance_evidence_digest_nonempty
        CHECK (
            evidence_digest_algorithm IS NULL OR
            (evidence_digest_algorithm <> '' AND evidence_digest_value <> '')
        ),
    CONSTRAINT fk_provenance_record
        FOREIGN KEY (identifier, record_kind)
        REFERENCES catalog.catalog_record (identifier, record_kind)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_provenance_activity_kind
        FOREIGN KEY (activity_kind_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

COMMENT ON COLUMN catalog.provenance_record.sealed IS
    'Physical construction state; deferred constraints require true before commit';

CREATE TABLE catalog.provenance_source_reference (
    provenance_record_identifier catalog.catalog_identifier NOT NULL,
    source_reference text NOT NULL CHECK (source_reference <> ''),
    PRIMARY KEY (provenance_record_identifier, source_reference),
    CONSTRAINT fk_provenance_source_record
        FOREIGN KEY (provenance_record_identifier)
        REFERENCES catalog.provenance_record (identifier)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.provenance_responsible_agent (
    provenance_record_identifier catalog.catalog_identifier NOT NULL,
    responsible_agent_identifier catalog.catalog_identifier NOT NULL,
    PRIMARY KEY (provenance_record_identifier, responsible_agent_identifier),
    CONSTRAINT fk_provenance_agent_record
        FOREIGN KEY (provenance_record_identifier)
        REFERENCES catalog.provenance_record (identifier)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_provenance_agent_agent
        FOREIGN KEY (responsible_agent_identifier)
        REFERENCES catalog.responsible_agent (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.provenance_subject (
    provenance_record_identifier catalog.catalog_identifier NOT NULL,
    subject_identifier catalog.catalog_identifier NOT NULL,
    PRIMARY KEY (provenance_record_identifier, subject_identifier),
    CONSTRAINT fk_provenance_subject_record
        FOREIGN KEY (provenance_record_identifier)
        REFERENCES catalog.provenance_record (identifier)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_provenance_subject_object
        FOREIGN KEY (subject_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.property_occurrence (
    subject_identifier catalog.catalog_identifier NOT NULL,
    property_definition_identifier catalog.catalog_identifier NOT NULL,
    position bigint NOT NULL CHECK (position >= 0),
    payload_kind catalog.occurrence_payload_kind NOT NULL,
    reference_target_identifier catalog.catalog_identifier,
    PRIMARY KEY (subject_identifier, property_definition_identifier, position),
    CONSTRAINT ck_property_occurrence_payload_columns
        CHECK (
            (payload_kind = 'reference' AND reference_target_identifier IS NOT NULL) OR
            (payload_kind = 'value' AND reference_target_identifier IS NULL)
        ),
    CONSTRAINT fk_property_occurrence_subject
        FOREIGN KEY (subject_identifier)
        REFERENCES catalog.catalog_object (identifier)
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_property_occurrence_definition
        FOREIGN KEY (property_definition_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_property_occurrence_reference_target
        FOREIGN KEY (reference_target_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE catalog.value_node (
    value_node_identifier bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    subject_identifier catalog.catalog_identifier NOT NULL,
    property_definition_identifier catalog.catalog_identifier NOT NULL,
    occurrence_position bigint NOT NULL CHECK (occurrence_position >= 0),
    parent_value_node_identifier bigint,
    position bigint NOT NULL CHECK (position >= 0),
    role catalog.value_role NOT NULL,
    lexical_value text,
    content_reference text,
    content_digest_algorithm text,
    content_digest_value text,
    datatype_definition_identifier catalog.catalog_identifier NOT NULL,
    field_definition_identifier catalog.catalog_identifier,
    CONSTRAINT uq_value_node_context
        UNIQUE (
            value_node_identifier,
            subject_identifier,
            property_definition_identifier,
            occurrence_position
        ),
    CONSTRAINT ck_value_node_root_parent
        CHECK (
            (parent_value_node_identifier IS NULL AND role = 'root' AND position = 0) OR
            (parent_value_node_identifier IS NOT NULL AND role <> 'root')
        ),
    CONSTRAINT ck_value_node_field_role
        CHECK (
            (
                role IN ('recordField', 'choiceAlternative') AND
                field_definition_identifier IS NOT NULL
            ) OR
            (
                role NOT IN ('recordField', 'choiceAlternative') AND
                field_definition_identifier IS NULL
            )
        ),
    CONSTRAINT ck_value_node_content_carrier
        CHECK (num_nonnulls(lexical_value, content_reference) <= 1),
    CONSTRAINT ck_value_node_content_reference
        CHECK (content_reference IS NULL OR content_reference <> ''),
    CONSTRAINT ck_value_node_digest_pair
        CHECK (
            (content_digest_algorithm IS NULL) =
            (content_digest_value IS NULL)
        ),
    CONSTRAINT ck_value_node_digest_nonempty
        CHECK (
            content_digest_algorithm IS NULL OR
            (
                content_digest_algorithm <> '' AND
                content_digest_value <> '' AND
                num_nonnulls(lexical_value, content_reference) = 1
            )
        ),
    CONSTRAINT fk_value_node_occurrence
        FOREIGN KEY (
            subject_identifier,
            property_definition_identifier,
            occurrence_position
        )
        REFERENCES catalog.property_occurrence (
            subject_identifier,
            property_definition_identifier,
            position
        )
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_value_node_parent
        FOREIGN KEY (
            parent_value_node_identifier,
            subject_identifier,
            property_definition_identifier,
            occurrence_position
        )
        REFERENCES catalog.value_node (
            value_node_identifier,
            subject_identifier,
            property_definition_identifier,
            occurrence_position
        )
        ON DELETE CASCADE
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_value_node_datatype_definition
        FOREIGN KEY (datatype_definition_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED,
    CONSTRAINT fk_value_node_field_definition
        FOREIGN KEY (field_definition_identifier)
        REFERENCES catalog.catalog_object (identifier)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE INDEX ix_catalog_object_governing_type
    ON catalog.catalog_object (governing_type_identifier);
CREATE INDEX ix_catalog_object_definition_revision
    ON catalog.catalog_object (governing_definition_revision_identifier);
CREATE INDEX ix_model_family_domain
    ON catalog.model_family (domain_identifier);
CREATE INDEX ix_model_family_status
    ON catalog.model_family (family_status_identifier);
CREATE INDEX ix_model_family_member_family
    ON catalog.model_family_model_revision (model_family_identifier);
CREATE INDEX ix_responsible_agent_kind
    ON catalog.responsible_agent (agent_kind_identifier);
CREATE INDEX ix_provenance_activity_kind
    ON catalog.provenance_record (activity_kind_identifier);
CREATE INDEX ix_provenance_agent_agent
    ON catalog.provenance_responsible_agent (responsible_agent_identifier);
CREATE INDEX ix_provenance_subject_subject
    ON catalog.provenance_subject (subject_identifier);
CREATE INDEX ix_property_occurrence_definition
    ON catalog.property_occurrence (property_definition_identifier);
CREATE INDEX ix_property_occurrence_reference_target
    ON catalog.property_occurrence (reference_target_identifier)
    WHERE reference_target_identifier IS NOT NULL;
CREATE INDEX ix_value_node_occurrence
    ON catalog.value_node (
        subject_identifier,
        property_definition_identifier,
        occurrence_position
    );
CREATE INDEX ix_value_node_parent
    ON catalog.value_node (parent_value_node_identifier)
    WHERE parent_value_node_identifier IS NOT NULL;
CREATE INDEX ix_value_node_datatype_definition
    ON catalog.value_node (datatype_definition_identifier);
CREATE INDEX ix_value_node_field_definition
    ON catalog.value_node (field_definition_identifier)
    WHERE field_definition_identifier IS NOT NULL;

CREATE UNIQUE INDEX uq_value_node_sibling
    ON catalog.value_node (
        subject_identifier,
        property_definition_identifier,
        occurrence_position,
        parent_value_node_identifier,
        role,
        field_definition_identifier,
        position
    ) NULLS NOT DISTINCT;

CREATE FUNCTION catalog.reject_catalog_identity_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
BEGIN
    IF OLD.identifier IS DISTINCT FROM NEW.identifier OR
       OLD.record_kind IS DISTINCT FROM NEW.record_kind THEN
        RAISE EXCEPTION 'catalog identity and record kind are immutable'
            USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER reject_catalog_record_identity_change
    BEFORE UPDATE OF identifier, record_kind ON catalog.catalog_record
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_catalog_identity_change();
CREATE TRIGGER reject_catalog_object_identity_change
    BEFORE UPDATE OF identifier, record_kind ON catalog.catalog_object
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_catalog_identity_change();
CREATE TRIGGER reject_model_family_identity_change
    BEFORE UPDATE OF identifier, record_kind ON catalog.model_family
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_catalog_identity_change();
CREATE TRIGGER reject_responsible_agent_identity_change
    BEFORE UPDATE OF identifier, record_kind ON catalog.responsible_agent
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_catalog_identity_change();
CREATE TRIGGER reject_provenance_record_identity_change
    BEFORE UPDATE OF identifier, record_kind ON catalog.provenance_record
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_catalog_identity_change();

CREATE FUNCTION catalog.assert_catalog_record_subtype()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
DECLARE
    record_identifier catalog.catalog_identifier;
    expected_kind catalog.catalog_record_kind;
    subtype_exists boolean;
BEGIN
    IF TG_OP = 'DELETE' THEN
        record_identifier := OLD.identifier;
    ELSE
        record_identifier := NEW.identifier;
    END IF;

    SELECT record_kind
      INTO expected_kind
      FROM catalog.catalog_record
     WHERE identifier = record_identifier;

    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    CASE expected_kind
        WHEN 'catalog_object' THEN
            SELECT EXISTS (
                SELECT 1 FROM catalog.catalog_object WHERE identifier = record_identifier
            ) INTO subtype_exists;
        WHEN 'model_family' THEN
            SELECT EXISTS (
                SELECT 1 FROM catalog.model_family WHERE identifier = record_identifier
            ) INTO subtype_exists;
        WHEN 'responsible_agent' THEN
            SELECT EXISTS (
                SELECT 1 FROM catalog.responsible_agent WHERE identifier = record_identifier
            ) INTO subtype_exists;
        WHEN 'provenance_record' THEN
            SELECT EXISTS (
                SELECT 1 FROM catalog.provenance_record WHERE identifier = record_identifier
            ) INTO subtype_exists;
    END CASE;

    IF NOT subtype_exists THEN
        RAISE EXCEPTION 'catalog record % lacks required % subtype',
            record_identifier, expected_kind
            USING ERRCODE = '23514';
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER catalog_record_requires_subtype
    AFTER INSERT OR UPDATE ON catalog.catalog_record
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_catalog_record_subtype();
CREATE CONSTRAINT TRIGGER catalog_object_preserves_subtype
    AFTER INSERT OR UPDATE OR DELETE ON catalog.catalog_object
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_catalog_record_subtype();
CREATE CONSTRAINT TRIGGER model_family_preserves_subtype
    AFTER INSERT OR UPDATE OR DELETE ON catalog.model_family
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_catalog_record_subtype();
CREATE CONSTRAINT TRIGGER responsible_agent_preserves_subtype
    AFTER INSERT OR UPDATE OR DELETE ON catalog.responsible_agent
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_catalog_record_subtype();
CREATE CONSTRAINT TRIGGER provenance_record_preserves_subtype
    AFTER INSERT OR UPDATE OR DELETE ON catalog.provenance_record
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_catalog_record_subtype();

CREATE FUNCTION catalog.reject_property_occurrence_identity_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
BEGIN
    IF OLD.subject_identifier IS DISTINCT FROM NEW.subject_identifier OR
       OLD.property_definition_identifier IS DISTINCT FROM NEW.property_definition_identifier OR
       OLD.position IS DISTINCT FROM NEW.position THEN
        RAISE EXCEPTION 'property occurrence logical identity is immutable'
            USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER reject_property_occurrence_identity_change
    BEFORE UPDATE OF subject_identifier, property_definition_identifier, position
    ON catalog.property_occurrence
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_property_occurrence_identity_change();

CREATE FUNCTION catalog.reject_value_node_identity_change()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
BEGIN
    IF OLD.value_node_identifier IS DISTINCT FROM NEW.value_node_identifier OR
       OLD.subject_identifier IS DISTINCT FROM NEW.subject_identifier OR
       OLD.property_definition_identifier IS DISTINCT FROM NEW.property_definition_identifier OR
       OLD.occurrence_position IS DISTINCT FROM NEW.occurrence_position THEN
        RAISE EXCEPTION 'value node physical identity and owning occurrence are immutable'
            USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER reject_value_node_identity_change
    BEFORE UPDATE OF
        value_node_identifier,
        subject_identifier,
        property_definition_identifier,
        occurrence_position
    ON catalog.value_node
    FOR EACH ROW EXECUTE FUNCTION catalog.reject_value_node_identity_change();

CREATE FUNCTION catalog.assert_property_occurrence_payload()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
DECLARE
    affected_subject catalog.catalog_identifier;
    affected_definition catalog.catalog_identifier;
    affected_position bigint;
    occurrence_kind catalog.occurrence_payload_kind;
    root_count bigint;
BEGIN
    IF TG_TABLE_NAME = 'property_occurrence' THEN
        IF TG_OP = 'DELETE' THEN
            affected_subject := OLD.subject_identifier;
            affected_definition := OLD.property_definition_identifier;
            affected_position := OLD.position;
        ELSE
            affected_subject := NEW.subject_identifier;
            affected_definition := NEW.property_definition_identifier;
            affected_position := NEW.position;
        END IF;
    ELSE
        IF TG_OP = 'DELETE' THEN
            affected_subject := OLD.subject_identifier;
            affected_definition := OLD.property_definition_identifier;
            affected_position := OLD.occurrence_position;
        ELSE
            affected_subject := NEW.subject_identifier;
            affected_definition := NEW.property_definition_identifier;
            affected_position := NEW.occurrence_position;
        END IF;
    END IF;

    SELECT payload_kind
      INTO occurrence_kind
      FROM catalog.property_occurrence
     WHERE subject_identifier = affected_subject
       AND property_definition_identifier = affected_definition
       AND position = affected_position;

    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    SELECT count(*)
      INTO root_count
      FROM catalog.value_node
     WHERE subject_identifier = affected_subject
       AND property_definition_identifier = affected_definition
       AND occurrence_position = affected_position
       AND parent_value_node_identifier IS NULL;

    IF occurrence_kind = 'reference' AND root_count <> 0 THEN
        RAISE EXCEPTION 'reference occurrence (%, %, %) cannot own value roots',
            affected_subject, affected_definition, affected_position
            USING ERRCODE = '23514';
    ELSIF occurrence_kind = 'value' AND root_count <> 1 THEN
        RAISE EXCEPTION 'value occurrence (%, %, %) must own exactly one value root; found %',
            affected_subject, affected_definition, affected_position, root_count
            USING ERRCODE = '23514';
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER property_occurrence_payload_is_complete
    AFTER INSERT OR UPDATE OR DELETE ON catalog.property_occurrence
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_property_occurrence_payload();
CREATE CONSTRAINT TRIGGER value_node_preserves_occurrence_payload
    AFTER INSERT OR UPDATE OR DELETE ON catalog.value_node
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_property_occurrence_payload();

CREATE FUNCTION catalog.assert_value_node_tree()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
DECLARE
    affected_subject catalog.catalog_identifier;
    affected_definition catalog.catalog_identifier;
    affected_position bigint;
    has_cycle boolean;
    payload_has_children boolean;
BEGIN
    IF TG_OP = 'DELETE' THEN
        affected_subject := OLD.subject_identifier;
        affected_definition := OLD.property_definition_identifier;
        affected_position := OLD.occurrence_position;
    ELSE
        affected_subject := NEW.subject_identifier;
        affected_definition := NEW.property_definition_identifier;
        affected_position := NEW.occurrence_position;
    END IF;

    IF NOT EXISTS (
        SELECT 1
          FROM catalog.value_node
         WHERE subject_identifier = affected_subject
           AND property_definition_identifier = affected_definition
           AND occurrence_position = affected_position
    ) THEN
        RETURN NULL;
    END IF;

    WITH RECURSIVE ancestry AS (
        SELECT
            node.value_node_identifier AS start_identifier,
            node.value_node_identifier,
            node.parent_value_node_identifier,
            ARRAY[node.value_node_identifier]::bigint[] AS visited,
            false AS cycle
        FROM catalog.value_node AS node
        WHERE node.subject_identifier = affected_subject
          AND node.property_definition_identifier = affected_definition
          AND node.occurrence_position = affected_position

        UNION ALL

        SELECT
            ancestry.start_identifier,
            parent.value_node_identifier,
            parent.parent_value_node_identifier,
            ancestry.visited || parent.value_node_identifier,
            parent.value_node_identifier = ANY(ancestry.visited)
        FROM ancestry
        JOIN catalog.value_node AS parent
          ON parent.value_node_identifier = ancestry.parent_value_node_identifier
        WHERE NOT ancestry.cycle
    )
    SELECT EXISTS (SELECT 1 FROM ancestry WHERE cycle)
      INTO has_cycle;

    IF has_cycle THEN
        RAISE EXCEPTION 'value-node occurrence (%, %, %) contains a cycle',
            affected_subject, affected_definition, affected_position
            USING ERRCODE = '23514';
    END IF;

    SELECT EXISTS (
        SELECT 1
          FROM catalog.value_node AS parent
         WHERE parent.subject_identifier = affected_subject
           AND parent.property_definition_identifier = affected_definition
           AND parent.occurrence_position = affected_position
           AND num_nonnulls(parent.lexical_value, parent.content_reference) > 0
           AND EXISTS (
               SELECT 1
                 FROM catalog.value_node AS child
                WHERE child.parent_value_node_identifier = parent.value_node_identifier
           )
    ) INTO payload_has_children;

    IF payload_has_children THEN
        RAISE EXCEPTION 'value-node payload carrier cannot also have children'
            USING ERRCODE = '23514';
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER value_node_tree_is_valid
    AFTER INSERT OR UPDATE OR DELETE ON catalog.value_node
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_value_node_tree();

CREATE FUNCTION catalog.guard_provenance_record_mutation()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
BEGIN
    IF OLD.sealed THEN
        RAISE EXCEPTION 'sealed provenance record % is immutable', OLD.identifier
            USING ERRCODE = '23514';
    END IF;
    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER guard_provenance_record_mutation
    BEFORE UPDATE OR DELETE ON catalog.provenance_record
    FOR EACH ROW EXECUTE FUNCTION catalog.guard_provenance_record_mutation();

CREATE FUNCTION catalog.guard_provenance_dependent_mutation()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
DECLARE
    old_record_identifier catalog.catalog_identifier;
    new_record_identifier catalog.catalog_identifier;
BEGIN
    IF TG_OP <> 'INSERT' THEN
        old_record_identifier := OLD.provenance_record_identifier;
        IF EXISTS (
            SELECT 1
              FROM catalog.provenance_record
             WHERE identifier = old_record_identifier
               AND sealed
        ) THEN
            RAISE EXCEPTION 'dependents of sealed provenance record % are immutable',
                old_record_identifier
                USING ERRCODE = '23514';
        END IF;
    END IF;

    IF TG_OP <> 'DELETE' THEN
        new_record_identifier := NEW.provenance_record_identifier;
        IF EXISTS (
            SELECT 1
              FROM catalog.provenance_record
             WHERE identifier = new_record_identifier
               AND sealed
        ) THEN
            RAISE EXCEPTION 'dependents cannot be added to sealed provenance record %',
                new_record_identifier
                USING ERRCODE = '23514';
        END IF;
    END IF;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$;

CREATE TRIGGER guard_provenance_source_mutation
    BEFORE INSERT OR UPDATE OR DELETE ON catalog.provenance_source_reference
    FOR EACH ROW EXECUTE FUNCTION catalog.guard_provenance_dependent_mutation();
CREATE TRIGGER guard_provenance_agent_mutation
    BEFORE INSERT OR UPDATE OR DELETE ON catalog.provenance_responsible_agent
    FOR EACH ROW EXECUTE FUNCTION catalog.guard_provenance_dependent_mutation();
CREATE TRIGGER guard_provenance_subject_mutation
    BEFORE INSERT OR UPDATE OR DELETE ON catalog.provenance_subject
    FOR EACH ROW EXECUTE FUNCTION catalog.guard_provenance_dependent_mutation();

CREATE FUNCTION catalog.assert_provenance_complete()
RETURNS trigger
LANGUAGE plpgsql
SET search_path = pg_catalog, catalog
AS $$
DECLARE
    record_identifier catalog.catalog_identifier;
    is_sealed boolean;
    agent_count bigint;
    subject_count bigint;
BEGIN
    IF TG_TABLE_NAME = 'provenance_record' THEN
        record_identifier := CASE WHEN TG_OP = 'DELETE' THEN OLD.identifier ELSE NEW.identifier END;
    ELSE
        record_identifier := CASE
            WHEN TG_OP = 'DELETE' THEN OLD.provenance_record_identifier
            ELSE NEW.provenance_record_identifier
        END;
    END IF;

    SELECT sealed
      INTO is_sealed
      FROM catalog.provenance_record
     WHERE identifier = record_identifier;

    IF NOT FOUND THEN
        RETURN NULL;
    END IF;

    SELECT count(*)
      INTO agent_count
      FROM catalog.provenance_responsible_agent
     WHERE provenance_record_identifier = record_identifier;
    SELECT count(*)
      INTO subject_count
      FROM catalog.provenance_subject
     WHERE provenance_record_identifier = record_identifier;

    IF NOT is_sealed OR agent_count < 1 OR subject_count < 1 THEN
        RAISE EXCEPTION
            'provenance record % must be sealed with at least one agent and subject',
            record_identifier
            USING ERRCODE = '23514';
    END IF;

    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER provenance_record_is_complete
    AFTER INSERT OR UPDATE OR DELETE ON catalog.provenance_record
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_provenance_complete();
CREATE CONSTRAINT TRIGGER provenance_source_preserves_completeness
    AFTER INSERT OR UPDATE OR DELETE ON catalog.provenance_source_reference
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_provenance_complete();
CREATE CONSTRAINT TRIGGER provenance_agent_preserves_completeness
    AFTER INSERT OR UPDATE OR DELETE ON catalog.provenance_responsible_agent
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_provenance_complete();
CREATE CONSTRAINT TRIGGER provenance_subject_preserves_completeness
    AFTER INSERT OR UPDATE OR DELETE ON catalog.provenance_subject
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION catalog.assert_provenance_complete();

CREATE VIEW catalog.value_node_with_path AS
WITH RECURSIVE node_path AS (
    SELECT
        node.value_node_identifier,
        node.subject_identifier,
        node.property_definition_identifier,
        node.occurrence_position,
        node.parent_value_node_identifier,
        node.position,
        node.role,
        node.lexical_value,
        node.content_reference,
        node.content_digest_algorithm,
        node.content_digest_value,
        node.datatype_definition_identifier,
        node.field_definition_identifier,
        '$'::text AS value_path
    FROM catalog.value_node AS node
    WHERE node.parent_value_node_identifier IS NULL

    UNION ALL

    SELECT
        child.value_node_identifier,
        child.subject_identifier,
        child.property_definition_identifier,
        child.occurrence_position,
        child.parent_value_node_identifier,
        child.position,
        child.role,
        child.lexical_value,
        child.content_reference,
        child.content_digest_algorithm,
        child.content_digest_value,
        child.datatype_definition_identifier,
        child.field_definition_identifier,
        parent.value_path || '/' || child.role::text || '[' || child.position::text || ']' ||
            CASE
                WHEN child.field_definition_identifier IS NULL THEN ''
                ELSE '{' || encode(
                    convert_to(child.field_definition_identifier::text, 'UTF8'),
                    'hex'
                ) || '}'
            END
    FROM node_path AS parent
    JOIN catalog.value_node AS child
      ON child.parent_value_node_identifier = parent.value_node_identifier
)
SELECT * FROM node_path;

COMMENT ON VIEW catalog.value_node_with_path IS
    'Read-only derivation of CAT-LOG ValuePath from occurrence-owned value-node trees';

CREATE VIEW catalog.deployed_object_inventory AS
SELECT
    'relation'::text AS object_kind,
    namespace.nspname::text AS schema_name,
    relation.relname::text AS object_name,
    relation.relkind::text AS detail
FROM pg_catalog.pg_class AS relation
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'column'::text,
    namespace.nspname::text,
    relation.relname::text,
    attribute.attname::text
FROM pg_catalog.pg_attribute AS attribute
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = attribute.attrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname = 'catalog'
  AND attribute.attnum > 0
  AND NOT attribute.attisdropped

UNION ALL

SELECT
    'constraint'::text,
    namespace.nspname::text,
    relation.relname::text,
    constraint_definition.conname::text
FROM pg_catalog.pg_constraint AS constraint_definition
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = constraint_definition.conrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'index'::text,
    namespace.nspname::text,
    relation.relname::text,
    index_relation.relname::text
FROM pg_catalog.pg_index AS index_definition
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = index_definition.indrelid
JOIN pg_catalog.pg_class AS index_relation
  ON index_relation.oid = index_definition.indexrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname = 'catalog';

COMMENT ON VIEW catalog.deployed_object_inventory IS
    'Named PostgreSQL metadata profile for derived inventory of the catalog schema';
