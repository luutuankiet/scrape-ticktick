import streamlit as st
import duckdb
import os
import pandas as pd
from helper.source_env import dbt_project_dir
import datetime
import re

motherduck_token = os.environ.get("motherduck_token")
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()


analytics_path = os.path.join(dbt_project_dir,'analyses')
tags_count_path = os.path.join(analytics_path,'active_tags_count.sql')
loops_count_path = os.path.join(analytics_path,'open_loops_count.sql')
active_count_path = os.path.join(analytics_path,'modified_counts.sql')



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

st.set_page_config(page_title="MY GTD DASHBOARD", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

st.header("🌏 Ken's GTD dashboard",divider="blue")



tab1,tab2,tab3 = st.tabs(['🧑🏽‍💻 daily ops',
         '📊 analytics',
         'placeholder'
         ])


with tab2:


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


    st.write("# at a glance")
    st.write("## count of clarified and next action")




    with open(tags_count_path, 'r') as f:
        tags_query=f.read()

        
    tags_count = get_table_nocache(tags_query)
    colored_tags_count = tags_count.style.map(highlight_text,subset=['clarification_progress'])
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




with tab1:


    with open(loops_count_path, 'r') as f:
        loops_query=f.read()


    loops_count = get_table_nocache(loops_query)
    loops = loops_count['content'].iloc[0]
    lines = loops.split('\n')
    counter = 0
    for line in lines:
        if re.search('[a-z0-9]',line.lower()):
            counter+=1 

    compare_clarify = int(tags_count['cnt_clarifyme'].iloc[0])
    counter_delta = counter - compare_clarify        


    clarifyme_count = tags_count['cnt_clarifyme'].iloc[0]
    clarifyme_avg = 80 # TODO : count average clarifyme across dataset.
    delta_clarifyme = clarifyme_avg - clarifyme_count
    
    
    today_table = get_table_nocache("""
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

                            """)
    overdue_count = today_table[today_table['due_date_id'] < pd.to_datetime(datetime.datetime.now().date())]
    overdue_count = overdue_count['cnt'].iloc[0]

    today_count = today_table[today_table['due_date_id'] == pd.to_datetime(datetime.datetime.now().date())]
    today_count = today_count['cnt'].iloc[0]
    today_avg = 8 # TODO : implement average count over dataset.
    delta_today = today_count - today_avg

    st.write("# your main metrics")
    st.write("*to answer the question, how munch do i have in my head?*")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
          st.metric(
            label="overdue tasks",
            value=overdue_count,
            delta = "reschedule them!!!" if overdue_count > 0 else None,
            delta_color="inverse"
        )
    with col2:
          st.metric(
            label="tasks lined up",
            value=today_count,
            delta = f"{delta_today} than usual {today_avg} tasks",
            delta_color="inverse",
        )

    with col3:
        st.metric(
            "open loops",
            value = counter,
            delta = f"{counter_delta} than clarify",
            delta_color="inverse",
            # help="compared to number of items to clarify"
            )
    with col4:
          st.metric(
            label="Clarifyme count",
            value=clarifyme_count,
            delta=f'{delta_clarifyme} than weekly average {clarifyme_avg}'
        )

    st.write('# active plots')

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


    active_count = get_table(active_query)
    filtered_active_count = active_count[(active_count['key'] >= pd.to_datetime(start)) & (active_count['key'] <= pd.to_datetime(end))]
    st.write('## 1. number of tasks you modified aka *actively working on*')
    st.bar_chart(
        filtered_active_count,
        x='day_of_year',y='tasks_active'
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




