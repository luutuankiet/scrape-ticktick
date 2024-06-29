with source as (
    select * from {{ ref('lvl1_lvl2_progress') }}
),

map as (
    select * from {{ ref('lvl3_progress') }}
)

select source.*


from source left join map on source.list_name = map.list_name
where
    map.list_name is null
    and source.list_name not like '%------%'
