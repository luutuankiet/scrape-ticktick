WITH source AS (
    SELECT *
    FROM
        {{ source (
            'raw_data',
            'raw_data'
        ) }}
)
,
stg_statuses AS (
    SELECT DISTINCT
        CAST(
            status AS INT
        ) AS status_id,
        CASE
            WHEN status = '-1' THEN 'wont do'
            WHEN status = '2' THEN 'done'
            WHEN status = '0' THEN 'undone'
        END AS "desc",
        CASE
            WHEN status = '-1' THEN 'regardless of archival'
            WHEN status = '2' THEN 'regardless of archival'
            WHEN status = '0' THEN 'regardless of archival'
        END AS status_comments
    FROM
        source
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['status_id']) }} AS status_key,
    *
FROM
    stg_statuses
