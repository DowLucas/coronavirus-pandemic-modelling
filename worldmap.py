import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
import geopy
from geopy.geocoders import Nominatim
import time
import json

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





df = load_data("COVID19_open_line_list.csv")
df = df[["country", "city", "latitude", "longitude", "travel_history_location"]]
df.dropna(inplace=True)


fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [10, 20, 30],
    lat = [10, 20,30],
    marker = {'size': 10}))


for n, row in df.iterrows():
    lives_in = row["city"]
    travelled_to = row["travel_history_location"]

    if travelled_to not in geo_dict.keys():
        continue

    lives_CORDS = [row["longitude"], row["latitude"]]
    visted_CORDS = geo_dict[travelled_to]

    print(lives_CORDS, visted_CORDS)


    fig.add_trace(go.Scattermapbox(
        mode="markers+lines",
        lon=[lives_CORDS[0], visted_CORDS[1]],
        lat=[lives_CORDS[1], visted_CORDS[0]],
        marker={'size': 10})
    )





fig.show()
