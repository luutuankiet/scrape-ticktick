WITH blank_to_nulls AS (
    SELECT
        {{setup_nulls(ref('init_todos_tmp'))}}
    FROM
        {{ ref('init_todos_tmp') }}
)

select * from blank_to_nulls