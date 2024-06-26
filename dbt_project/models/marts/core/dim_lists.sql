WITH source AS (
    SELECT
        *
    FROM
        {{ ref ('stg_lists') }}
),
seeds_nulls AS (
    SELECT
        {{ coalesce_defaults(ref('stg_lists'), seed = True) }}),
surr_nulls AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['list_key']) }} AS list_key,
        {{ dbt_utils.star(
            from = ref('stg_lists'),
            except = ['list_key']
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
