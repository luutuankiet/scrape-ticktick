
  
    
    

    create  table
      "ticktick_gtd"."main"."dim_statuses__dbt_tmp"
  
    as (
      WITH stg_statuses AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_statuses"
)

SELECT *
FROM
    stg_statuses
    );
  
  