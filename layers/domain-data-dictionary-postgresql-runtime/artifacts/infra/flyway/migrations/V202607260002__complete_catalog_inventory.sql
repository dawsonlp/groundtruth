CREATE OR REPLACE VIEW catalog.deployed_object_inventory AS
SELECT
    'schema'::text AS object_kind,
    namespace.nspname::text AS schema_name,
    namespace.nspname::text AS object_name,
    NULL::text AS detail
FROM pg_catalog.pg_namespace AS namespace
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'relation'::text,
    namespace.nspname::text,
    relation.relname::text,
    relation.relkind::text
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
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'type'::text,
    namespace.nspname::text,
    type_definition.typname::text,
    type_definition.typtype::text
FROM pg_catalog.pg_type AS type_definition
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = type_definition.typnamespace
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'function'::text,
    namespace.nspname::text,
    function_definition.proname::text,
    pg_catalog.pg_get_function_identity_arguments(function_definition.oid)::text
FROM pg_catalog.pg_proc AS function_definition
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = function_definition.pronamespace
WHERE namespace.nspname = 'catalog'

UNION ALL

SELECT
    'trigger'::text,
    namespace.nspname::text,
    relation.relname::text,
    trigger_definition.tgname::text
FROM pg_catalog.pg_trigger AS trigger_definition
JOIN pg_catalog.pg_class AS relation
  ON relation.oid = trigger_definition.tgrelid
JOIN pg_catalog.pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname = 'catalog'
  AND NOT trigger_definition.tgisinternal;

COMMENT ON VIEW catalog.deployed_object_inventory IS
    'Named PostgreSQL metadata profile for schema, relation, column, constraint, index, type, function, and trigger inventory';
