WITH todos AS (
    SELECT *
    FROM
        {{ ref ('stg_todos') }}
),

lists AS (
    SELECT *
    FROM
        {{ ref ('stg_lists') }}
),

folders AS (
    SELECT *
    FROM
        {{ ref('stg_folders') }}
),

statuses AS (
    SELECT *
    FROM
        {{ ref('stg_statuses') }}
),

dates AS (
    SELECT *
    FROM
        {{ ref('stg_dates') }}
),

facts_todo AS (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['l.list_id']) }} AS list_key,
        {{ dbt_utils.generate_surrogate_key(['fld.folder_id']) }} AS folder_key,
        {{ dbt_utils.generate_surrogate_key(['ss.status_id']) }} AS status_key,
        {{ dbt_utils.generate_surrogate_key(['dds.date_id']) }} AS date_start_key,
        {{ dbt_utils.generate_surrogate_key(['ddd.date_id']) }} AS date_due_key,
        {{ dbt_utils.generate_surrogate_key(['ddcm.date_id']) }} AS date_completed_key,
        {{ dbt_utils.generate_surrogate_key(['ddc.date_id']) }} AS date_created_key,
        td.*
{#         
        
        title,
        kind,
        tags,
        reminder,
        repeat_,
        priority,
        timezone,
        isallday,
        isfloating #}
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
