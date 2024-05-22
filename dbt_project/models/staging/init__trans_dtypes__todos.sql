with source as (
    select * from {{ ref('init_trans_nulls__todos') }}
),
dtypes as (
    select 
)
