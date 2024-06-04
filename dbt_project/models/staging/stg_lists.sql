WITH lists AS (
    SELECT
        *
    FROM
        {{ source (
            'raw_data',
            'lists_raw'
        ) }}
),
tasks AS (
    SELECT
        *
    FROM
        {{ source(
            "raw_data",
            "tasks_raw"
        ) }}
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
        ) :: TIMESTAMP AS created_time {# created_time::timestamp AS created_time #}
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
                    {# grabs min date from the tasks table to generate lists' created time #}
                    SELECT
                        projectid,
                        MIN(createdTime) AS created_time
                    FROM
                        tasks
                    GROUP BY
                        projectid
                ) AS t
                RIGHT JOIN lists l
                ON l.id = t.projectid
        ) AS p2
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,*
FROM
    renamed
