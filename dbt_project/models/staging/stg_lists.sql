WITH lists AS (
    SELECT
        {{ coalesce_defaults(ref('src__lists_raw')) }}
    FROM
        {{ ref(
            'src__lists_raw'
        ) }}
),
todo AS (
    SELECT
        {{ coalesce_defaults(ref('src__tasks_raw')) }}
    FROM
        {{ ref(
            "src__tasks_raw"
        ) }}
),
list_created AS (
    SELECT
        todo_projectid,
        MIN(todo_createdTime) AS list_created_time
    FROM
        todo
    GROUP BY
        todo_projectid
),
list_isActive AS (
    SELECT
        CASE
            WHEN list_closed = 'True' THEN 0
            ELSE 1
        END AS list_isActive,
        list_id
    FROM
        lists
),
joined AS (
    SELECT
        l.*,
        COALESCE(
            t.list_created_time,
            '1900-01-01T00:00:00'
        ) :: TIMESTAMP AS list_created_time,
        list_isActive :: BOOLEAN AS list_isActive
    FROM
        lists l
        INNER JOIN list_created t
        ON l.list_id = t.todo_projectid
        INNER JOIN list_isActive i
        ON l.list_id = i.list_id 
        -- ingest the inbox list
    UNION
    SELECT
        'inbox120295392' :: text,
        'Inbox' :: text,
        '1' :: BOOLEAN,
        'default' :: text,
        '1' :: BOOLEAN,
        '2413980260956790869' :: bigint,
        '' :: text,
        'dueDate' :: text,
        '1' :: INTEGER,
        '7si0ks2b' :: text,
        '2024-06-18 08:44:47.704' :: TIMESTAMP without TIME ZONE,
        '0' :: BOOLEAN,
        '0' :: BOOLEAN,
        'default' :: text,
        '2843425faae40e6deeb4b829' :: text,
        'default' :: text,
        'default' :: text,
        'default' :: text,
        'default' :: text,
        'TASK' :: text,
        '' :: text,
        '1' :: BOOLEAN,
        '0' :: BOOLEAN,
        '0' :: BOOLEAN,
        'default' :: text,
        '1' :: text,
        '2022-08-22 15:04:29' :: TIMESTAMP without TIME ZONE,
        '1' :: BOOLEAN
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,*
FROM
    joined
