with map as (
    select * from {{ ref('list_goal_mapping') }}

),

goals as (
    select * from {{ ref('init_duckdb__lvl3') }}
),
joined AS (
    SELECT
        goals.*,
        map.folder_name,
        map.list_name
    FROM
        goals
    LEFT JOIN map ON ',' || goals.goal_id || ',' LIKE '%,' || map.goal_ids || ',%'
)

SELECT * FROM joined
UNION ALL
SELECT
    goals.*,
    map.folder_name,
    map.list_name
FROM
    map
LEFT JOIN
    goals ON ',' || goals.goal_id || ',' LIKE '%,' || map.goal_ids || ',%'
WHERE
    goals.goal_id IS NULL
