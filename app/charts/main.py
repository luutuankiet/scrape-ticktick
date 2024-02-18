from click import style
import streamlit as st
import pandas as pd
import duckdb
import os

motherduck_token = os.environ.get("motherduck_token")
con = duckdb.connect(f'md:ticktick_gtd?motherduck_token={motherduck_token}')
cur = con.cursor()

def highlight_low_val(val):
    if val < 20:
        color = 'red' 
    elif val < 80:
        color = 'yellow'
    # elif val < 75:
    #     color = 'orange'
    elif val == 100:
        color = 'green'
    else: 
        color = ''
    return f'background-color: {color}'


try:
    st.write("## clarify / done progress for lists")
    lvl1_lvl2_progress = cur.query("select * from lvl1_lvl2_progress").df()
    df=lvl1_lvl2_progress
    # df=df.style.map(highlight_low_val,subset=['done_progress','clarify_progress'])
    st.dataframe(
        df,
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


finally:
    cur.close()
    con.close()
