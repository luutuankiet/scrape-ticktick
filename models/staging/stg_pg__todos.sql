WITH source AS (
    SELECT *
    FROM
        {{ source (
            'raw_data',
            'raw_data'
        ) }}
),

stg_fact_todo AS (
    SELECT
        taskid::INT AS todo_id,
        COALESCE(
            "Folder Name",
            'Default'
        )::TEXT AS folder_name,
        COALESCE(
            "List Name",
            'Default'
        )::TEXT AS list_name,
        status::INT AS status_id,
        -- sl.list_id::int as list_id,
        -- fld.folder_id::int as folder_id,
        -- ss.status_id::int as status_id,
        -- dd.date_id::text as date_id,
        COALESCE(
            "Start Date",
            '1900-01-01'
        )::TIMESTAMP AS start_date,
        COALESCE(
            "Due Date",
            '1900-01-01'
        )::TIMESTAMP AS due_date,
        priority::INT AS priority,
        "Created Time"::TIMESTAMP AS created_time,
        COALESCE(
            "Completed Time",
            '1900-01-01'
        )::TIMESTAMP AS completed_time,
        COALESCE(
            timezone,
            'Default'
        )::TEXT AS timezone,
        COALESCE(
            "Is All Day",
            'Default'
        )::TEXT AS isallday,
        COALESCE(
            "Is Floating",
            'Default'
        )::TEXT AS isfloating,
        COALESCE(
            title,
            'Default'
        ) AS title,
        COALESCE(
            kind,
            'Default'
        ) AS kind,
        COALESCE(
            tags,
            'Default'
        ) AS tags,
        COALESCE(
            reminder,
            'Default'
        ) AS reminder,
        COALESCE(
            repeat,
            'Default'
        ) AS repeat_
    FROM
        source
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['todo_id']) }} AS todo_key,
    *
FROM
    stg_fact_todo
