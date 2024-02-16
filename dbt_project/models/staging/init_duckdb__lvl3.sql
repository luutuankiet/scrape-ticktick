WITH source AS (
    SELECT
        title AS goal_name,
        ROW_NUMBER() over (
            ORDER BY
                title
        ) AS goal_id
    FROM
        {{ source(
            'raw_data',
            'tasks_raw'
        ) }}
        t
        LEFT JOIN {{ source(
            'raw_data',
            'lists_raw'
        ) }}
        l
        ON l.id = t.projectId
        LEFT JOIN {{ source(
            'raw_data',
            'folders_raw'
        ) }}
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
