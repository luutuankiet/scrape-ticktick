#%%
import sys; sys.path.append('/home/ken/dev-main/scrape-ticktick-1/app')
import streamlit as st
import duckdb
import os
import pandas as pd
from helper.source_env import dbt_project_dir
from helper.query_retry import retry
import datetime
from datetime import timedelta, timezone
import re
import altair as alt
import subprocess
import pytz
import humanize
from streamlit_gsheets import GSheetsConnection

#%%
motherduck_token = os.environ.get("motherduck_token")
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()

utc = pytz.timezone('UTC')

# to make date comparison work, 
# 1 create a common timezone. using ecuador gmt-5
# 2 convert date values into tz aware / localize accoding to the specified tz column
# 3 convert the result to the common tz
# 4 every comparison with external dates, always use the external date's timezone aware at the common timezone.
    # ajust the timezone 
common_tz = pytz.timezone('America/Guayaquil')
def convert_row_to_common_tz(row,date_column):
    #create tz aware
    val = row[date_column]
    try:
        tz = pytz.timezone(row['td_timezone'])
    except Exception as e:
        tz = common_tz
    
    tz_aware = pd.to_datetime(val).tz_localize(tz="UTC")
    tz_aware = tz_aware.astimezone(tz)
    # tz_aware =  (tz_aware + timedelta(days=+1)) if tz_aware.hour == 0 and tz_aware.minute == 0 and  tz_aware.tzinfo == 'Asia/Ho_Chi_Minh' else tz_aware
    # fix ticktick bug setting default time of due item wihtout time = 00:00 
    # TODO : handle time conversion for fields already UTC in raw : completedTime, modifiedTime, createdTime
    return tz_aware.astimezone(common_tz)



def convert_df_to_common_tz(df):
    date_columns = df.filter(regex='(date|time)(?!zone)').columns.tolist()
    for col in date_columns:
        try:
            df[col] = df.apply(convert_row_to_common_tz,date_column=col, axis=1)
        except Exception as e:
            pass
    return df



analytics_path = os.path.join(dbt_project_dir,'analyses')
tags_count_path = os.path.join(analytics_path,'active_tags_count.sql')
loops_count_path = os.path.join(analytics_path,'open_loops_count.sql')
active_count_path = os.path.join(analytics_path,'modified_counts.sql')
created_count_path = os.path.join(analytics_path,'created_counts.sql')
completed_count_path = os.path.join(analytics_path,'completed_counts.sql')

st.set_page_config(page_title="MY GTD DASHBOARD", layout="wide", initial_sidebar_state="collapsed", menu_items=None)

st.header("🌏 Ken's GTD dashboard",divider="blue")



# @retry()
@st.cache_data(ttl=datetime.timedelta(hours=24),max_entries=10)
def get_table(query):
    df = cur.sql(query).df()
    df = convert_df_to_common_tz(df)
    return df

# @retry()
def get_table_nocache(query):
    df = cur.sql(query).df()
    df = convert_df_to_common_tz(df)
    return df

with st.expander("server ops"):

    if st.button("force reload server"):
            kill = "tmux send-keys -t streamlit.0 C-c"
            # setup = "cd ../.. && tmux new-session -s $STREAMLIT -d"
            reload = "tmux send-keys -t streamlit.0 'streamlit run main.py' ENTER"
            subprocess.run(f"{kill} & {kill}", shell=True)
            subprocess.run(f"sleep 10 && {reload}",shell=True)
    if st.button("force cache reload"):
            st.cache_data.clear()

    if st.button("reload data"):
            log_path = "/logs/dbt/manual_run_log.txt"
            dbt_cmd = "source /main/scrape-ticktick/.venv/bin/activate && source /main/scrape-ticktick/.env && dagster job execute -m app.ETL.definitions -j ETL_job -d $DAGSTER_HOME"
            
            with open(log_path, "w") as output_file:
                result = subprocess.run(f"{dbt_cmd}", shell=True, stdout=output_file, stderr=subprocess.STDOUT,executable="/bin/bash")

        # Read and display the output file content  
            with open(log_path, "r") as output_file:
                output_content = output_file.read()
            st.code(output_content)




# with st.sidebar:
#     obt=get_table("select * from obt")
#     folders = obt['fld_folder_name'].drop_duplicates().to_list()
#     filter_folder = st.multiselect('folders',folders,default=folders)


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



tab1,tab2,tab3,tab4 = st.tabs(['🧑🏽‍💻 daily ops',
         '📊 analytics',
         'placeholder',
         'lvl3 goals'
         ])



with tab1:
    st.write("# your main metrics")
    st.write("*to answer the question, how munch do i have in my head?*")

    today_table_query = """
                            select 
                            td_title
                            ,td_due_date
                            ,td_repeatFlag
                            ,fld_folder_name
                            ,l_list_name
                            
                            ,* from obt where 
                            completed_date_id is null
                            and l_is_active = '1'
                            and td_kind = 'TEXT'
                            and fld_folder_name not in ('🚀SOMEDAY lists','🛩Horizon of focus','💤on hold lists')
                            and l_list_name not like '%tickler note%'                            
                            and due_date_id is not null 
                            and td_tags not like '%tickler%'
                               
                            """
    today_table = get_table_nocache(today_table_query).reset_index(drop=True)
    st.write(today_table)
    today_clarify_count_df = today_table[(today_table['td_tags'].str.contains('clarifyme')) & 
                                         (today_table['td_title'].str.contains('clarifytoday')) &
                                         ((today_table['td_due_date'].dt.date == pd.Timestamp.now(tz=common_tz).date()) |
                                          (today_table['td_due_date'].dt.date < pd.to_datetime('2020-01-01T00:00:00').date())
                                          )] # for metrics clarifyme


    today_clarify_count =  today_clarify_count_df.shape[0] if today_clarify_count_df.shape[0] > 0 else 0


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

    if tags_count.shape[0] > 0:
        compare_clarify = int(tags_count['cnt_clarifyme'].iloc[0]) 
        clarifyme_count = tags_count['cnt_clarifyme'].iloc[0]
        clarify_progress = tags_count['clarification_progress'].iloc[0]
    else:
        compare_clarify  = 0
        clarifyme_count  = 0
        clarify_progress = 0
        
    counter_delta = counter - compare_clarify        

    clarifyme_avg = 80 # TODO : count average clarifyme across dataset.
    delta_clarifyme =  clarifyme_count - clarifyme_avg
    
    overdue_count_df = today_table[today_table['td_due_date'].dt.date < pd.Timestamp.now(tz=common_tz).date()]

    overdue_count = overdue_count_df.shape[0]

    today_count_df = today_table[today_table['td_due_date'].dt.date == pd.Timestamp.now(tz=common_tz).date()]
    today_count_norepeat_df = today_count_df[today_count_df['td_repeatFlag'] == 'nan']
    today_count_repeat_df = today_count_df[today_count_df['td_repeatFlag'] != 'nan']
    
    today_count_norepeat = today_count_norepeat_df.shape[0]
    today_count_repeat = today_count_repeat_df.shape[0]
    today_count = today_count_norepeat + today_count_repeat


    today_avg = 8 # TODO : implement average count over dataset.
    delta_today = today_count_norepeat - today_avg


    col1,col2,col3,col4 = st.columns(4)
    with col1:
          st.metric(
            label="overdue tasks",
            value=overdue_count,
            delta = "reschedule them!!!" if overdue_count > 0 else "all's well.",
            delta_color="inverse" if overdue_count > 0 else "off",
        )
          with st.expander("query"):
              debug_overdue_count = overdue_count_df
              debug_overdue_count.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True,inplace=True)
              st.dataframe(debug_overdue_count,hide_index=True)


    with col2:
          st.metric(
            label="tasks lined up",
            value=f"{today_count_norepeat} unique | {today_count_repeat} recur",
            delta = f"{delta_today} than usual {today_avg} tasks" if today_count_norepeat > 0 else "all's well.",
            delta_color="inverse" if today_count_norepeat > 0 else "off",
        )
          with st.expander("query"):
              debug_today_count_norepeat_df = today_count_norepeat_df
              debug_today_count_norepeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True,inplace=True)
              
              debug_today_count_repeat_df = today_count_repeat_df
              debug_today_count_repeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True,inplace=True)
              
              st.write("unique today:")
              st.dataframe(debug_today_count_norepeat_df,hide_index=True)
              
              
              st.write("today recurring:")
              st.dataframe(debug_today_count_repeat_df,hide_index=True)

    with col3:
        st.metric(
            "open loops",
            value = counter,
            delta = f"capture them!!! (gap {counter_delta} vs clarify)" if counter > 0 else "all's well.",
            delta_color="inverse" if counter > 0 else "off",
            )
    with col4:
          st.metric(
            label="Clarifyme count",
            value=f"{clarifyme_count} all | {today_clarify_count} clarifytoday",
            delta=f'{delta_clarifyme} than weekly average {clarifyme_avg}' if clarify_progress > 80 else f"clarify them!!! clarification at {clarify_progress}% progress",
            delta_color="inverse" if clarifyme_count > 0 else "off",
        )
          if today_clarify_count > 0:
            with st.expander("query"):
                st.write("clarifytoday count:")
                st.dataframe(today_clarify_count_df,hide_index=True)
          else:
              pass

    st.divider()
    st.write("## look ahead")
    st.write("*what is queued in for the times ahead? give yourself the best chance of completing them in time.*")

    future_count_df = today_table[today_table['td_due_date'].dt.date >= pd.Timestamp.now(tz=common_tz).date()]
    tmr_count_df = future_count_df[(future_count_df['td_due_date'].dt.date <= pd.Timestamp.now(tz=common_tz).date() + datetime.timedelta(days=1))&
                                   (future_count_df['td_due_date'].dt.date > pd.Timestamp.now(tz=common_tz).date())
                                   ]
    tmr_1d_count_df = future_count_df[(future_count_df['td_due_date'].dt.date > pd.Timestamp.now(tz=common_tz).date() + datetime.timedelta(days=1)) &
                                      (future_count_df['td_due_date'].dt.date <= pd.Timestamp.now(tz=common_tz).date() + datetime.timedelta(days=2))
                                      ]
    
    heatmap_count_df = today_table[(today_table['td_due_date'].dt.date >= pd.Timestamp.now(tz=common_tz).date() ) &
                                   (today_table['td_due_date'].dt.date <= pd.Timestamp.now(tz=common_tz).date() + timedelta(days=365)) &
                                   (today_table['td_repeatFlag'] == 'nan')
                                   ]
    
    
    



    col1, col2 = st.columns(2)
    with col1:
        tmr_count_next_norepeat_df = tmr_count_df[(tmr_count_df['td_repeatFlag'] == 'nan') & (~tmr_count_df['td_tags'].str.contains('clarifyme'))]
        tmr_count_clarify_norepeat_df = tmr_count_df[(tmr_count_df['td_repeatFlag'] == 'nan') & (tmr_count_df['td_tags'].str.contains('clarifyme'))]
        tmr_count_repeat_df = tmr_count_df[tmr_count_df['td_repeatFlag'] != 'nan']
        
        
        tmr_count_next_norepeat = tmr_count_next_norepeat_df.shape[0]
        tmr_count_clarify_norepeat = tmr_count_clarify_norepeat_df.shape[0]
        tmr_count_repeat = tmr_count_repeat_df.shape[0]
        tmr_count_norepeat = tmr_count_next_norepeat + tmr_count_clarify_norepeat
        tmr_count = tmr_count_next_norepeat + tmr_count_clarify_norepeat + tmr_count_repeat


        tmr_avg = 12 # TODO : implement average count over dataset.
        delta_tmr = tmr_count_norepeat - tmr_avg
        


        st.metric(
        label="tomorrow's outlook",
        value=f"{tmr_count_next_norepeat} next | {tmr_count_clarify_norepeat} clarify | {tmr_count_repeat} recur",
        delta = f"{delta_tmr} next & clarify more than usual {tmr_avg} tasks" if tmr_count_norepeat > 0 else "all's well.",
        delta_color="inverse" if tmr_count_norepeat > 0 else "off",
    )
        with st.expander("query"):
            debug_tmr_count_next_norepeat_df = tmr_count_next_norepeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            debug_tmr_count_clarify_norepeat_df = tmr_count_clarify_norepeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            debug_tmr_count_repeat_df = tmr_count_repeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            st.write("unique next:")
            st.dataframe(debug_tmr_count_next_norepeat_df,hide_index=True)
            
            st.write("clarify:")
            st.dataframe(debug_tmr_count_clarify_norepeat_df,hide_index=True)
            
            st.write("recurring:")
            st.dataframe(debug_tmr_count_repeat_df,hide_index=True)      
    
    
    with col2:
        
        tmr_1d_count_next_norepeat_df = tmr_1d_count_df[(tmr_1d_count_df['td_repeatFlag'] == 'nan') & (~tmr_1d_count_df['td_tags'].str.contains('clarifyme'))]
        tmr_1d_count_clarify_norepeat_df = tmr_1d_count_df[(tmr_1d_count_df['td_repeatFlag'] == 'nan') & (tmr_1d_count_df['td_tags'].str.contains('clarifyme'))]
        tmr_1d_count_repeat_df = tmr_1d_count_df[tmr_1d_count_df['td_repeatFlag'] != 'nan']
        
        
        tmr_1d_count_next_norepeat = tmr_1d_count_next_norepeat_df.shape[0]
        tmr_1d_count_clarify_norepeat = tmr_1d_count_clarify_norepeat_df.shape[0]
        tmr_1d_count_repeat = tmr_1d_count_repeat_df.shape[0]
        tmr_1d_count_norepeat = tmr_1d_count_next_norepeat + tmr_1d_count_clarify_norepeat
        tmr_1d_count = tmr_1d_count_next_norepeat + tmr_1d_count_clarify_norepeat + tmr_1d_count_repeat


        tmr_1d_avg = 12 # TODO : implement average count over dataset.
        delta_1d_tmr = tmr_1d_count_norepeat - tmr_avg


        st.metric(
        label="day after tomrrow outlook",
        value=f"{tmr_1d_count_next_norepeat} next | {tmr_1d_count_clarify_norepeat} clarify | {tmr_1d_count_repeat} recur",
        delta = f"{delta_1d_tmr} next & clarify more than usual {tmr_1d_avg} tasks" if tmr_1d_count_norepeat > 0 else "all's well.",
        delta_color="inverse" if tmr_1d_count_norepeat > 0 else "off",
    )
        with st.expander("query"):
            debug_tmr_1d_count_next_norepeat_df = tmr_1d_count_next_norepeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            debug_tmr_1d_count_clarify_norepeat_df = tmr_1d_count_clarify_norepeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            debug_tmr_1d_count_repeat_df = tmr_1d_count_repeat_df.sort_values(by=['due_date_id','fld_folder_name','l_list_name'], ascending=True)
            
            st.write("unique next:")
            st.dataframe(debug_tmr_1d_count_next_norepeat_df,hide_index=True)
            
            st.write("clarify:")
            st.dataframe(debug_tmr_1d_count_clarify_norepeat_df,hide_index=True)
            
            st.write("recurring:")
            st.dataframe(debug_tmr_1d_count_repeat_df,hide_index=True)      



    # Group by day of week and count tasks


    st.write("your upcoming **NON-REPEAT** schedule")
    
    heatmap_count_df['day_of_week'] = heatmap_count_df['due_date_id'].dt.strftime('%a')
    heatmap_count_df['month'] = heatmap_count_df['due_date_id'].dt.month_name()
    heatmap_count_df['date'] = heatmap_count_df['due_date_id'].dt.strftime('%Y-%m-%d') # bug: due_date_id somehow gets converted to common tz 2 times. fields parsed from this will get double offset.
    heatmap_count_df['week'] = heatmap_count_df['due_date_id'].dt.strftime('%U')
    heatmap_count_df['month_and_week'] = heatmap_count_df['due_date_id'].dt.strftime('%b - w%U')
    heatmap_count = heatmap_count_df.groupby(['date','due_week_of_year','day_of_week','month','month_and_week']).size().reset_index(name='count')
    
    st.write(heatmap_count_df)
    custom_sort_order = ['Sun','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # Create heatmap using Altair
    heatmap = alt.Chart(heatmap_count).mark_rect().encode(
        x=alt.X('month_and_week:N',sort=None, title='week'),
        y=alt.Y('day_of_week:O',sort=custom_sort_order,title='weekday'),
        color='count:Q',
        tooltip=[
            alt.Tooltip("date:T", title="date"),
            alt.Tooltip("day_of_week:O", title="weekday"),
            alt.Tooltip("count:Q", title="count"),
        ]
    )
    
  
    st.altair_chart(heatmap,use_container_width=True)
    with st.expander("query"):
        debug_future_count_df = heatmap_count_df[['td_title','date','day_of_week','week','due_date_id','fld_folder_name','l_list_name']].sort_values(by='due_date_id', ascending=True)
        st.dataframe(debug_future_count_df,hide_index=True)
    




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

    today = datetime.datetime.now(tz=common_tz)
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

# TODO : conform to UTC time 
        

    active_count = get_table(active_query)
    filtered_active_count = active_count[(active_count['key'] >= pd.to_datetime(start)) & (active_count['key'] <= pd.to_datetime(end))]
    filtered_active_count.sort_values(by=['key'],ascending=True,inplace=True)
    active_count_grouped = filtered_active_count.groupby('day_of_year')['tasks_active'].sum().astype(int)
    active_count_grouped = active_count_grouped.reset_index()
    active_count_grouped['group'] = 'active'
    

    created_count = get_table(created_count_path)
    filtered_created_count = created_count[(created_count['key'] >= pd.to_datetime(start)) & (created_count['key'] <= pd.to_datetime(end))]
    filtered_created_count.sort_values(by=['key'],ascending=True,inplace=True)
    created_count_grouped = filtered_created_count.groupby('day_of_year')['tasks_created'].sum().astype(int)
    created_count_grouped = created_count_grouped.reset_index()
    created_count_grouped['group'] = 'created'


    completed_count = get_table(completed_count_path)
    filtered_completed_count = completed_count[(completed_count['key'] >= pd.to_datetime(start)) & (completed_count['key'] <= pd.to_datetime(end))]
    filtered_completed_count.sort_values(by=['key'],ascending=True,inplace=True)
    completed_count_grouped = filtered_completed_count.groupby('day_of_year')['tasks_completed'].sum().astype(int)
    completed_count_grouped = completed_count_grouped.reset_index()
    completed_count_grouped['group'] = 'completed'

    # for detailed tabular data
    completed_df = filtered_completed_count[['fld_folder_name','l_list_name','tasks_completed','max_day_completed_timestamp','day_of_year']]
    created_df = filtered_created_count[['fld_folder_name','l_list_name','tasks_created','max_day_created_timestamp','day_of_year']]
    active_df = filtered_active_count[['fld_folder_name','l_list_name','tasks_active','max_day_active_timestamp','day_of_year']]


    completed_df.sort_values(by=['max_day_completed_timestamp'],ascending=False,inplace=True)
    created_df.sort_values(by=['max_day_created_timestamp'],ascending=False,inplace=True)
    active_df.sort_values(by=['max_day_active_timestamp'],ascending=False,inplace=True)




    st.write("## lists you have been working on")

    lvl1_lvl2_progress = get_table("select * from lvl1_lvl2_progress")
    # filtered_lvl1_lvl2_progress = lvl1_lvl2_progress[lvl1_lvl2_progress['fld_folder_name'].isin(filter_folder)] # TODO : a way to prevent filter init load stalling the dash
    filtered_lvl1_lvl2_progress = lvl1_lvl2_progress

    
    created_df_delta = created_df
    # created_df_delta['max_day_created_timestamp'] = pd.Timestamp.now(tz=common_tz) - pd.to_datetime(created_df_delta['max_day_created_timestamp']).dt.tz_localize(common_tz)
    created_df_delta['max_day_created_timestamp'] = pd.Timestamp.now(tz=common_tz) - pd.to_datetime(created_df_delta['max_day_created_timestamp'])
    created_df_delta['max_day_created_timestamp'] = created_df_delta['max_day_created_timestamp'].apply(lambda x: humanize.naturaltime(x.total_seconds(),future=False))
    create_progress = pd.merge(created_df_delta,filtered_lvl1_lvl2_progress,on=['fld_folder_name','l_list_name'],how='left')
    
    st.write(create_progress)
    
    create_progress = create_progress.style.map(
        highlight_text,subset=['done_progress','clarify_progress']
    ).apply(
        highlight_row,axis=1
    )


    active_df_delta = active_df
    # active_df_delta['max_day_active_timestamp'] = pd.Timestamp.now(tz=common_tz) - active_df_delta['max_day_active_timestamp'].dt.tz_localize(common_tz)
    active_df_delta['max_day_active_timestamp'] = pd.Timestamp.now(tz=common_tz) - active_df_delta['max_day_active_timestamp']
    active_df_delta['max_day_active_timestamp'] = active_df_delta['max_day_active_timestamp'].apply(lambda x: humanize.naturaltime(x.total_seconds(),future=False))
    active_progress = pd.merge(active_df_delta,filtered_lvl1_lvl2_progress,on=['fld_folder_name','l_list_name'],how='left')
    active_progress = active_progress.style.map(
        highlight_text,subset=['done_progress','clarify_progress']
    ).apply(
        highlight_row,axis=1
    )




    completed_df_delta = completed_df
    # completed_df_delta['max_day_completed_timestamp'] = pd.Timestamp.now(tz=common_tz) - completed_df_delta['max_day_completed_timestamp'].dt.tz_localize(common_tz)
    completed_df_delta['max_day_completed_timestamp'] = pd.Timestamp.now(tz=common_tz) - completed_df_delta['max_day_completed_timestamp']
    completed_df_delta['max_day_completed_timestamp'] = completed_df_delta['max_day_completed_timestamp'].apply(lambda x: humanize.naturaltime(x.total_seconds(),future=False))
    complete_progress = pd.merge(completed_df_delta,filtered_lvl1_lvl2_progress,on=['fld_folder_name','l_list_name'],how='left')
    complete_progress = complete_progress.style.map(
        highlight_text,subset=['done_progress','clarify_progress']
    ).apply(
        highlight_row,axis=1
    )




    col1,col2,col3 = st.columns(3)
    
    avg_days = (abs(start - end) + datetime.timedelta(days=1)).days

    col1.metric("avg completed",value=int(completed_df.groupby('day_of_year')['tasks_completed'].sum().sum() / avg_days) if completed_df_delta.shape[0] > 0 else None,
                delta=f"last item {completed_df_delta.iloc[0,3] }" if completed_df_delta.shape[0] > 0 else None,
                delta_color="off")
    col2.metric("avg created",value=int(created_df.groupby('day_of_year')['tasks_created'].sum().sum() / avg_days) if created_df_delta.shape[0] > 0 else None,
                delta=f"last item {created_df_delta.iloc[0,3]}" if created_df_delta.shape[0] > 0 else None,
                delta_color="off")
    col3.metric("avg active",value=int(active_df.groupby('day_of_year')['tasks_active'].sum().sum() / avg_days) if active_df_delta.shape[0] > 0 else None,
                delta=f"last item {active_df_delta.iloc[0,3] }" if active_df_delta.shape[0] > 0 else None,
                delta_color="off")
    



        
    with st.expander("complete",expanded = False):
        st.dataframe(
            complete_progress,
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



    with st.expander("created",expanded = False):
        st.dataframe(
            create_progress,
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

    with st.expander("active",expanded = False):
        st.dataframe(
            active_progress,
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

    # for graph 


    # TODO : refactor using 3 queries to one cause they use same base except for the datestamp field.
    melted_active_count = active_count_grouped.melt(id_vars=['group','day_of_year'], value_vars=['tasks_active'], var_name='task_type', value_name='count')
    melted_created_count = created_count_grouped.melt(id_vars=['group','day_of_year'], value_vars=['tasks_created'], var_name='task_type', value_name='count')
    melted_completed_count = completed_count_grouped.melt(id_vars=['group','day_of_year'], value_vars=['tasks_completed'], var_name='task_type', value_name='count')
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
    frame=[-5, 0]
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


with tab4:
    goal_index_query = "select * from init_duckdb__lvl3"
    goal_index = get_table(goal_index_query)

    list_index_query = """select
                                fld_folder_name,
                                l_list_name,
                                '' as goal_ids
                            from lvl1_lvl2_progress"""
    
    list_index = get_table(list_index_query)
    st.write(goal_index,list_index,hide_index=True)
    
    conn = st.connection("gsheets",type=GSheetsConnection)
    
    
    
    og_goals = conn.read()
    edited_goals = st.data_editor(og_goals,num_rows="dynamic",hide_index=True)

    if st.button("commit"):
        conn.update(data=edited_goals)
        og_goals = conn.read()
    