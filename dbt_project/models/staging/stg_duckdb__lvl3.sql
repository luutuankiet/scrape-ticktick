WITH MAP AS (
    SELECT
        *,
        unnest(
            regexp_split_to_array(
                goals,
                ',(?=(?:[^"]*"[^"]*")*[^"]*$)'
            )
        ) AS goal
    FROM
        {{ ref('list_goal_mapping') }}
),
goals AS (
    SELECT
        *
    FROM
        {{ ref('init_duckdb__lvl3') }}
),
unmapped AS (
    SELECT
        *
    FROM
        {{ ref("list_goal_mapping") }}
    WHERE
        goals IS NULL
),
joined AS (
    SELECT
        goals.*,
        MAP.folder_name,
        MAP.list_name
    FROM
        goals
        LEFT JOIN MAP {# ON goals.goal like '%' || MAP.goal || '%' #}
        ON TRIM(goals.goal) LIKE '%' || REPLACE(TRIM(MAP.goal), '"', '') || '%'
    UNION ALL
    SELECT
        NULL AS goal_name,
        NULL AS goal_id,
        folder_name,
        list_name
    FROM
        unmapped
)
SELECT
    *
FROM
    joined
ORDER BY
    folder_name,
    list_name
