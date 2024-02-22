import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data (replace with your actual data)
data = {'day_of_year': ['2022-01-01', '2022-01-02', '2022-01-03'],
        'tasks_created': [10, 15, 20],
        'tasks_modified': [5, 10, 15],
        'tasks_completed': [2, 8, 12]}

df = pd.DataFrame(data)

# Convert 'day_of_year' to datetime for proper plotting
df['day_of_year'] = pd.to_datetime(df['day_of_year'].date())

# Streamlit App
st.title('Activity Counts Over Time')

# Line Chart
st.area_chart(df.set_index('day_of_year'))

# Data Table (optional)
st.write("Activity Data:")
st.dataframe(df)

# You can add more Streamlit components, sliders, date pickers, etc., for interactivity

# # Show the app
# st.show()
