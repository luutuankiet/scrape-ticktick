with source as (

select 
coalesce(fld_folder_name,'Default') as fld_folder_name,
coalesce(l_list_name,'Inbox') as l_list_name,
datepart('day',active) as day,
datepart('month',active) as month,
datepart('year',active) as year,
count(*) as cnt
from 
(
select 
td_modified_time::timestamp as active,
*
from obt
) a
group by 
fld_folder_name,
l_list_name,
datepart('day',active),
datepart('month',active),
datepart('year',active) 
),

task_level as (
select 
fld_folder_name,
l_list_name,
sum(cnt) as tasks_active, day,month,year

from source group by day,month,year,l_list_name,fld_folder_name


)

select *
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level