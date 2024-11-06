WITH source AS (
    SELECT
        *
    FROM
        {{ ref('stg_duckdb__lvl3') }}
    WHERE
        goal IS NOT NULL
),
progress AS (
    SELECT
        *
    FROM
        {{ ref('lvl1_lvl2_progress') }}
)
SELECT
    goal_id,
    goal AS lvl3_goal,
    CAST(AVG(done_progress) over (PARTITION BY goal) AS DECIMAL(10, 2)) AS lvl3_done_progress,
    CAST(AVG(clarify_progress) over (PARTITION BY goal) AS DECIMAL(10, 2)) AS lvl3_clarify_progress,
    source.list_name,
    progress.done_progress AS l_done_progress,
    progress.clarify_progress AS l_clarify_progress
FROM
    source
    LEFT JOIN progress
    ON source.list_name = progress.list_name
ORDER BY
    1
