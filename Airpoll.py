import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.io as pio


airdata = pd.read_csv('Air_Quality.csv')

airdata = airdata.drop('Message', 1)
airdata = airdata[(airdata['Name'] == 'Fine Particulate Matter (PM2.5)') |
   (airdata['Name'] == 'Nitrogen Dioxide (NO2)') |
   (airdata['Name'] == 'Ozone (O3)')|
   (airdata['Name'] == 'Sulfur Dioxide (SO2)')]

airdata['Start_Date'] = airdata['Start_Date'].apply(pd.to_datetime)
airdata['Start_Date'] = airdata['Start_Date'].dt.year

airdata.drop(['Time Period', 'Indicator ID', 'Unique ID'], axis=1)
airdata= airdata[(airdata['Start_Date'] <=2015) & (airdata['Start_Date'] >=2009)]
airdata = airdata.rename({'Start_Date': 'TimeFrame', 'Geo Place Name': 'Location', 'Name': 'Pollutant', 'Data Value': 'Mean Pollutant Value'}, axis=1)
airdata = airdata.drop(columns=['Unique ID', 'Indicator ID', 'Measure', 'Time Period'])
airdata = airdata[airdata['Geo Type Name'] == 'CD']



#ASTHMA DATA
asth = pd.read_csv('Asthma_Emergency_Department_Visits.csv')
asth = asth[asth['Age Group'] == '0 to 17 Years']
asth = asth.rename({'Fips': 'Geo Join ID'}, axis=1)
asth = asth[(asth['Location'] != 'Brooklyn')]
asth = asth[(asth['Location'] != 'Bronx')]
asth = asth[(asth['Location'] != 'Queens')]
asth = asth[(asth['Location'] != 'Staten Island')]
asth = asth[(asth['Location'] != 'New York City')]
asth = asth[(asth['Location'] != 'Manhattan')]
asth['Geo Join ID'] = asth['Geo Join ID'].map(lambda x: x.lstrip('uhf'))
asth['Geo Join ID']=asth['Geo Join ID'].astype(int)
asth= asth[(asth['TimeFrame'] <=2015) & (asth['TimeFrame'] >=2009)]
asth = asth.rename(columns={'Data': 'Asthma Emergency Dep. Visits'})

nycb = json.load(open('UHF42.json', 'r'))
Boro_map = {}
for feature in nycb['features']:
    feature['Borough'] = feature['properties']['BOROUGH']
    Boro_map[feature['properties']['GEOCODE']] = feature['Borough']
asth['Borough'] = asth['Geo Join ID'].map(Boro_map)


def Boroughdata(Borough):
    #merg = airdata.merge(asth, on=['Geo Join ID', 'TimeFrame'],how='left')
#     merg = merg.rename(columns={'Data Value': 'Mean Pollution Value', 'Data': 'Asthma Emergency Dep. Visits', 'Location_x': 'Location'})
#     merg= merg.dropna()
    nycb = json.load(open('neigh.json', 'r'))
    Boro_map = {}
    for feature in nycb['features']:
        feature['Borough'] = feature['properties']['BOROUGH']
        Boro_map[feature['properties']['GEOCODE']] = feature['Borough']
    airdata['Borough'] = airdata['Geo Join ID'].map(Boro_map)
    x = airdata[airdata['Borough'] == Borough]
    return x

def Bmap(data):
    nycb = json.load(open('neigh.json', 'r'))
    fig = px.choropleth_mapbox(data, locations='Geo Join ID', geojson=nycb, color='Mean Pollutant Value', hover_name='Location', mapbox_style='carto-positron', center = {'lat':40.681395467965096, 'lon':-73.93646399798689}, zoom=9, opacity = 0.5)
    return fig


def Piech(year, data, Borough):
    df = data.query("TimeFrame == {}".format(year))
    fig = px.pie(df, values='Mean Pollutant Value', names='Pollutant', title=Borough +' Pollutants in ' + year)
    return fig

def asthmamap(asth):
    nyc = json.load(open('boroughsgeojson.json', 'r'))
    Boro = {}
    y = asth.dropna()
    for feature in nyc['features']:
        feature['id'] = feature['properties']['BoroCode']
        Boro[feature['properties']['BoroName']] = feature['id']
    y['BoroughID'] = y['Borough'].apply(lambda x: Boro[x])

    location = 'Geo Join ID'
    geo = nycb
    hover = 'Location'
    fig = px.choropleth_mapbox(y, locations=location, geojson=geo, color='Asthma Emergency Dep. Visits', hover_name=hover, mapbox_style='carto-positron', center = {'lat':40.681395467965096, 'lon':-73.93646399798689}, zoom=8, opacity = 0.5)
    return fig

def nycpie():
    fig = px.pie(airdata, values='Mean Pollutant Value', names='Pollutant', title='Pollutants in NYC')
    return fig
