-- pool
WITH pool AS (
    SELECT
        *,
        CASE
            WHEN td_tags LIKE '%clarifyme%' THEN 'not_clarified'
            WHEN td_tags NOT LIKE '%clarifyme%' THEN 'clarified'
        END AS progress_type
    FROM
        {{ ref('obt') }}
    WHERE
        --ss_desc ='undone'
        td_tags NOT LIKE '%someday%'
        AND td_tags NOT LIKE '%waiting_for%'
        AND td_tags NOT LIKE '%tickler%'
        AND td_kind = 'TEXT'
        AND l_is_active = TRUE
        AND fld_folder_name NOT IN (
            '🚀SOMEDAY lists',
            '🛩Horizon of focus'
        )
        AND l_list_name NOT IN ('🧳SOMEDAY')
),

done_progress AS (
    SELECT
        fld_folder_name,
        l_list_name,
        SUM(
            CASE
                WHEN ss_desc = 'done' THEN 1
                ELSE 0
            END
        ) AS cnt_done,
        SUM(
            CASE
                WHEN ss_desc = 'undone' THEN 1
                ELSE 0
            END
        ) AS cnt_not_done,
        SUM(
            CASE
                WHEN ss_desc = 'done' THEN 1
                ELSE 0
            END
        ) * 100.0 / (
            SUM(
                CASE
                    WHEN ss_desc = 'done' THEN 1
                    ELSE 0
                END
            ) + SUM(
                CASE
                    WHEN ss_desc = 'undone' THEN 1
                    ELSE 0
                END
            )
        ) AS done_progress
    FROM
        pool
    GROUP BY
        fld_folder_name,
        l_list_name
),

clarify_progress AS (
    SELECT
        fld_folder_name,
        l_list_name,
        SUM(
            CASE
                WHEN
                    progress_type = 'clarified'
                    AND ss_desc = 'undone' THEN 1
                ELSE 0
            END
        ) AS cnt_clarified,
        SUM(
            CASE
                WHEN
                    progress_type = 'not_clarified'
                    AND ss_desc = 'undone' THEN 1
                ELSE 0
            END
        ) AS cnt_not_clarified,
        COALESCE(
            (
                SUM(
                    CASE
                        WHEN
                            progress_type = 'clarified'
                            AND ss_desc = 'undone' THEN 1
                        ELSE 0
                    END
                ) * 100.0 / (
                    SUM(
                        CASE
                            WHEN
                                progress_type = 'clarified'
                                AND ss_desc = 'undone' THEN 1
                            ELSE 0
                        END
                    ) + SUM(
                        CASE
                            WHEN
                                progress_type = 'not_clarified'
                                AND ss_desc = 'undone' THEN 1
                            ELSE 0
                        END
                    )
                )
            ),
            100.0
        ) AS clarify_progress
    FROM
        pool
    GROUP BY
        fld_folder_name,
        l_list_name
),

lists_progress AS (
    SELECT
        clarify_progress.fld_folder_name,
        clarify_progress.l_list_name,
        cnt_done,
        cnt_not_done,
        done_progress.done_progress,
        cnt_clarified,
        cnt_not_clarified,
        clarify_progress
    FROM
        done_progress
    INNER JOIN clarify_progress
        ON
            done_progress.l_list_name = clarify_progress.l_list_name
            AND done_progress.fld_folder_name = clarify_progress.fld_folder_name
),

folder_progress AS (
    -- aggregate folder progresss
    SELECT
        fld_folder_name,
        '-----------------------' AS l_list_name,
        100 AS cnt_done,
        100 AS cnt_not_done,
        folder_progress.folder_progress AS done_progress,
        100 AS cnt_clarified,
        100 AS cnt_not_clarified,
        list_progress AS clarify_progress
    FROM
        (
            SELECT
                fld_folder_name,
                AVG(done_progress) AS folder_progress,
                AVG(clarify_progress) AS list_progress
            FROM
                lists_progress
            GROUP BY
                fld_folder_name
        ) AS folder_progress
    UNION ALL
    SELECT *
    FROM
        lists_progress
),

staging AS (
    SELECT
        fld_folder_name,
        l_list_name,
        done_progress::decimal(10,2) as done_progress,
        clarify_progress::decimal(10,2) as clarify_progress


    FROM folder_progress
)

SELECT *
FROM
    staging
ORDER BY 1, 2, 3, 4
