WITH source AS (
    SELECT
        SUM(
            CASE
                WHEN td_tags LIKE '%clarifyme%' THEN 1
                ELSE 0
            END
        ) AS cnt_clarifyme,
        SUM(
            CASE
                WHEN td_tags = '[]' THEN 1
                ELSE 0
            END
        ) AS cnt_none,
        SUM(
            CASE
                WHEN td_tags LIKE '%@%' THEN 1
                ELSE 0
            END
        ) AS cnt_context,
        SUM(
            CASE
                WHEN td_tags LIKE '%someday%' THEN 1
                ELSE 0
            END
        ) AS cnt_someday,
        SUM(
            CASE
                WHEN td_tags LIKE '%waiting_for%' THEN 1
                ELSE 0
            END
        ) AS cnt_waiting_for
    FROM
        {{ schema }}.obt {# {{ref('obt')}} #}
    WHERE
        td_kind = 'TEXT'
        AND ss_desc = 'undone'
        AND (
            folder_name NOT IN (
                '🚀SOMEDAY lists',
                '🛩Horizon of focus',
                '💤on hold lists'
            )
            OR folder_name IS NULL
        )
)
SELECT
    cnt_clarifyme :: INT AS cnt_clarifyme,
    (
        cnt_none + cnt_context
    ) :: INT AS cnt_next_action,
    CAST(
        100 - (
            cnt_clarifyme * 100 / (
                cnt_clarifyme + cnt_none + cnt_context
            )
        ) AS DECIMAL(
            10,
            2
        )
    ) AS clarification_progress
FROM
    source
