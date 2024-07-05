WITH source AS (
    SELECT
        COALESCE(
            folder_name,
            'Default'
        ) AS folder_name,
        COALESCE(
            list_name,
            'Inbox'
        ) AS list_name,
        datepart(
            'day',
            created
        ) AS DAY,
        datepart(
            'month',
            created
        ) AS MONTH,
        datepart(
            'year',
            created
        ) AS YEAR,
        max_day_created_timestamp,
        COUNT(*) AS cnt
    FROM
        (
            SELECT
                td_created_time :: TIMESTAMP AS created,
                MAX(created) over(
                    PARTITION BY folder_name,
                    list_name,
                    datepart(
                        'day',
                        created
                    ),
                    datepart(
                        'month',
                        created
                    ),
                    datepart(
                        'year',
                        created
                    )
                ) AS max_day_created_timestamp,*
            FROM
                {{ schema }}.obt
        ) A
    GROUP BY
        folder_name,
        list_name,
        datepart(
            'day',
            created
        ),
        datepart(
            'month',
            created
        ),
        datepart(
            'year',
            created
        ),
        max_day_created_timestamp
),
task_level AS (
    SELECT
        folder_name,
        list_name,
        SUM(cnt) :: INT AS tasks_created,
        max_day_created_timestamp,
        DAY,
        MONTH,
        YEAR
    FROM
        source
    GROUP BY
        DAY,
        MONTH,
        YEAR,
        list_name,
        folder_name,
        max_day_created_timestamp
)
SELECT
    t.*,
    o.td_timezone,(
        YEAR || '-' || MONTH || '-' || DAY
    ) :: DATE AS key,(
        YEAR || '-' || MONTH || '-' || DAY
    ) AS day_of_year
FROM
    task_level t
    INNER JOIN (
        SELECT
            td_timezone,
            folder_name,
            list_name,
            td_created_time
        FROM
            {{ schema }}.obt
    ) o
    ON o.td_created_time = t.max_day_created_timestamp
    AND o.folder_name = t.folder_name
    AND o.list_name = t.list_name
