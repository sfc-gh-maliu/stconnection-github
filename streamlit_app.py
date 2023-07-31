import streamlit as st 
from customer_connection import GithubConnection
import pandas as pd
st.set_page_config(layout = 'wide')
conn = st.experimental_connection("github-api", type=GithubConnection)
owner = "streamlit"

st.header("Python Visualization Landscape 🌆")

packages = ['streamlit', 'gradio', 'dash']
col_list = st.columns(len(packages))
for index, package in enumerate(packages):
    #streamlit mentions
    df = conn.search_code(package)
    with col_list[index]:
        st.metric(label = packages[index], value = df['total_count'][0])
        with st.expander("Show top search code results:"):
            st.dataframe(df[['url', 'repository']])

input = st.text_input("Search for code")

df = conn.search_code(input)
st.write(f"Found {df['total_count'][0]} results")
with st.expander("Show top search code results:"):
    st.dataframe(df[['url', 'repository']])
