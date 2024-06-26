WITH todo AS (
    SELECT
        {{coalesce_defaults(ref('src__tasks_raw'))}}
    FROM
        {{ ref('src__tasks_raw') }}
),
lists AS (
    SELECT
        {{coalesce_defaults(ref('src__lists_raw'))}}
        
    FROM
        {{ ref('src__lists_raw') }}
),
folders AS (
    SELECT
        {{coalesce_defaults(ref('src__folders_raw'))}}
        
    FROM
        {{ ref('src__folders_raw') }}
),
joined AS (
    SELECT
        t.*,
        coalesce(l.list_name,'default') as list_name,
        coalesce(f.folder_name,'default') as folder_name
    FROM
        todo t
        LEFT JOIN lists l
        ON t.todo_projectid = l.list_id
        LEFT JOIN folders f
        ON l.list_groupid = f.folder_id
)
SELECT
    {{dbt_utils.generate_surrogate_key(['todo_id'])}} as todo_key,*
FROM
    joined