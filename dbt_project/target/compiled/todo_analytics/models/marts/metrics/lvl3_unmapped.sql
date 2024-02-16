with source as (
    select * from "ticktick_gtd"."main"."lvl1_lvl2_progress"
),

map as (
    select * from "ticktick_gtd"."main"."lvl3_progress"
)

select source.*


from source left join map on source.l_list_name = map.l_list_name
where
    map.l_list_name is null
    and source.l_list_name not like '%------%'