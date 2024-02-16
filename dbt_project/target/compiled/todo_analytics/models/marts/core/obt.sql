WITH f_todos AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."fact_todos"
),

d_lists AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_lists"
),

d_folders AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_folders"
),

d_statuses AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_statuses"
),

d_start_dates AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_dates"
),

d_due_dates AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_dates"
),

d_created_dates AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_dates"
),

d_completed_dates AS (
    SELECT *
    FROM
        "ticktick_gtd"."main"."dim_dates"
)

SELECT
    f_todos."todo_id" as "td_todo_id",
  f_todos."todo_key:1" as "td_todo_key:1",
  f_todos."todo_id:1" as "td_todo_id:1",
  f_todos."folder_name" as "td_folder_name",
  f_todos."list_name" as "td_list_name",
  f_todos."status_id" as "td_status_id",
  f_todos."title" as "td_title",
  f_todos."timezone" as "td_timezone",
  f_todos."reminder" as "td_reminder",
  f_todos."reminders" as "td_reminders",
  f_todos."exDate" as "td_exDate",
  f_todos."items" as "td_items",
  f_todos."progress" as "td_progress",
  f_todos."modified_time" as "td_modified_time",
  f_todos."completed_time" as "td_completed_time",
  f_todos."created_time" as "td_created_time",
  f_todos."etag" as "td_etag",
  f_todos."deleted" as "td_deleted",
  f_todos."kind" as "td_kind",
  f_todos."tags" as "td_tags",
  f_todos."repeatFrom" as "td_repeatFrom",
  f_todos."repeatTaskId" as "td_repeatTaskId",
  f_todos."repeatFlag" as "td_repeatFlag",
  f_todos."pinned_time" as "td_pinned_time",
  f_todos."start_date" as "td_start_date",
  f_todos."due_date" as "td_due_date",
  f_todos."deletedTime" as "td_deletedTime",
  f_todos."repeatFirstDate" as "td_repeatFirstDate",
  f_todos."parentId" as "td_parentId",
  f_todos."remindTime" as "td_remindTime",
    d_lists."list_id" as "l_list_id",
  d_lists."list_name" as "l_list_name",
  d_lists."modified_time" as "l_modified_time",
  d_lists."folder_id" as "l_folder_id",
  d_lists."lkind" as "l_lkind",
  d_lists."is_active" as "l_is_active",
  d_lists."created_time" as "l_created_time",
    d_folders."folder_id" as "fld_folder_id",
  d_folders."folder_name" as "fld_folder_name",
    d_statuses."status_id" as "ss_status_id",
  d_statuses."desc" as "ss_desc",
  d_statuses."status_comments" as "ss_status_comments",
    -- dates roleplay
    d_start_dates."date_id" as "start_date_id",
  d_start_dates."day_of_year" as "start_day_of_year",
  d_start_dates."week_key" as "start_week_key",
  d_start_dates."week_of_year" as "start_week_of_year",
  d_start_dates."day_of_week" as "start_day_of_week",
  d_start_dates."iso_day_of_week" as "start_iso_day_of_week",
  d_start_dates."day_name" as "start_day_name",
  d_start_dates."first_day_of_week" as "start_first_day_of_week",
  d_start_dates."last_day_of_week" as "start_last_day_of_week",
  d_start_dates."month_key" as "start_month_key",
  d_start_dates."month_of_year" as "start_month_of_year",
  d_start_dates."day_of_month" as "start_day_of_month",
  d_start_dates."month_name_short" as "start_month_name_short",
  d_start_dates."month_name" as "start_month_name",
  d_start_dates."first_day_of_month" as "start_first_day_of_month",
  d_start_dates."last_day_of_month" as "start_last_day_of_month",
  d_start_dates."quarter_key" as "start_quarter_key",
  d_start_dates."quarter_of_year" as "start_quarter_of_year",
  d_start_dates."day_of_quarter" as "start_day_of_quarter",
  d_start_dates."quarter_desc_short" as "start_quarter_desc_short",
  d_start_dates."quarter_desc" as "start_quarter_desc",
  d_start_dates."first_day_of_quarter" as "start_first_day_of_quarter",
  d_start_dates."last_day_of_quarter" as "start_last_day_of_quarter",
  d_start_dates."year_key" as "start_year_key",
  d_start_dates."first_day_of_year" as "start_first_day_of_year",
  d_start_dates."last_day_of_year" as "start_last_day_of_year",
  d_start_dates."ordinal_weekday_of_month" as "start_ordinal_weekday_of_month",
    d_due_dates."date_id" as "due_date_id",
  d_due_dates."day_of_year" as "due_day_of_year",
  d_due_dates."week_key" as "due_week_key",
  d_due_dates."week_of_year" as "due_week_of_year",
  d_due_dates."day_of_week" as "due_day_of_week",
  d_due_dates."iso_day_of_week" as "due_iso_day_of_week",
  d_due_dates."day_name" as "due_day_name",
  d_due_dates."first_day_of_week" as "due_first_day_of_week",
  d_due_dates."last_day_of_week" as "due_last_day_of_week",
  d_due_dates."month_key" as "due_month_key",
  d_due_dates."month_of_year" as "due_month_of_year",
  d_due_dates."day_of_month" as "due_day_of_month",
  d_due_dates."month_name_short" as "due_month_name_short",
  d_due_dates."month_name" as "due_month_name",
  d_due_dates."first_day_of_month" as "due_first_day_of_month",
  d_due_dates."last_day_of_month" as "due_last_day_of_month",
  d_due_dates."quarter_key" as "due_quarter_key",
  d_due_dates."quarter_of_year" as "due_quarter_of_year",
  d_due_dates."day_of_quarter" as "due_day_of_quarter",
  d_due_dates."quarter_desc_short" as "due_quarter_desc_short",
  d_due_dates."quarter_desc" as "due_quarter_desc",
  d_due_dates."first_day_of_quarter" as "due_first_day_of_quarter",
  d_due_dates."last_day_of_quarter" as "due_last_day_of_quarter",
  d_due_dates."year_key" as "due_year_key",
  d_due_dates."first_day_of_year" as "due_first_day_of_year",
  d_due_dates."last_day_of_year" as "due_last_day_of_year",
  d_due_dates."ordinal_weekday_of_month" as "due_ordinal_weekday_of_month",
    d_completed_dates."date_id" as "completed_date_id",
  d_completed_dates."day_of_year" as "completed_day_of_year",
  d_completed_dates."week_key" as "completed_week_key",
  d_completed_dates."week_of_year" as "completed_week_of_year",
  d_completed_dates."day_of_week" as "completed_day_of_week",
  d_completed_dates."iso_day_of_week" as "completed_iso_day_of_week",
  d_completed_dates."day_name" as "completed_day_name",
  d_completed_dates."first_day_of_week" as "completed_first_day_of_week",
  d_completed_dates."last_day_of_week" as "completed_last_day_of_week",
  d_completed_dates."month_key" as "completed_month_key",
  d_completed_dates."month_of_year" as "completed_month_of_year",
  d_completed_dates."day_of_month" as "completed_day_of_month",
  d_completed_dates."month_name_short" as "completed_month_name_short",
  d_completed_dates."month_name" as "completed_month_name",
  d_completed_dates."first_day_of_month" as "completed_first_day_of_month",
  d_completed_dates."last_day_of_month" as "completed_last_day_of_month",
  d_completed_dates."quarter_key" as "completed_quarter_key",
  d_completed_dates."quarter_of_year" as "completed_quarter_of_year",
  d_completed_dates."day_of_quarter" as "completed_day_of_quarter",
  d_completed_dates."quarter_desc_short" as "completed_quarter_desc_short",
  d_completed_dates."quarter_desc" as "completed_quarter_desc",
  d_completed_dates."first_day_of_quarter" as "completed_first_day_of_quarter",
  d_completed_dates."last_day_of_quarter" as "completed_last_day_of_quarter",
  d_completed_dates."year_key" as "completed_year_key",
  d_completed_dates."first_day_of_year" as "completed_first_day_of_year",
  d_completed_dates."last_day_of_year" as "completed_last_day_of_year",
  d_completed_dates."ordinal_weekday_of_month" as "completed_ordinal_weekday_of_month",
    d_created_dates."date_id" as "created_date_id",
  d_created_dates."day_of_year" as "created_day_of_year",
  d_created_dates."week_key" as "created_week_key",
  d_created_dates."week_of_year" as "created_week_of_year",
  d_created_dates."day_of_week" as "created_day_of_week",
  d_created_dates."iso_day_of_week" as "created_iso_day_of_week",
  d_created_dates."day_name" as "created_day_name",
  d_created_dates."first_day_of_week" as "created_first_day_of_week",
  d_created_dates."last_day_of_week" as "created_last_day_of_week",
  d_created_dates."month_key" as "created_month_key",
  d_created_dates."month_of_year" as "created_month_of_year",
  d_created_dates."day_of_month" as "created_day_of_month",
  d_created_dates."month_name_short" as "created_month_name_short",
  d_created_dates."month_name" as "created_month_name",
  d_created_dates."first_day_of_month" as "created_first_day_of_month",
  d_created_dates."last_day_of_month" as "created_last_day_of_month",
  d_created_dates."quarter_key" as "created_quarter_key",
  d_created_dates."quarter_of_year" as "created_quarter_of_year",
  d_created_dates."day_of_quarter" as "created_day_of_quarter",
  d_created_dates."quarter_desc_short" as "created_quarter_desc_short",
  d_created_dates."quarter_desc" as "created_quarter_desc",
  d_created_dates."first_day_of_quarter" as "created_first_day_of_quarter",
  d_created_dates."last_day_of_quarter" as "created_last_day_of_quarter",
  d_created_dates."year_key" as "created_year_key",
  d_created_dates."first_day_of_year" as "created_first_day_of_year",
  d_created_dates."last_day_of_year" as "created_last_day_of_year",
  d_created_dates."ordinal_weekday_of_month" as "created_ordinal_weekday_of_month"
FROM
    f_todos
LEFT JOIN d_lists
    ON f_todos.list_key = d_lists.list_key
LEFT JOIN d_folders
    ON f_todos.folder_key = d_folders.folder_key
LEFT JOIN d_statuses
    ON f_todos.status_key = d_statuses.status_key
LEFT JOIN d_start_dates
    ON f_todos.date_start_key = d_start_dates.date_key
LEFT JOIN d_due_dates
    ON f_todos.date_due_key = d_due_dates.date_key
LEFT JOIN d_completed_dates
    ON f_todos.date_completed_key = d_completed_dates.date_key
LEFT JOIN d_created_dates
    ON f_todos.date_created_key = d_created_dates.date_key