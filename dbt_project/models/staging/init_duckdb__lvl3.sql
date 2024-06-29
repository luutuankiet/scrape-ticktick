WITH source AS (
    SELECT
        todo_title AS goal_name,
        ROW_NUMBER() over (
            ORDER BY
                todo_title
        ) AS goal_id
    FROM
        {{ ref(
            'stg_todos'
        ) }}
        t
        LEFT JOIN {{ ref(
            'stg_lists'
        ) }}
        l
        ON l.list_key = t.list_key
        LEFT JOIN {{ ref(
            'stg_folders'
        ) }}
        f
        ON f.folder_key = t.folder_key
    WHERE
        f.folder_name = '🛩Horizon of focus'
        AND l.list_name LIKE '%lvl3%'
        AND t.todo_kind = 'TEXT'
)
SELECT
    *
FROM
    source
