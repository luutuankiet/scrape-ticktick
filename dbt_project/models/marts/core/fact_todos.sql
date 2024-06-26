WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_todos') }}
)
SELECT
    {{ coalesce_defaults(ref('stg_todos'), seed = True) }}
FROM
    source
UNION ALL
SELECT
    *
FROM
    source
