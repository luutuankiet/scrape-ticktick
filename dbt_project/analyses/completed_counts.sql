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
            completed
        ) AS DAY,
        datepart(
            'month',
            completed
        ) AS MONTH,
        datepart(
            'year',
            completed
        ) AS YEAR,
        max_day_completed_timestamp,
        COUNT(*) AS cnt
    FROM
        (
            SELECT
                td_completed_time :: TIMESTAMP AS completed,
                MAX(completed) over(
                    PARTITION BY folder_name,
                    list_name,
                    datepart(
                        'day',
                        completed
                    ),
                    datepart(
                        'month',
                        completed
                    ),
                    datepart(
                        'year',
                        completed
                    )
                ) AS max_day_completed_timestamp,*
            FROM
                {{ schema }}.obt
        ) A
    GROUP BY
        folder_name,
        list_name,
        datepart(
            'day',
            completed
        ),
        datepart(
            'month',
            completed
        ),
        datepart(
            'year',
            completed
        ),
        max_day_completed_timestamp
),
task_level AS (
    SELECT
        folder_name,
        list_name,
        SUM(cnt) :: INT AS tasks_completed,
        max_day_completed_timestamp,
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
        max_day_completed_timestamp
)
SELECT
    t.*,
    td_timezone,(
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
            td_completed_time
        FROM
            {{ schema }}.obt
    ) o
    ON o.td_completed_time = t.max_day_completed_timestamp
    AND o.folder_name = t.folder_name
    AND o.list_name = t.list_name
