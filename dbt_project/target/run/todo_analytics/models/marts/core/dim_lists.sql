
  
    
    

    create  table
      "ticktick_gtd"."main"."dim_lists__dbt_tmp"
  
    as (
      WITH stg_lists AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_lists"
)

SELECT *
FROM
    stg_lists
    );
  
  