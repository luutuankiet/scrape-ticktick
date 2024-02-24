             
                            select * from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%'                            
                            and due_date_id is not null 
                               
                                