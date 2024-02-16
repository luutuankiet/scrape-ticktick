WITH stg_statuses AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_statuses"
)

SELECT *
FROM
    stg_statuses