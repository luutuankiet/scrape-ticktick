{{ config(
    materialized = 'view',
) }}

WITH source AS (

    SELECT
        *
    FROM
        {{ ref('stg_todos') }}
),

dates_lookahead AS (
    SELECT
        *
    FROM
        {{ ref('stg_dates_lookahead') }}
),
joined AS (
    SELECT
        t.*,
        {{ dbt_utils.generate_surrogate_key(['dl.date_id']) }} AS date_due_lookahead_key,
        {{ dbt_utils.generate_surrogate_key(['dl.date_id','todo_id']) }} AS todo_lookahead_skey,
        CASE
            WHEN -- build the flag window
            -- case1: the records from due_lookahead
            dl.date_id IS NOT NULL THEN TRUE
            WHEN -- case2: the left records facts; grabs dummy records within the window
            todo_id IS NULL THEN TRUE
            ELSE FALSE
        END AS lookahead_flag
    FROM
        source t
        {# injecting the dummy due dates lookahead  #}
        FULL OUTER JOIN dates_lookahead dl
        ON dl.date_id = t.todo_duedate_derived_date
)
SELECT
    *
FROM
    joined
