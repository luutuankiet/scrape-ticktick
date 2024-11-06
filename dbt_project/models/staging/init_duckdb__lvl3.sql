WITH source AS (
    SELECT
        ROW_NUMBER() over(
            ORDER BY
                todo_sortorder
        ) AS goal_id,
        todo_title AS goal
    FROM
        {{ ref("fact_todos") }}
    WHERE
        todo_list_name = 'lvl3 - 1 - 2 years goals'
        AND todo_tags = 'default'
)
SELECT
    *
FROM
    source
