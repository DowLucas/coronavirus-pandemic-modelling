import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import geopy
from geopy.geocoders import Nominatim
import time
import json
import chart_studio
import chart_studio.plotly as py
geo = Nominatim(user_agent="Lucas")


direc = "Data1"


def load_data(file):
    return pd.read_csv(os.path.join(direc, file))

def getSetOfLocations(df):
    locations = df["travel_history_location"].values
    locations = set(locations)

    geo = Nominatim(user_agent="Lucas")
    geo_dict = {}

    for loc in locations:
        time.sleep(1)
        print(loc)
        geoLocation = geo.geocode(loc)
        if geoLocation:
            print(geoLocation.address)

            geo_dict[loc] = [geoLocation.latitude, geoLocation.longitude]

    json.dump(geo_dict, open("geo_dict.json", "w"))



def loadGeoDict():
    return json.load(open("geo_dict.json", "r"))

geo_dict = loadGeoDict()

print(geo_dict)

username = "lucasdow1"
api_key = "ZPnqzLjN0g7VMZX2R16C"
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)


df = load_data("COVID19_open_line_list.csv")
df = df[["country", "city", "latitude", "longitude", "travel_history_location"]]
df.dropna(inplace=True)



df_tavel = df[["latitude", "longitude", "travel_history_location"]]

values = df_tavel.values


travel_dict = {}
count_dict = {}
for val in values:
    if val[2] not in travel_dict.keys():
        travel_dict[val[2]] = val[:2]
        count_dict[val[2]] = 5
    else:
        count_dict[val[2]] += 1
print(travel_dict)
print(count_dict)


fig = go.Figure()


for city, value in travel_dict.items():


    if city not in geo_dict.keys():
        continue

    lives_CORDS = value
    visted_CORDS = geo_dict[city]

    print(lives_CORDS, visted_CORDS)


    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=[lives_CORDS[1], visted_CORDS[1]],
        lat=[lives_CORDS[0], visted_CORDS[0]],
        marker={'size': count_dict[city] if count_dict[city] < 30 else 30},
        text=city,
    ))


fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "carto-positron",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1,
    })


fig.show()

py.plot(fig, filename="test", auto_open=True)
