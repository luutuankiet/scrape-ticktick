
{{ config(
    materialized='incremental',
    unique_key = ['todo_id'],
    incremental_strategy = 'merge',
    on_schema_change='append_new_columns'
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
            ) THEN TRUE
            ELSE FALSE
        END AS todo_derived__is_repeat
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
            WHEN todo_status = '0' THEN NULL
            WHEN todo_status = '-1' THEN 0
        END AS todo_derived__habit_streak
    FROM
        _todo__habit_streak_init
),
_todo__habit_latest_wrapper AS (
    -- add bunch of wrapper fields for those recurring that grabs the latest ocurrence's fields
    SELECT
        COALESCE(
            b.todo_title,
            A.todo_title
        ) AS todo_title,
        COALESCE(
            b.todo_projectid,
            A.todo_projectid
        ) AS todo_projectid,
        A.todo_derived__is_repeat,
        A._todo__habit_streak_bucket_id,
        A.todo_derived__habit_streak,
        {{ dbt_utils.star(ref('src__tasks_raw'), relation_alias = 'A', except = ["todo_title", "todo_projectid" ]) }}
    FROM
        _todo__habit_streak A
        LEFT JOIN _todo__habit_streak b
        ON A.todo_repeattaskid = b.todo_id
),
todo_habit_stg AS (
    SELECT
        h.todo_title,
        h.todo_projectid,
        h.todo_derived__habit_streak,
        h._todo__habit_streak_bucket_id,
        r.todo_derived__is_repeat,
        {{ dbt_utils.star(ref('src__tasks_raw'), relation_alias = 'r', except = ["todo_title", "todo_projectid" ]) }}
    FROM
        _todo__recurring r
        LEFT JOIN _todo__habit_latest_wrapper h
        ON r.todo_id = h.todo_id),

init_todo_add_consecutive_undone AS (
    SELECT
        todo_habit_stg.*,
        CASE
            
            WHEN todo_status in ('-1','2') THEN SUM( -- add in 0 to also wrap undone NEW tasks to the count
                CASE
                    WHEN todo_status = '-1' THEN 1
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
        END AS _todo__habit_undone_streak_bucket_id,
        lag(todo_status) over (partition by todo_repeattaskid order by todo_duedate) as _status_lag,
        lead(todo_status) over (partition by todo_repeattaskid order by todo_duedate) as _status_lead
    FROM
        todo_habit_stg
),
todo_add_consecutive_undone AS (
    SELECT
        init_todo_add_consecutive_undone.*,
        CASE
            
            WHEN todo_status in ('-1','2')
            AND _todo__habit_undone_streak_bucket_id = MIN(_todo__habit_undone_streak_bucket_id) over (
                PARTITION BY todo_repeattaskid
            )
            THEN SUM(
                CASE
                    WHEN todo_status = '-1' THEN 1
                    WHEN todo_status = '2' and (_status_lag = '-1' and _status_lead in ('2','0')) 
                    THEN -99999

                    ELSE 0
                END
            ) over(
                PARTITION BY todo_repeattaskid,
                _todo__habit_undone_streak_bucket_id
            )
            ELSE 0
        END AS _todo_derived__consecutive_undone
    FROM
        init_todo_add_consecutive_undone
),
stg_todo_undone AS (
    select todo_add_consecutive_undone.*,
        case
            when max(_todo_derived__consecutive_undone) over(partition by todo_title) > 0 
            then max(_todo_derived__consecutive_undone) over (partition by todo_title)
            else null
        end as todo_derived__consecutive_undone
    from todo_add_consecutive_undone
),
todo AS (
    -- this be the final table
    SELECT
        *
    FROM
        stg_todo_undone
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
        {{ dbt_utils.generate_surrogate_key(['ddm.date_id']) }} AS date_modified_key,
        {{ dbt_utils.generate_surrogate_key(['list_id']) }} AS list_key,
        {{ dbt_utils.generate_surrogate_key(['folder_id']) }} AS folder_key,
        {{ dbt_utils.generate_surrogate_key(['status_id']) }} AS status_key,
        t.*,
        COALESCE(l.list_name, 'default') AS todo_list_name,
        COALESCE(f.folder_name, 'default') AS todo_folder_name,
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
        ON ddm.date_id = t.todo_modifiedtime_derived_date
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['todo_id']) }} AS todo_key,
    *
FROM
    joined

{% if is_incremental() %}
  WHERE 
  todo_modifiedtime >= (select coalesce(max(todo_modifiedtime),'1900-01-01 00:00:00') from {{ this }} )
  OR
  todo_modifiedtime IS NULL
{% endif %}