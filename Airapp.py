import streamlit as st
import Airpoll
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import altair as alt

st.set_page_config(
     page_title="Air Pollution in NYC",
     page_icon="chart_with_upwards_trend",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

title = '<p style="font-family:Palatino, URW Palladio L, serif; color:#0E715F; font-size: 22px;">Air pollution in NYC  </p>'
sidebarTitle = '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 22px;">Data</p>'

st.title('Air pollution in NYC 🗽')
st.sidebar.markdown(sidebarTitle, unsafe_allow_html=True)
st.markdown(title, unsafe_allow_html=True)




Borough = st.sidebar.selectbox(
    "Pollution by Borough",
    ("Brooklyn", "Bronx", "Manhattan", 'Staten Island', 'Queens')
)

df = Airpoll.Boroughdata(Borough)

st.dataframe(df)

y = Airpoll.Bmap(df)
st.write(y)

Y = '<p style="font-family:Palatino, URW Palladio L, serif; color:#0E715F; font-size: 22px;">Select Year</p>'
st.markdown(Y, unsafe_allow_html=True)

Year = st.selectbox(
    "Year",
    ("2009", "2010", "2011", '2012', '2013', '2014', '2015')
    )

fig = Airpoll.Piech(Year, df)
st.write(fig)
