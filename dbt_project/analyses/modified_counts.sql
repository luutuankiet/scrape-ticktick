with source as (

select 
coalesce(fld_folder_name,'Default') as fld_folder_name,
coalesce(l_list_name,'Inbox') as l_list_name,
datepart('day',active) as day,
datepart('month',active) as month,
datepart('year',active) as year,
max_day_active_timestamp,
count(*) as cnt
from 
(
select 
td_modified_time::timestamp as active,
max(active) over(partition by fld_folder_name,l_list_name,datepart('day',active),datepart('month',active),datepart('year',active)) as max_day_active_timestamp,
*
from obt
) a
group by 
fld_folder_name,
l_list_name,
datepart('day',active),
datepart('month',active),
datepart('year',active),
max_day_active_timestamp
),

task_level as (
select 
fld_folder_name,
l_list_name,
sum(cnt)::int as tasks_active,
max_day_active_timestamp,
 day,month,year

from source group by day,month,year,l_list_name,fld_folder_name,max_day_active_timestamp


)

select t.*
,o.td_timezone
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level t 
 inner join 
 (select
 td_timezone,
 fld_folder_name,
 l_list_name,
 td_modified_time
 from obt
 ) o on o.td_modified_time=t.max_day_active_timestamp
 and o.fld_folder_name=t.fld_folder_name
 and o.l_list_name=t.l_list_name
 