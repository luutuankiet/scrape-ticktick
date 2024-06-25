WITH source AS (
    SELECT
        "date_id" :: TIMESTAMP AS "date_id",
        -- so that the surr func below correcly generates from a timestamp default.
        {{ dbt_utils.star(
            from = ref('date_seed'),
            except = ['date_id']
        ) }}
    FROM
        {{ ref(
            'date_seed'
        ) }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['date_id']) }} AS date_key,*
FROM
    source
