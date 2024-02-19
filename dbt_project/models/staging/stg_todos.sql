WITH tasks AS (
    SELECT
        *
    FROM
        {{ ref ('init_todos') }}
),
folders AS (
    SELECT
        *
    FROM
        {{ source(
            'raw_data',
            'folders_raw'
        ) }}
),
lists AS (
    SELECT
        *
    FROM
        {{ source(
            'raw_data',
            'lists_raw'
        ) }}
),
renamed AS (
    SELECT
        t.id :: text AS todo_id,
        COALESCE(
            f.name,
            'Default'
        ) :: text AS folder_name,
        COALESCE(
            l.name,
            'Default'
        ) :: text AS list_name,
        status :: INT AS status_id,
        title :: text AS title,
        timeZone :: text AS timezone,
        reminder,
        reminders,
        exDate,
        items,
        progress,
        t.modifiedTime :: TIMESTAMP AS modified_time,
        CASE
            WHEN t.completedTime = 'nan' THEN '1900-01-01T00:00:00'
            ELSE t.completedTime :: TIMESTAMP
        END AS completed_time,
         CASE
            WHEN t.createdTime = 'nan' THEN '1900-01-01T00:00:00'
            ELSE t.createdTime :: TIMESTAMP
        END AS created_time,
        t.etag :: text AS etag,
        t.deleted :: INT AS deleted,
        t.kind :: text AS kind,
        tags :: text AS tags,
        repeatFrom,
        repeatTaskId,
        repeatFlag,
        CASE
            WHEN pinnedTime = 'nan' THEN '1900-01-01T00:00:00'
            ELSE pinnedTime :: TIMESTAMP
        END AS pinned_time,
        CASE
            WHEN startDate = 'nan' THEN '1900-01-01T00:00:00'
            ELSE startDate :: TIMESTAMP
        END AS start_date,
        CASE
            WHEN dueDate = 'nan' THEN '1900-01-01T00:00:00'
            ELSE dueDate :: TIMESTAMP
        END AS due_date,
        deletedTime,
        repeatFirstdate,
        parentId,
        remindTime
    FROM
        tasks t
        LEFT JOIN lists l
        ON t.projectId = l.id
        LEFT JOIN folders f
        ON f.id = l.groupId
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['todo_id']) }} AS todo_key,*
FROM
    renamed
