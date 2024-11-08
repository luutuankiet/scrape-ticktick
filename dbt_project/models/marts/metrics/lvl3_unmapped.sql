WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_duckdb__lvl3') }}
)
SELECT
    *
FROM
    source
WHERE
    goal_id IS NULL
    AND list_name NOT LIKE '%-%'
