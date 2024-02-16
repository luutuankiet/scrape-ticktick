with map as (
    select * from {{ ref('list_goal_mapping') }}

),

goals as (
    select * from {{ ref('init_duckdb__lvl3') }}
),

joined as (

    select
        goals.*,
        map.fld_folder_name,
        map.l_list_name
    from
        map full outer join
        goals on position(',' || goals.goal_id || ',' in ',' || map.goal_ids ||  ',') > 0
        {# to allow for multi link rows  #}
)

select * from joined
