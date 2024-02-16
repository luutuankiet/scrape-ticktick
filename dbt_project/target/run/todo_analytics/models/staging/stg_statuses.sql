
  
  create view "ticktick_gtd"."main"."stg_statuses__dbt_tmp" as (
    WITH source AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."tasks_raw"
)
,
renamed AS (
    SELECT DISTINCT
        CAST(
            status AS INT
        ) AS status_id,
        CASE
            WHEN status = '-1' THEN 'wont do'
            WHEN status = '2' THEN 'done'
            WHEN status = '0' THEN 'undone'
        END AS "desc",
        CASE
            WHEN status = '-1' THEN 'regardless of archival'
            WHEN status = '2' THEN 'regardless of archival'
            WHEN status = '0' THEN 'regardless of archival'
        END AS status_comments
    FROM
        source
)

SELECT
    md5(cast(coalesce(cast(status_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS status_key,
    *
FROM
    renamed
  );
