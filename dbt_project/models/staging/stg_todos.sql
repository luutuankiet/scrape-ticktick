WITH todo AS (
    SELECT
        {{ coalesce_defaults(ref('src__tasks_raw')) }}
    FROM
        {{ ref('src__tasks_raw') }}
),
lists AS (
    SELECT
        {{ coalesce_defaults(ref('src__lists_raw')) }}
    FROM
        {{ ref('src__lists_raw') }}
),
folders AS (
    SELECT
        {{ coalesce_defaults(ref('src__folders_raw')) }}
    FROM
        {{ ref('src__folders_raw') }}
),
statuses AS (
    SELECT
        *
    FROM
        {{ ref('stg_statuses') }}
),
dates AS (
    SELECT
        *
    FROM
        {{ ref('stg_dates') }}
),
joined AS (
    SELECT
        {# gotta handle the NULLs from this join; they are hashed. next up is to generate that hashed null in other tables #}
        {{ dbt_utils.generate_surrogate_key(['dds.date_id']) }} AS date_start_key,
        {{ dbt_utils.generate_surrogate_key(['ddd.date_id']) }} AS date_due_key,
        {{ dbt_utils.generate_surrogate_key(['ddcm.date_id']) }} AS date_completed_key,
        {{ dbt_utils.generate_surrogate_key(['ddc.date_id']) }} AS date_created_key,
        {{ dbt_utils.generate_surrogate_key(['todo_id']) }} AS todo_key,
        {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,
        {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,
        {{ dbt_utils.generate_surrogate_key(['status_id']) }} AS status_key,
        t.*,
        COALESCE(
            l.list_id,
            'default'
        ) AS list_id,
        COALESCE(
            f.folder_id,
            'default'
        ) AS folder_id,
        COALESCE(
            ss.status_id,
            'default'
        ) AS status_id
    FROM
        todo t
        LEFT JOIN lists l
        ON t.todo_projectid = l.list_id
        LEFT JOIN folders f
        ON l.list_groupid = f.folder_id
        LEFT JOIN statuses ss
        ON ss.status_id = t.todo_status
        LEFT JOIN dates dds
        ON dds.date_id = t.todo_startdate_derived_date
        LEFT JOIN dates ddd
        ON ddd.date_id = t.todo_duedate_derived_date
        LEFT JOIN dates ddc
        ON ddc.date_id = t.todo_createdtime_derived_date
        LEFT JOIN dates ddcm
        ON ddcm.date_id = t.todo_completedtime_derived_date
)
SELECT
    *
FROM
    joined
