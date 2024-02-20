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
td_modified_time::timestamp as active,
*
from obt) a
group by 
fld_folder_name,
l_list_name,
datepart('day',active),
datepart('month',active),
datepart('year',active) 
),

task_level as (
select count(*) as tasks_active, day,month,year

from source group by day,month,year


)

select *
,(year||'-'||month||'-'||day)::date as key
,(year||'-'||month||'-'||day) as day_of_year
 from task_level
 


-- select 
-- *

-- from source 
-- order by day,month,year,fld_folder_name,l_list_name





-- select * from obt where td_modified_time::timestamp like '2024-01-09%' 