WITH stg_lists AS (
    SELECT *
    FROM
        {{ ref ('stg_lists') }}
)

SELECT *
FROM
    stg_lists
