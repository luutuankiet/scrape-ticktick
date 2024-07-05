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
            active
        ) AS DAY,
        datepart(
            'month',
            active
        ) AS MONTH,
        datepart(
            'year',
            active
        ) AS YEAR,
        max_day_active_timestamp,
        COUNT(*) AS cnt
    FROM
        (
            SELECT
                td_modified_time :: TIMESTAMP AS active,
                MAX(active) over(
                    PARTITION BY folder_name,
                    list_name,
                    datepart(
                        'day',
                        active
                    ),
                    datepart(
                        'month',
                        active
                    ),
                    datepart(
                        'year',
                        active
                    )
                ) AS max_day_active_timestamp,*
            FROM
                {{ schema }}.obt
        ) A
    GROUP BY
        folder_name,
        list_name,
        datepart(
            'day',
            active
        ),
        datepart(
            'month',
            active
        ),
        datepart(
            'year',
            active
        ),
        max_day_active_timestamp
),
task_level AS (
    SELECT
        folder_name,
        list_name,
        SUM(cnt) :: INT AS tasks_active,
        max_day_active_timestamp,
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
        max_day_active_timestamp
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
            td_modified_time
        FROM
            {{ schema }}.obt
    ) o
    ON o.td_modified_time = t.max_day_active_timestamp
    AND o.folder_name = t.folder_name
    AND o.list_name = t.list_name
