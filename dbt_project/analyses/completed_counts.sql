with source as (

select 
fld_folder_name,
l_list_name,
datepart('day',active) as day,
datepart('month',active) as month,
datepart('year',active) as year,
count(*) as cnt
from 
(
select 
td_completed_time::timestamp as active,
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
sum(cnt) as tasks_completed, 
day,month,year

from source 
group by day,month,year


)

select *
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level
 

