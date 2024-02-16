WITH folders AS (
    SELECT
        *
    FROM
        {{ source (
            'raw_data',
            'folders_raw'
        ) }}
),
renamed AS (
    SELECT
        id :: text AS folder_id,
        NAME :: text AS folder_name,
    FROM
        folders
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,*
FROM
    renamed
