WITH lists AS (
    SELECT
        *
    FROM
        "ticktick_gtd"."main"."lists_raw"
),
tasks AS (
    SELECT
        *
    FROM
        "ticktick_gtd"."main"."tasks_raw"
),
renamed AS (
    SELECT
        DISTINCT id AS list_id,
        NAME :: text AS list_name,
        modifiedTime :: TIMESTAMP AS modified_time,
        groupId :: text AS folder_id,
        kind :: text AS lkind,
        isactive :: BOOLEAN AS is_active,
        COALESCE(
            created_time,
            '1900-01-01T00:00:00'
        ) :: TIMESTAMP AS created_time 
    FROM
        (
            SELECT
                CASE
                    WHEN closed = 'True' THEN 0
                    ELSE 1
                END AS isactive,
                created_time,
                l.*
            FROM
                (
                    
                    SELECT
                        "projectId",
                        MIN("createdTime") AS created_time
                    FROM
                        tasks
                    GROUP BY
                        "projectId"
                ) AS t
                RIGHT JOIN lists l
                ON l.id = t.projectId
        ) AS p2
)
SELECT
    md5(cast(coalesce(cast(list_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS list_key,*
FROM
    renamed