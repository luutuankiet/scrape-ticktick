with source as (
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
    {{ref('obt')}}
WHERE
    td_kind = 'TEXT'
    AND ss_desc = 'undone'
    AND (
        fld_folder_name NOT IN (
            '🚀SOMEDAY lists',
            '🛩Horizon of focus',
            '💤on hold lists'
        )
        OR fld_folder_name IS NULL
    )
)

select

cnt_clarifyme::int as cnt_clarifyme,
(cnt_none+cnt_context)::int as cnt_next_action,
cast(
    100 - (cnt_clarifyme* 100 / (cnt_clarifyme + cnt_none + cnt_context)) as decimal(10,2)
    ) as clarification_progress
from source