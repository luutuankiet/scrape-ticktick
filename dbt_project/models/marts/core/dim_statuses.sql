WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_statuses') }}
),

seeds_nulls AS (
    SELECT
        {{ coalesce_defaults(ref('stg_statuses'), seed = True) }}

),
surr_nulls AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['status_key']) }} AS status_key,
        {{ dbt_utils.star(
            from = ref('stg_statuses'),
            except = ['status_key']
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
