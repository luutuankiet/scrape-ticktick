with source as (

select 
coalesce(fld_folder_name,'Default') as fld_folder_name,
coalesce(l_list_name,'Inbox') as l_list_name,
datepart('day',created) as day,
datepart('month',created) as month,
datepart('year',created) as year,
max_day_created_timestamp,
count(*) as cnt
from 
(
select 
td_created_time::timestamp as created,
max(created) over(partition by fld_folder_name,l_list_name,datepart('day',created),datepart('month',created),datepart('year',created)) as max_day_created_timestamp,

*
from obt) a
group by 
fld_folder_name,
l_list_name,
datepart('day',created),
datepart('month',created),
datepart('year',created),
max_day_created_timestamp 
),

task_level as (

select 
fld_folder_name,
l_list_name,
sum(cnt) as tasks_created,
max_day_created_timestamp,
 day,month,year

from source group by day,month,year,l_list_name,fld_folder_name,max_day_created_timestamp


)

select *
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level
 

