with source as (
    select * from {{ ref('lvl1_lvl2_progress') }}
),

lvl3_goals as (
    select * from {{ ref('init_duckdb__lvl3') }}
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
