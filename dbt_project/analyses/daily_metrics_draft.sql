SELECT
    due_date_id,
    folder_name,
    list_name,
    td_title,* {# COUNT(*) AS cnt #}
FROM
    (
        SELECT
            *
        FROM
            {{ schema }}.obt
        WHERE
            completed_date_id IS NULL
            AND l_is_active = '1'
            AND td_kind = 'TEXT'
            AND folder_name NOT IN (
                '🚀SOMEDAY lists',
                '🛩Horizon of focus',
                '💤on hold lists'
            )
            AND list_name NOT LIKE '%tickler note%'
    ) NEW
WHERE
    due_date_id IS NOT NULL {# GROUP BY
    due_date_id #}
ORDER BY
    1,
    2,
    3
