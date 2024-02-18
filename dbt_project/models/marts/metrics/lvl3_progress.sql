with source as (
    select * from {{ ref('stg_duckdb__lvl3') }}
    where goal_name is not null
),

progress as (
    select * from {{ ref('lvl1_lvl2_progress') }}
)

select
    goal_id,
    goal_name as lvl3_goal,
    cast(avg(done_progress) over (partition by goal_name) as decimal(10,2)) as lvl3_done_progress,
    cast(avg(clarify_progress) over (partition by goal_name) as decimal(10,2)) as lvl3_clarify_progress,
    source.l_list_name,
    progress.done_progress as l_done_progress,
    progress.clarify_progress as l_clarify_progress


from source
left join progress
    on source.l_list_name = progress.l_list_name
order by 1
