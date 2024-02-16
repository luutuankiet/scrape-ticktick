WITH source AS (
    SELECT *
    FROM
        {{ ref('stg_dates') }}
)

SELECT *
FROM
    source
