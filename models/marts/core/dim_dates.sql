WITH source AS (
    SELECT *
    FROM
        {{ ref('stg_pg__dates') }}
)

SELECT *
FROM
    source
