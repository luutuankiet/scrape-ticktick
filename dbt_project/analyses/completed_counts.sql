WITH source AS (
    SELECT
        COALESCE(
            fld_folder_name,
            'Default'
        ) AS fld_folder_name,
        COALESCE(
            l_list_name,
            'Inbox'
        ) AS l_list_name,
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
                    PARTITION BY fld_folder_name,
                    l_list_name,
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
        fld_folder_name,
        l_list_name,
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
        fld_folder_name,
        l_list_name,
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
        l_list_name,
        fld_folder_name,
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
            fld_folder_name,
            l_list_name,
            td_completed_time
        FROM
            {{ schema }}.obt
    ) o
    ON o.td_completed_time = t.max_day_completed_timestamp
    AND o.fld_folder_name = t.fld_folder_name
    AND o.l_list_name = t.l_list_name
