SELECT
    due_date_id,
    
    fld_folder_name,
    l_list_name,
    td_title

    ,*
    {# COUNT(*) AS cnt #}
FROM
    (
        SELECT
            *
        FROM
            obt
        WHERE
            completed_date_id IS NULL
            AND l_is_active = '1'
            AND td_kind = 'TEXT'
            AND fld_folder_name NOT IN (
                '🚀SOMEDAY lists',
                '🛩Horizon of focus',
                '💤on hold lists'
            )
            AND l_list_name NOT LIKE '%tickler note%'
    ) NEW
WHERE
    due_date_id IS NOT NULL
{# GROUP BY
    due_date_id #}
    order by 1,2,3