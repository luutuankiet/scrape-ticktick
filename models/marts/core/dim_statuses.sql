WITH stg_statuses AS (
    SELECT *
    FROM
        {{ ref('stg_pg__statuses') }}
)

SELECT *
FROM
    stg_statuses
