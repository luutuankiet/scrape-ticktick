select 
* from 
(select 
fld_folder_name
,l_list_name
,sum(case when td_tags like '%clarifyme%' then 1 else 0 end) as cnt_clarifyme
,sum(case when td_tags = '[]' then 1 else 0 end) as cnt_none
,sum(case when td_tags like '%@%' then 1 else 0 end) as cnt_context
,sum(case when td_tags like '%someday%' then 1 else 0 end) as cnt_someday
,sum(case when td_tags like '%waiting_for%' then 1 else 0 end) as cnt_waiting_for

from obt
where td_kind = 'TEXT' and ss_desc = 'undone'
group by fld_folder_name
,l_list_name
) a where cnt_clarifyme + cnt_none + cnt_context + cnt_someday + cnt_waiting_for <> 0
order by 1,2