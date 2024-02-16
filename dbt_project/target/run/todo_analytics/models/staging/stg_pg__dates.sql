
  
  create view "ticktick_gtd"."main"."stg_pg__dates__dbt_tmp" as (
    WITH source AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."date_seed"
)

SELECT
    md5(cast(coalesce(cast(date_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS date_key,
    *
FROM
    source
  );
