with source as (
      select 
        {{setup_nulls(source('raw_data', 'tasks_raw'))}}
      
       from {{ source('raw_data', 'tasks_raw') }}
),
renamed as (
    select
        {{ adapter.quote("id") }}:: text as "todo_id",
        {{ adapter.quote("projectid") }}:: text as "todo_projectid",
        {{ adapter.quote("sortorder") }}:: bigint as "todo_sortorder",
        {{ adapter.quote("title") }}:: text as "todo_title",
        {{ adapter.quote("content") }}:: text as "todo_content",
        {{ adapter.quote("desc") }}:: text as "todo_desc",
        {{ adapter.quote("timezone") }}:: text as "todo_timezone",
        {{ adapter.quote("isfloating") }}:: boolean as "todo_isfloating",
        {{ adapter.quote("isallday") }}:: boolean as "todo_isallday",
        {{ adapter.quote("reminder") }}:: text as "todo_reminder",
        {{ adapter.quote("reminders") }}:: text as "reminders" , -- array
        {{ adapter.quote("exdate") }}:: text as "todo_exdate",
        {{ adapter.quote("priority") }}:: int as "todo_priority",
        {{ adapter.quote("status") }}:: text as "todo_status",
        {{ adapter.quote("items") }}:: text as "todo_items",
        {{ adapter.quote("progress") }}:: float as "todo_progress",
        {{ adapter.quote("modifiedtime") }}:: timestamp as "todo_modifiedtime",
        {{ adapter.quote("etag") }}:: text as "todo_etag",
        {{ adapter.quote("deleted") }}:: boolean as "todo_deleted",
        {{ adapter.quote("createdtime") }}:: timestamp as "todo_createdtime",
        {{ adapter.quote("creator") }}:: int as "todo_creator",
        {{ adapter.quote("focussummaries") }}:: text as "todo_focussummaries",
        {{ adapter.quote("columnid") }}:: text as "todo_columnid",
        {{ adapter.quote("kind") }}:: text as "todo_kind",
        {{ adapter.quote("imgmode") }}:: text as "todo_imgmode",
        {{ adapter.quote("tags") }}:: text as "todo_tags",
        {{ adapter.quote("repeatfrom") }}:: int as "todo_repeatfrom",
        {{ adapter.quote("attachments") }}:: text as "todo_attachments", -- json
        {{ adapter.quote("repeattaskid") }}:: text as "todo_repeattaskid",
        {{ adapter.quote("commentcount") }}:: float as "todo_commentcount",
        {{ adapter.quote("completedtime") }}:: timestamp as "todo_completedtime",
        {{ adapter.quote("completeduserid") }}:: text as "todo_completeduserid", -- "120295392.0"
        {{ adapter.quote("repeatflag") }}:: text as "todo_repeatflag",
        {{ adapter.quote("startdate") }}:: timestamp as "todo_startdate",
        {{ adapter.quote("duedate") }}:: timestamp as "todo_duedate",
        {{ adapter.quote("pinnedtime") }}:: timestamp as "todo_pinnedtime",
        {{ adapter.quote("childids") }}:: text as "childids" , -- array
        {{ adapter.quote("deletedtime") }}:: text as "todo_deletedtime", -- some weird epoc time ? "120295392.0" >>> to_timestamp(1669956236000 / 1000)
        {{ adapter.quote("repeatfirstdate") }}:: timestamp as "todo_repeatfirstdate",
        {{ adapter.quote("pomodorosummaries") }}:: text as "todo_pomodorosummaries", -- array
        {{ adapter.quote("parentid") }}:: text as "todo_parentid",
        {{ adapter.quote("annoyingalert") }}:: text as "todo_annoyingalert",
        {{ adapter.quote("remindtime") }}:: text as "todo_remindtime"

    from source
)
select * from renamed
  