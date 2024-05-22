with source as (
    select * from {{ ref('init__trans_nulls__todos') }} 
 )
,
dtypes as (
    select 
id::text as todo_id,
name::text as folder_name,
name_1::text as list_name,
status::int as status_id,
title::text as title,
timeZone::text as timeZone,
reminder::text as reminder,
reminders::text as reminders,
exDate::date as exDate,
items::text as items,
progress::float as progress,
modifiedTime::timestamp as modified_time,
completedTime::timestamp as completed_time,
createdTime::timestamp as created_time,
etag::text as etag,
deleted::int as deleted,
kind::text as kind,
tags::text as tags,
repeatFrom::text as repeatFrom,
repeatTaskId::text as repeatTaskId,
repeatFlag::text as repeatFlag,
pinnedTime::timestamp as pinned_time,
startDate::timestamp as start_date,
dueDate::timestamp as due_date,
deletedTime::text as deletedTime,
repeatFirstDate::timestamp as repeatFirstDate,
parentId::text as parentId,
remindTime::timestamp as remindTime
from source 
)
 select * from dtypes