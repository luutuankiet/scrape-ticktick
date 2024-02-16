WITH source AS (
    SELECT
        title AS goal_name,
        ROW_NUMBER() over (
            ORDER BY
                title
        ) AS goal_id
    FROM
        "ticktick_gtd"."main"."tasks_raw"
        t
        LEFT JOIN "ticktick_gtd"."main"."lists_raw"
        l
        ON l.id = t.projectId
        LEFT JOIN "ticktick_gtd"."main"."folders_raw"
        f
        ON f.id = l.groupId
    WHERE
        f.name = '🛩Horizon of focus'
        AND l.name LIKE '%lvl3%'
        AND t.kind = 'TEXT'
)
SELECT
    *
FROM
    source