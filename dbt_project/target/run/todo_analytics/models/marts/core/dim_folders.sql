
  
    
    

    create  table
      "ticktick_gtd"."main"."dim_folders__dbt_tmp"
  
    as (
      WITH stg_folders AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_folders"
)

SELECT *
FROM
    stg_folders
    );
  
  