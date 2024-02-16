WITH folders AS (
    SELECT
        *
    FROM
        "ticktick_gtd"."main"."folders_raw"
),
renamed AS (
    SELECT
        id :: text AS folder_id,
        NAME :: text AS folder_name,
    FROM
        folders
)
SELECT
    md5(cast(coalesce(cast(folder_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS folder_key,*
FROM
    renamed