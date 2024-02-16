WITH stg_folders AS (
    SELECT *
    FROM
        {{ ref('stg_pg__folders') }}
)

SELECT *
FROM
    stg_folders
