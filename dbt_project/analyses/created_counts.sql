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
                    PARTITION BY fld_folder_name,
                    l_list_name,
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
        fld_folder_name,
        l_list_name,
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
        fld_folder_name,
        l_list_name,
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
        l_list_name,
        fld_folder_name,
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
            fld_folder_name,
            l_list_name,
            td_created_time
        FROM
            {{ schema }}.obt
    ) o
    ON o.td_created_time = t.max_day_created_timestamp
    AND o.fld_folder_name = t.fld_folder_name
    AND o.l_list_name = t.l_list_name
