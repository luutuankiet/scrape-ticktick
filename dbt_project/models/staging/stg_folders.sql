WITH source AS (
    SELECT
         {{coalesce_defaults(ref(
            'src__folders_raw'
        ) )}}
    FROM
        {{ ref(
            'src__folders_raw'
        ) }}
)
 
SELECT
    {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,*
FROM
    source
