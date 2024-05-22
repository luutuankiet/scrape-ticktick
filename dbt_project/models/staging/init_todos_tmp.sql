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
base AS (
    SELECT
        t.id ,
        f.name ,
        l.name ,
        t.status ,
        title ,
        timeZone ,
        reminder ,
        reminders ,
        exDate ,
        items ,
        progress ,
        t.modifiedTime ,
        t.completedTime ,
        t.createdTime ,
        t.etag ,
        t.deleted ,
        t.kind ,
        tags ,
        repeatFrom,
        repeatTaskId,
        repeatFlag,
        pinnedTime ,
        startDate ,
        dueDate ,
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
    *
FROM
    base
