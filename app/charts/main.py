from click import style
import streamlit as st
import pandas as pd
import duckdb
import os
from helper.source_env import dbt_models_path

motherduck_token = os.environ.get("motherduck_token")
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()

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

obt=cur.sql("select * from obt").df() 


with st.sidebar:
    folders = obt['fld_folder_name'].drop_duplicates().to_list()
    filter_folder = st.multiselect('folders',folders,default=folders)


st.write("# at a glance")
st.write("## count of clarified and next action")


analytics_path = os.path.join(dbt_models_path,'analytics')
tags_count_path = os.path.join(analytics_path,'active_tags_count.sql')


with open(tags_count_path,'r') as f:
    query = f.read()
    tags_count = cur.sql(query).df()
    
    st.dataframe(
        tags_count,
        column_config={
            "weight_clarifyme": st.column_config.ProgressColumn(
            "weight_clarifyme",
            format="%f",
            min_value=0,
            max_value=100
        ),
        "weight_next_action": st.column_config.ProgressColumn(
            "weight_next_action",
            format="%f",
            min_value=0,
            max_value=100
        )
        },

        hide_index=True,
        use_container_width=True
        )




st.write("# lvl1-lvl2 analytics")
st.write("## progress summary")
lvl1_lvl2_progress = cur.query("select * from lvl1_lvl2_progress").df()

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



st.write("# lvl3 analytics")
st.write("## summary")
lvl3_sumarize = cur.query("select * from lvl3_sumarize").df()
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
lvl3_progress = cur.query("select * from lvl3_progress").df()
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