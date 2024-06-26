-- pool
WITH pool AS (
    SELECT
        *,
        CASE
            WHEN todo_tags LIKE '%clarifyme%' THEN 'not_clarified'
            WHEN todo_tags NOT LIKE '%clarifyme%' THEN 'clarified'
        END AS progress_type
    FROM
        {{ ref('obt') }}
    WHERE
        --status_desc ='undone'
        todo_tags NOT LIKE '%someday%'
        AND todo_tags NOT LIKE '%waiting_for%'
        AND todo_tags NOT LIKE '%tickler%'
        AND todo_kind = 'TEXT'
        AND list_isactive = TRUE
        AND folder_name NOT IN (
            '🚀SOMEDAY lists',
            '🛩Horizon of focus'
        )
        AND list_name NOT IN ('🧳SOMEDAY')
),
done_progress AS (
    SELECT
        folder_name,
        list_name,
        SUM(
            CASE
                WHEN status_desc = 'done' THEN 1
                ELSE 0
            END
        ) AS cnt_done,
        (
            SUM(
                CASE
                    WHEN status_desc = 'undone' THEN 1
                    ELSE 0
                END
            )
        ) AS cnt_not_done,
        (
            SUM(
                CASE
                    WHEN status_desc = 'done' THEN 1
                    ELSE 0
                END
            ) * 100.0 / (
                COALESCE(
                    NULLIF(
                        (
                            SUM(
                                CASE
                                    WHEN status_desc = 'done' THEN 1
                                    ELSE 0
                                END
                            ) + SUM(
                                CASE
                                    WHEN status_desc = 'undone' THEN 1
                                    ELSE 0
                                END
                            )
                        ),
                        0
                    ),
                    1
                )
            )
        ) AS done_progress
    FROM
        pool
    GROUP BY
        folder_name,
        list_name
),
clarify_progress AS (
    SELECT
        folder_name,
        list_name,
        SUM(
            CASE
                WHEN progress_type = 'clarified'
                AND status_desc = 'undone' THEN 1
                ELSE 0
            END
        ) AS cnt_clarified,
        SUM(
            CASE
                WHEN progress_type = 'not_clarified'
                AND status_desc = 'undone' THEN 1
                ELSE 0
            END
        ) AS cnt_not_clarified,
        COALESCE(
            (
                SUM(
                    CASE
                        WHEN progress_type = 'clarified'
                        AND status_desc = 'undone' THEN 1
                        ELSE 0
                    END
                ) * 100.0 / (
                    COALESCE(
                        NULLIF(
                            (
                                SUM(
                                    CASE
                                        WHEN progress_type = 'clarified'
                                        AND status_desc = 'undone' THEN 1
                                        ELSE 0
                                    END
                                ) + SUM(
                                    CASE
                                        WHEN progress_type = 'not_clarified'
                                        AND status_desc = 'undone' THEN 1
                                        ELSE 0
                                    END
                                )
                            ),
                            0
                        ),
                        1
                    )
                )
            ),
            100
        ) AS clarify_progress
    FROM
        pool
    GROUP BY
        folder_name,
        list_name
),
    lists_progress AS (
        SELECT
            clarify_progress.folder_name,
            clarify_progress.list_name,
            cnt_done,
            cnt_not_done,
            done_progress.done_progress,
            cnt_clarified,
            cnt_not_clarified,
            clarify_progress
        FROM
            done_progress
            INNER JOIN clarify_progress
            ON done_progress.list_name = clarify_progress.list_name
            AND done_progress.folder_name = clarify_progress.folder_name
    ),
    folder_progress AS (
        -- aggregate folder progresss
        SELECT
            folder_name,
            '-----------------------' AS list_name,
            100 AS cnt_done,
            100 AS cnt_not_done,
            folder_progress.folder_progress AS done_progress,
            100 AS cnt_clarified,
            100 AS cnt_not_clarified,
            list_progress AS clarify_progress
        FROM
            (
                SELECT
                    folder_name,
                    AVG(done_progress) AS folder_progress,
                    AVG(clarify_progress) AS list_progress
                FROM
                    lists_progress
                GROUP BY
                    folder_name
            ) AS folder_progress
        UNION ALL
        SELECT
            *
        FROM
            lists_progress
    ),
    staging AS (
        SELECT
            COALESCE(
                folder_name,
                'Default'
            ) AS folder_name,
            COALESCE(
                list_name,
                'Inbox'
            ) AS list_name,
            done_progress :: DECIMAL(
                10,
                2
            ) AS done_progress,
            clarify_progress :: DECIMAL(
                10,
                2
            ) AS clarify_progress
        FROM
            folder_progress
    )
SELECT
    *
FROM
    staging
ORDER BY
    1,
    2,
    3,
    4
