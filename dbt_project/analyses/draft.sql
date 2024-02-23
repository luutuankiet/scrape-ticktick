  select 
                                due_date_id,td_repeatFlag,count(*) as cnt  from 
                            
                            (
                            select * from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%'                            
                            ) new
                                where due_date_id is not null
                                group by due_date_id,td_repeatFlag
                                having td_repeatFlag = 'nan'