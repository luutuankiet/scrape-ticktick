with source as (

select 
coalesce(fld_folder_name,'Default') as fld_folder_name,
coalesce(l_list_name,'Inbox') as l_list_name,
datepart('day',completed) as day,
datepart('month',completed) as month,
datepart('year',completed) as year,
max_day_completed_timestamp,
count(*) as cnt
from 
(
select 
td_completed_time::timestamp as completed,
max(completed) over(partition by fld_folder_name,l_list_name,datepart('day',completed),datepart('month',completed),datepart('year',completed)) as max_day_completed_timestamp,

*
from obt) a
group by 
fld_folder_name,
l_list_name,
datepart('day',completed),
datepart('month',completed),
datepart('year',completed),
max_day_completed_timestamp
),

task_level as (

select 
fld_folder_name,
l_list_name,
sum(cnt)::int as tasks_completed,
max_day_completed_timestamp,
 day,month,year

from source group by day,month,year,l_list_name,fld_folder_name,max_day_completed_timestamp


)

select t.*
,td_timezone
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level t
 inner join 

(select
 td_timezone,
 fld_folder_name,
 l_list_name,
 td_completed_time
 from obt
 ) o on o.td_completed_time=t.max_day_completed_timestamp
 and o.fld_folder_name=t.fld_folder_name
 and o.l_list_name=t.l_list_name
 