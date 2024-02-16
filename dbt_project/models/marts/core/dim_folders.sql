WITH stg_folders AS (
    SELECT *
    FROM
        {{ ref('stg_folders') }}
)

SELECT *
FROM
    stg_folders
