import streamlit as st
import duckdb
import os
import pandas as pd
from helper.source_env import dbt_project_dir
import datetime
import re
import altair as alt

motherduck_token = os.environ.get("motherduck_token")
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()


analytics_path = os.path.join(dbt_project_dir,'analyses')
tags_count_path = os.path.join(analytics_path,'active_tags_count.sql')
loops_count_path = os.path.join(analytics_path,'open_loops_count.sql')
active_count_path = os.path.join(analytics_path,'modified_counts.sql')
created_count_path = os.path.join(analytics_path,'created_counts.sql')
completed_count_path = os.path.join(analytics_path,'completed_counts.sql')

st.set_page_config(page_title="MY GTD DASHBOARD", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

st.header("🌏 Ken's GTD dashboard",divider="blue")



@st.cache_data(ttl=datetime.timedelta(hours=1),max_entries=10)
def get_table(query):
    return cur.sql(query).df()
def get_table_nocache(query):
    return cur.sql(query).df()


obt=get_table("select * from obt")


with st.sidebar:
    if st.button("force script reload"):
        st.rerun()

    if st.button("force cache reload"):
        st.cache_data.clear()
    folders = obt['fld_folder_name'].drop_duplicates().to_list()
    filter_folder = st.multiselect('folders',folders,default=folders)

def highlight_cell(val):
    if val < 20:
        color = 'yellow' 
    # elif val < 80:
    #     color = 'yellow'
    # elif val < 75:
    #     color = 'orange'
    elif val == 100:
        color = 'blue'
    else: 
        color = ''
    return f'background-color: {color}'

def highlight_text(val):
    if val == 100:
        return 'color: #86acff; font-weight: bold;'
    elif 0 <= val < 100:
        # Calculate the RGB values for a color between red and green based on the progress
        r = int(255 * (1 - val/100))
        g = int(255 * (val/100))
        b = 0
        return f'color: rgb({r}, {g}, {b}); font-weight: bold;'
    else:
        return ''

def highlight_row(row):
    if any(row.astype(str).str.count('-') >= 4):
        return ['background-color: #D3D3D3; font-weight: bold;'] * len(row)
    else:
        return [''] * len(row)



tab1,tab2,tab3 = st.tabs(['🧑🏽‍💻 daily ops',
         '📊 analytics',
         'placeholder'
         ])



with tab1:
    st.write("# your main metrics")
    st.write("*to answer the question, how munch do i have in my head?*")
    with open(tags_count_path, 'r') as f:
        tags_query=f.read()
    tags_count = get_table_nocache(tags_query)

    with open(loops_count_path, 'r') as f:
        loops_query=f.read()


    loops_count = get_table_nocache(loops_query)
    loops = loops_count['content'].iloc[0]
    lines = loops.split('\n')
    counter = 0
    for line in lines:
        if re.search('[a-z0-9]',line.lower()):
            counter+=1 

    compare_clarify = int(tags_count['cnt_clarifyme'].iloc[0]) if tags_count.shape[0] > 0 else 0
        
    counter_delta = counter - compare_clarify        

    clarifyme_count = tags_count['cnt_clarifyme'].iloc[0] if tags_count.shape[0] > 0 else 0

    clarifyme_avg = 80 # TODO : count average clarifyme across dataset.
    delta_clarifyme =  clarifyme_count - clarifyme_avg
    
    today_table_query = """
                                select 
                                due_date_id,count(*) as cnt  from 
                            
                            (
                            select * from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%'                            
                            ) new
                                where due_date_id is not null
                                group by due_date_id

                            """
    today_table = get_table_nocache(today_table_query).reset_index(drop=True)
    overdue_count = today_table[today_table['due_date_id'] < pd.to_datetime(datetime.datetime.now().date())]
    overdue_count = overdue_count['cnt'].iloc[0] if overdue_count.shape[0] > 0 else 0

    today_count = today_table[today_table['due_date_id'] == pd.to_datetime(datetime.datetime.now().date())]
    today_count = today_count['cnt'].iloc[0] if today_count.shape[0] > 0 else 0
    today_avg = 8 # TODO : implement average count over dataset.
    delta_today = today_count - today_avg


    col1,col2,col3,col4 = st.columns(4)
    with col1:
          st.metric(
            label="overdue tasks",
            value=overdue_count,
            delta = "reschedule them!!!" if overdue_count > 0 else "all's well.",
            delta_color="inverse" if overdue_count > 0 else "off",
        )
          with st.expander("query"):
              debug_overdue_count=get_table_nocache("""
                            select 
                            due_date_id::date as due_date_id,
                                             td_created_time::timestamp as td_created_time,
                                                    td_modified_time::timestamp as td_modified_time,
                                             fld_folder_name,
                                             l_list_name,
                                             td_title
                                             ,* from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%' 
                            and due_date_id is not null
                                """).reset_index(drop=True)
              debug_overdue_count = debug_overdue_count[debug_overdue_count['due_date_id'] < pd.to_datetime(datetime.datetime.now().date())] if debug_overdue_count.shape[0] > 0 else None
              debug_overdue_count.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True,inplace=True)
              st.dataframe(debug_overdue_count,hide_index=True)
              st.code(today_table_query)    
    with col2:
          st.metric(
            label="tasks lined up",
            value=today_count,
            delta = f"{delta_today} than usual {today_avg} tasks" if today_count > 0 else "all's well.",
            delta_color="inverse" if today_count > 0 else "off",
        )
          with st.expander("query"):
              debug_today_count=get_table_nocache("""
                            select 
                             due_date_id::date as due_date_id,
                                             td_created_time::timestamp as td_created_time,
                                                    td_modified_time::timestamp as td_modified_time,
                                             fld_folder_name,
                                             l_list_name,
                                             td_title
                                             ,* from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%' 
                            and due_date_id is not null
                                """).reset_index(drop=True)
              debug_today_count = debug_today_count[debug_today_count['due_date_id'] == pd.to_datetime(datetime.datetime.now().date())]
              debug_today_count.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True,inplace=True)
              st.dataframe(debug_today_count,hide_index=True)
              st.code(today_table_query)    
            #   st.code(today_table)

    with col3:
        st.metric(
            "open loops",
            value = counter,
            delta = f"{counter_delta} than clarify" if counter > 0 else "all's well.",
            delta_color="inverse" if counter > 0 else "off",
            # help="compared to number of items to clarify"
            )
    with col4:
          st.metric(
            label="Clarifyme count",
            value=clarifyme_count,
            delta=f'{delta_clarifyme} than weekly average {clarifyme_avg}' if clarifyme_count > 0 else "all's well.",
            delta_color="inverse" if clarifyme_count > 0 else "off",
        )

    st.divider()

    st.write("## count of clarified and next action")
    
    try:
        colored_tags_count = tags_count.style.map(highlight_text,subset=['clarification_progress'])
    except Exception as e:
        colored_tags_count = pd.DataFrame()
    tags_count_final = colored_tags_count

    st.dataframe(
        tags_count_final,
        column_config={
            "clarification_progress": st.column_config.ProgressColumn(
            "clarification_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        },

        hide_index=True,
        use_container_width=True
        )



    st.divider()

    


with tab2:





    st.write("# at a glance")


    st.write('## your activities')

    today = datetime.datetime.now()
    this_week_begin = today - datetime.timedelta(days=today.weekday())

    start,end = st.date_input(
        "select the desired week:",
        (this_week_begin,today),
        max_value=today,
        format="MM.DD.YYYY"
    )




    with open(active_count_path, 'r') as f:
        active_query=f.read()
    with open(created_count_path, 'r') as f:
        created_count_path=f.read()
    with open(completed_count_path, 'r') as f:
        completed_count_path=f.read()


    active_count = get_table(active_query)
    filtered_active_count = active_count[(active_count['key'] >= pd.to_datetime(start)) & (active_count['key'] <= pd.to_datetime(end))]
    filtered_active_count.sort_values(by=['key'],ascending=True,inplace=True)
    filtered_active_count['group'] = 'active'
    
    # alt_active_count = alt.Chart(filtered_active_count).mark_bar().encode(
    #                     x=alt.X('day_of_year', sort=None, title="Day of week"),
    #                     y=alt.Y('tasks_active', title="Count"),
    #                 )


    created_count = get_table(created_count_path)
    filtered_created_count = created_count[(created_count['key'] >= pd.to_datetime(start)) & (created_count['key'] <= pd.to_datetime(end))]
    filtered_created_count.sort_values(by=['key'],ascending=True,inplace=True)
    filtered_created_count['group'] = 'created'

    # alt_created_count = alt.Chart(filtered_created_count).mark_bar().encode(
    #                     x=alt.X('day_of_year', sort=None, title="Day of week"),
    #                     y=alt.Y('tasks_created', title="Count"),
    #                 )


    completed_count = get_table(completed_count_path)
    filtered_completed_count = completed_count[(completed_count['key'] >= pd.to_datetime(start)) & (completed_count['key'] <= pd.to_datetime(end))]
    filtered_completed_count.sort_values(by=['key'],ascending=True,inplace=True)
    filtered_completed_count['group'] = 'completed'
    # alt_completed_count = alt.Chart(filtered_completed_count).mark_bar().encode(
    #                     x=alt.X('day_of_year', sort=None, title="Day of week"),
    #                     y=alt.Y('tasks_completed', title="Count"),
    #                 )

    

    melted_active_count = filtered_active_count.melt(id_vars=['key', 'group','day_of_year'], value_vars=['tasks_active'], var_name='task_type', value_name='count')
    melted_created_count = filtered_created_count.melt(id_vars=['key', 'group','day_of_year'], value_vars=['tasks_created'], var_name='task_type', value_name='count')
    melted_completed_count = filtered_completed_count.melt(id_vars=['key', 'group','day_of_year'], value_vars=['tasks_completed'], var_name='task_type', value_name='count')
    activities = pd.concat([melted_active_count, melted_created_count, melted_completed_count], ignore_index=True)

    # base color  "#6281c3",
    # Define a color dictionary
    color_dict = {
        "active": "orange", # base color
        "created":  "red",
        "completed": "#6281c3" 
    }

    activities_bar = alt.Chart(activities).mark_bar().encode(
    x=alt.X('day_of_year:N',sort=None, title="Day of week"),
    y=alt.Y('count:Q', title="Count"),
    xOffset="group:N",
    # color="group:N",
    color=alt.Color("group:N", scale=alt.Scale(domain=list(color_dict.keys()), range=list(color_dict.values()))),
    )

    active_line = alt.Chart(melted_active_count).mark_line(color='orange').transform_window(
    # The field to average
    rolling_mean='mean(count)',
    # The number of values before and after the current value to include.
    frame=[-5, 0]
    ).encode(
    x=alt.X('day_of_year:N',sort=None, title="Day of week"),
    y=alt.Y('rolling_mean:Q',title="active_average")
    )

    created_line = alt.Chart(melted_created_count).mark_line(color='red').transform_window(
    # The field to average
    rolling_mean='mean(count)',
    # The number of values before and after the current value to include.
    frame=[-5, 0]
    ).encode(
    x=alt.X('day_of_year:N',sort=None, title="Day of week"),
    y=alt.Y('rolling_mean:Q',title="created_average")
    )

    completed_line = alt.Chart(melted_completed_count).mark_line(color='#6281c3').transform_window(
    # The field to average
    rolling_mean='mean(count)',
    # The number of values before and after the current value to include.
    frame=[-9, 0]
    ).encode(
    x=alt.X('day_of_year:N',sort=None, title="Day of week"),
    y=alt.Y('rolling_mean:Q',title="completed_average")
    )

    
    combo_activities = activities_bar+active_line+created_line+completed_line
    st.write("## trends over week")
    st.altair_chart(combo_activities,use_container_width=True)

    
    st.divider()



    st.write("# lvl1-lvl2 analytics")
    st.write("## progress summary")
    lvl1_lvl2_progress = get_table("select * from lvl1_lvl2_progress")

    filtered_lvl1_lvl2_progress = lvl1_lvl2_progress[lvl1_lvl2_progress['fld_folder_name'].isin(filter_folder)]
    colored_lvl1_lvl2_progress = filtered_lvl1_lvl2_progress.style.map(
        highlight_text,subset=['done_progress','clarify_progress']
    ).apply(
        highlight_row,axis=1
    )
    final_lvl1_lvl2_progress = colored_lvl1_lvl2_progress

    st.dataframe(
        final_lvl1_lvl2_progress,
        column_config={
            "done_progress": st.column_config.ProgressColumn(
            "done_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        "clarify_progress": st.column_config.ProgressColumn(
            "clarify_progress",
            format="%f",
            min_value=0,
            max_value=100
        )
        },

        hide_index=True,
        use_container_width=True
        )




    


with tab3:
    st.write("# lvl3 analytics")
    st.write("## summary")
    lvl3_sumarize = get_table("select * from lvl3_sumarize")
    colored_lvl3_sumarize = lvl3_sumarize.style.map(highlight_text,subset=['lvl3_done_progress'])
    lvl3_sumarize_final = colored_lvl3_sumarize

    st.dataframe(
        lvl3_sumarize_final,
        column_config={
            "lvl3_done_progress": st.column_config.ProgressColumn(
            "lvl3_done_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        },

        hide_index=True,
        use_container_width=True
        )




    st.write("## detailed")
    lvl3_progress = get_table("select * from lvl3_progress")
    colored_lvl3_progress = lvl3_progress.style.map(highlight_text,subset=['lvl3_done_progress','lvl3_clarify_progress','l_done_progress','l_clarify_progress'])
    lvl3_progress_final = colored_lvl3_progress
    st.dataframe(
        lvl3_progress_final,
        column_config={
            "lvl3_done_progress": st.column_config.ProgressColumn(
            "lvl3_done_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        "lvl3_clarify_progress": st.column_config.ProgressColumn(
            "lvl3_clarify_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        "l_done_progress": st.column_config.ProgressColumn(
                "l_done_progress",
                format="%f",
                min_value=0,
                max_value=100
            ),
        "l_clarify_progress": st.column_config.ProgressColumn(
            "l_clarify_progress",
            format="%f",
            min_value=0,
            max_value=100
        ),
        },

        hide_index=True,
        use_container_width=True
        )




