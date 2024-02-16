WITH todos AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_todos"
),

lists AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_lists"
),

folders AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_folders"
),

statuses AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_statuses"
),

dates AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."stg_dates"
),

facts_todo AS (
    SELECT
        td.todo_id,
        md5(cast(coalesce(cast(td.todo_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS todo_key,
        md5(cast(coalesce(cast(l.list_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS list_key,
        md5(cast(coalesce(cast(fld.folder_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS folder_key,
        md5(cast(coalesce(cast(ss.status_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS status_key,
        md5(cast(coalesce(cast(dds.date_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS date_start_key,
        md5(cast(coalesce(cast(ddd.date_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS date_due_key,
        md5(cast(coalesce(cast(ddcm.date_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS date_completed_key,
        md5(cast(coalesce(cast(ddc.date_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) AS date_created_key,
        td.*

    FROM
        todos AS td
    LEFT JOIN -- folder
        folders AS fld
        ON td.folder_name = fld.folder_name
    LEFT JOIN -- list
        lists AS l
        ON td.list_name = l.list_name
    LEFT JOIN -- status
        statuses AS ss
        ON cast(ss.status_id AS text) = cast(td.status_id AS text) -- role play dates for start, due, create, complete
    LEFT JOIN dates AS dds
        ON cast(dds.date_id AS date) = cast(td.start_date AS date)
    LEFT JOIN dates AS ddd
        ON cast(ddd.date_id AS date) = cast(td.due_date AS date)
    LEFT JOIN dates AS ddc
        ON cast(ddc.date_id AS date) = cast(td.created_time AS date)
    LEFT JOIN dates AS ddcm
        ON cast(ddcm.date_id AS date) = cast(td.completed_time AS date)
)

SELECT *
FROM
    facts_todo