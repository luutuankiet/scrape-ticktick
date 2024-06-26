WITH source AS (
    SELECT
        {{coalesce_defaults(ref('src__tasks_raw'))}}
    FROM
        {{ref('src__tasks_raw')}}
),
renamed AS (
    SELECT
        DISTINCT todo_status AS status_id,
        CASE
            WHEN todo_status = '-1' THEN 'wont do'
            WHEN todo_status = '2' THEN 'done'
            WHEN todo_status = '0' THEN 'undone'
        END AS "status_desc",
        CASE
            WHEN todo_status = '-1' THEN 'regardless of archival'
            WHEN todo_status = '2' THEN 'regardless of archival'
            WHEN todo_status = '0' THEN 'regardless of archival'
        END AS status_comments
    FROM
        source
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['status_id']) }} AS status_key,*
FROM
    renamed
