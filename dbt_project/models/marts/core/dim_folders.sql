WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_folders') }}
),
seeds_nulls AS (
    SELECT
        {{ coalesce_defaults(ref('stg_folders'), seed = True) }}

),
surr_nulls AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['folder_key']) }} AS folder_key,
        {{ dbt_utils.star(
            from = ref('stg_folders'),
            except = ['folder_key']
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
