WITH stg_lists AS (
    SELECT *
    FROM
        {{ ref ('stg_pg__lists') }}
)

SELECT *
FROM
    stg_lists
