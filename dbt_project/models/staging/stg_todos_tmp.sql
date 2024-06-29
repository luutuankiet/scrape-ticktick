with source as  (
    select {{coalesce_defaults(ref('init__trans_dtypes__todos'))}}
    from {{ ref('init__trans_dtypes__todos') }}
)
 select * from source