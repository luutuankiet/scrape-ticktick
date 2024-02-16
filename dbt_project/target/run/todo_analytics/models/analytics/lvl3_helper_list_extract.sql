
  
  create view "ticktick_gtd"."main"."lvl3_helper_list_extract__dbt_tmp" as (
    with source as (
    select * from "ticktick_gtd"."main"."lvl1_lvl2_progress"
),

lvl3_goals as (
    select * from "ticktick_gtd"."main"."init_duckdb__lvl3"
)

select
    fld_folder_name,
    l_list_name,
    '' as goal_ids
from source
union all 
(
select 
'goal',
'id',
'' as goal_ids

union all

select *,'' as goal_ids from lvl3_goals)
  );
