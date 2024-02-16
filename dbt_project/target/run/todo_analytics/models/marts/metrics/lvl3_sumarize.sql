
  
    
    

    create  table
      "ticktick_gtd"."main"."lvl3_sumarize__dbt_tmp"
  
    as (
      select distinct
    goal_id,
    lvl3_goal,
    lvl3_done_progress
from "ticktick_gtd"."main"."lvl3_progress"
order by 1
    );
  
  