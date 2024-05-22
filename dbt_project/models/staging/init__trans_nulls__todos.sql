WITH blank_to_nulls AS (
    SELECT
        {{convert_blank_to_null(ref('init_todos_tmp'))}}
    FROM
        {{ ref('init_todos_tmp') }}
)

select * from blank_to_nulls