with source as (
      select 
        {{setup_nulls(source('raw_data', 'tasks_raw'))}}
      
       from {{ source('raw_data', 'tasks_raw') }}
),
renamed as (
    select
        {{ adapter.quote("id") }},
        {{ adapter.quote("projectid") }},
        {{ adapter.quote("sortorder") }},
        {{ adapter.quote("title") }},
        {{ adapter.quote("content") }},
        {{ adapter.quote("desc") }},
        {{ adapter.quote("timezone") }},
        {{ adapter.quote("isfloating") }},
        {{ adapter.quote("isallday") }},
        {{ adapter.quote("reminder") }},
        {{ adapter.quote("reminders") }},
        {{ adapter.quote("exdate") }},
        {{ adapter.quote("priority") }},
        {{ adapter.quote("status") }},
        {{ adapter.quote("items") }},
        {{ adapter.quote("progress") }},
        {{ adapter.quote("modifiedtime") }},
        {{ adapter.quote("etag") }},
        {{ adapter.quote("deleted") }},
        {{ adapter.quote("createdtime") }},
        {{ adapter.quote("creator") }},
        {{ adapter.quote("focussummaries") }},
        {{ adapter.quote("columnid") }},
        {{ adapter.quote("kind") }},
        {{ adapter.quote("imgmode") }},
        {{ adapter.quote("tags") }},
        {{ adapter.quote("repeatfrom") }},
        {{ adapter.quote("attachments") }},
        {{ adapter.quote("repeattaskid") }},
        {{ adapter.quote("commentcount") }},
        {{ adapter.quote("completedtime") }},
        {{ adapter.quote("completeduserid") }},
        {{ adapter.quote("repeatflag") }},
        {{ adapter.quote("startdate") }},
        {{ adapter.quote("duedate") }},
        {{ adapter.quote("pinnedtime") }},
        {{ adapter.quote("childids") }},
        {{ adapter.quote("deletedtime") }},
        {{ adapter.quote("repeatfirstdate") }},
        {{ adapter.quote("pomodorosummaries") }},
        {{ adapter.quote("parentid") }},
        {{ adapter.quote("annoyingalert") }},
        {{ adapter.quote("remindtime") }}

    from source
)
select * from renamed
  