with source as (
    select
        title as goal_name,
        ROW_NUMBER() over (order by title) as goal_id

    from
        {{ source('raw_data', 'raw_data') }} where "Folder Name" = '🛩Horizon of focus'

    and "List Name" like '%lvl3%'
    and kind = 'TEXT'


)

select *
from source
