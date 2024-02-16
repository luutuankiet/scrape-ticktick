WITH source AS (
    SELECT *
    FROM
        {{ source (
            'raw_data',
            'raw_data'
        ) }}
),

stg_folders AS (
    SELECT DISTINCT
        s2.rn AS folder_id,
        s1."Folder Name" AS folder_name
    FROM
        source AS s1
    INNER JOIN (
        SELECT
            "Folder Name",
            ROW_NUMBER() OVER (
                ORDER BY
                    "Folder Name"
            ) AS rn
        FROM
            source
        GROUP BY
            "Folder Name"
    ) AS s2
        ON s1."Folder Name" = s2."Folder Name"
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,
    *
FROM
    stg_folders
