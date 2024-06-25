WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_dates') }}
),
seeds_nulls AS (
    SELECT
        {{ coalesce_defaults(ref('stg_dates'), seed = True) }}

),
surr_nulls AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['date_key']) }} AS date_key,
        {{ dbt_utils.star(
            from = ref('stg_dates'),
            except = ['date_key']
        ) }}
    FROM
        seeds_nulls
)
SELECT
    *
FROM
    surr_nulls
UNION ALL
SELECT
    *
FROM
    source
