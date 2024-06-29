WITH source AS (
    SELECT
        *
    FROM
        {{ ref(
            'date_seed'
        ) }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['date_id']) }} AS date_key,*
FROM
    source
