with source as (select * from {{ref('stg_todos')}})
select * from source 