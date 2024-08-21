{# materialized='incremental', #}
{# unique_key = ['todo_id'], #}
{# on_schema_change='append_new_columns', #}
{{ config(
    materialized = 'table',
    indexes = [ {'columns': ['list_key'],
    'type': 'hash' },{ 'columns': ['folder_key'],
    'type': 'hash' },{ 'columns': ['status_key'],
    'type': 'hash' },{ 'columns': ['date_start_key'],
    'type': 'hash' },{ 'columns': ['date_due_key'],
    'type': 'hash' },{ 'columns': ['date_completed_key'],
    'type': 'hash' },{ 'columns': ['date_created_key'],
    'type': 'hash' },{ 'columns': ['date_modified_key'],
    'type': 'hash' },{ 'columns': ['date_due_lookahead_key'],
    'type': 'hash' },],
    unlogged = True
) }}

WITH init_todo AS (

    SELECT
        DISTINCT {{ coalesce_defaults(ref('src__tasks_raw')) }}
    FROM
        {{ ref('src__tasks_raw') }}
),
_todo__recurring AS (
    -- handle flagging habits
    SELECT
        *,
        CASE
            WHEN (
                todo_status <> '0'
                AND EXISTS (
                    SELECT
                        todo_id
                    FROM
                        init_todo A
                    WHERE
                        A.todo_id = b.todo_repeattaskid
                        AND A.todo_repeatflag <> 'default'
                )
            )
            OR (
                todo_status = '0'
                AND todo_repeatflag <> 'default'
            ) THEN 'recurring'
            ELSE 'default'
        END AS todo_derived__recurring
    FROM
        init_todo b
),
_todo__habit_streak_init AS (
    -- create buckets
    SELECT
        *,
        CASE
            WHEN todo_status = '2' THEN SUM(
                CASE
                    WHEN todo_status = '2' THEN 1
                    ELSE 0
                END
            ) over (
                PARTITION BY todo_repeattaskid
                ORDER BY
                    todo_completedtime rows BETWEEN unbounded preceding
                    AND CURRENT ROW
            ) - ROW_NUMBER() over (
                PARTITION BY todo_repeattaskid
                ORDER BY
                    todo_completedtime
            ) + 1
            ELSE NULL
        END AS _todo__habit_streak_bucket_id
    FROM
        _todo__recurring
),
_todo__habit_streak AS (
    -- add additional column for rolling streak counter all time
    SELECT
        *,
        CASE
            WHEN todo_status = '2' THEN ROW_NUMBER() over(
                PARTITION BY todo_repeattaskid,
                _todo__habit_streak_bucket_id
                ORDER BY
                    todo_completedtime ASC
            )
            when todo_status = '0' then NULL
            when todo_status = '-1' then 0
        END AS todo_derived__habit_streak
    FROM
        _todo__habit_streak_init
    WHERE
        todo_derived__recurring = 'recurring'
),
todo AS (
    SELECT
        r.*,
        h.todo_derived__habit_streak,
        h._todo__habit_streak_bucket_id
    FROM
        _todo__recurring r
        LEFT JOIN _todo__habit_streak h
        ON r.todo_id = h.todo_id
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
dates_lookahead AS (
    SELECT
        *
    FROM
        {{ ref('stg_dates_lookahead') }}
),
joined AS (
    SELECT
        {# gotta handle the NULLs from this join; they are hashed. next up is to generate that hashed null in other tables #}
        {{ dbt_utils.generate_surrogate_key(['dds.date_id']) }} AS date_start_key,
        {{ dbt_utils.generate_surrogate_key(['ddd.date_id']) }} AS date_due_key,
        {{ dbt_utils.generate_surrogate_key(['dl.date_id']) }} AS date_due_lookahead_key,
        {{ dbt_utils.generate_surrogate_key(['ddcm.date_id']) }} AS date_completed_key,
        {{ dbt_utils.generate_surrogate_key(['ddc.date_id']) }} AS date_created_key,
        {{ dbt_utils.generate_surrogate_key(['ddm.date_id']) }} AS date_modified_key,
        {{ dbt_utils.generate_surrogate_key(['todo_id']) }} AS todo_key,
        {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,
        {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,
        {{ dbt_utils.generate_surrogate_key(['status_id']) }} AS status_key,
        t.*,
        CASE
            WHEN -- build the flag window
            -- case1: the records from due_lookahead
            dl.date_id IS NOT NULL THEN TRUE
            WHEN -- case2: the left records facts; grabs dummy records within the window
            todo_id IS NULL THEN TRUE
            ELSE FALSE
        END AS lookahead_flag,
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
        LEFT JOIN dates ddm
        ON ddm.date_id = t.todo_modifiedtime_derived_date full
        OUTER JOIN dates_lookahead dl
        ON dl.date_id = t.todo_duedate_derived_date
)
SELECT
    *
FROM
    joined
