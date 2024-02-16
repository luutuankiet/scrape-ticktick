WITH stg_statuses AS (
    SELECT *
    FROM
        {{ ref('stg_statuses') }}
)

SELECT *
FROM
    stg_statuses
