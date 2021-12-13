import streamlit as st
import Airpoll
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import altair as alt
from PIL import Image


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

title = '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 22px;">Air pollution in NYC  </p>'
sidebarTitle = '<p style="font-family:Palatino, URW Palladio L, serif; color:#465fab; font-size: 22px;">Data</p>'
FPM = '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 15px;">Fine Particulate Matter (PM2.5) :  Fine particles are released by automobiles, building boilers, and other forms of combustion, and are a major source of air pollution that impacts human health.</p>'
ND = '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 15px;">Nitrogen Dioxide (NO2): is a type of pollutant produced by combustion that can harm lung tissue, induce breathing and respiratory issues, and contribute to smog and acid rain.</p>'
SD= '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 15px;">Sulfur Dioxide (SO2):  Sulfur dioxide comes from burning certain types of fuel oil. As an air pollutant, it can can worsen lung diseases. </p>'
OZ= '<p style="font-family:Palatino, URW Palladio L, serif; color:#5184AA; font-size: 15px;">Ozone (O3):  Ozone is a common air pollutant that can harm breathing and worsen asthma and other respiratory conditions.</p>'
poll= '<p style="font-family:Palatino, URW Palladio L, serif; color:#465fab; font-size: 20;">Pollutants</p>'
st.title('Air pollution in NYC 🗽')
st.sidebar.markdown(sidebarTitle, unsafe_allow_html=True)
st.markdown(title, unsafe_allow_html=True)
pollimg = Image.open('pollution.png')

st.image(pollimg, width = 400)





Borough = st.sidebar.selectbox(
    "Data by Location",
    ("New York City","Brooklyn", "Bronx", "Manhattan", 'Staten Island', 'Queens')
)

st.sidebar.markdown(poll, unsafe_allow_html=True)
st.sidebar.markdown(FPM, unsafe_allow_html=True)
st.sidebar.markdown(ND, unsafe_allow_html=True)
st.sidebar.markdown(SD, unsafe_allow_html=True)
st.sidebar.markdown(OZ, unsafe_allow_html=True)

image = Image.open('Lung.png')

st.sidebar.image(image)

st.write('Python Libaries such as pandas,  numpy,  pyplot were used to analyze and depict the Emergency Asthma Hospitalizations of children aged 0 to 17 from 2009 to 2015 in NYC, as well as the amount of pollutants in the air during the same time period.')


if Borough == "New York City":
    df = Airpoll.asth
    st.code('import pandas as pd\nasthmadata = pd.read_csv(\'Asthma_Emergency_Department_Visits.csv\')')
    st.write(Borough + ' Data')
    st.dataframe(df.head(10))
    st.write('\nDisplaying map of Asthma Emergency Department Visits in NYC areas from year 2009-2015')
    fig = Airpoll.asthmamap(df)

    st.write(fig)
    pie = Airpoll.nycpie()
    st.write(pie)
else:
    df = Airpoll.Boroughdata(Borough)
    st.code('import pandas as pd\nairdata = pd.read_csv(\'Air_Quality.csv\')')
    st.write(Borough + ' sData')
    st.dataframe(df.head(10))
    st.write('Map of Pollution values in ' + Borough + ' according to area: ')
    y = Airpoll.Bmap(df)
    st.write(y)

    Y = '<p style="font-family:Palatino, URW Palladio L, serif; color:#0E715F; font-size: 22px;">Select Year</p>'
    st.markdown(Y, unsafe_allow_html=True)

    Year = st.slider("Year",min_value= 2009, max_value = 2015, step = 1)


    fig = Airpoll.Piech(str(Year), df, Borough)
    st.write(fig)




dataused = '<p style="font-family:Palatino, URW Palladio L, serif; color:#465fab; font-size: 19px;">Data and Resources Used</p>'
st.markdown(dataused, unsafe_allow_html=True)
st.write('[Air Quality Data from NYC Open Data](https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r)')
st.write('[Asthma Emergency Department Visits from Citizen’s commute for children of New York](https://data.cccnewyork.org/data/table/6/asthma-emergency-department-visits#6/9/22/a/a)')
