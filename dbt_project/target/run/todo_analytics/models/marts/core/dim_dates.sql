
  
    
    

    create  table
      "ticktick_gtd"."main"."dim_dates__dbt_tmp"
  
    as (
      WITH source AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_dates"
)

SELECT *
FROM
    source
    );
  
  