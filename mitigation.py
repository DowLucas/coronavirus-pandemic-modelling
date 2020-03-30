import pandas as pd
import numpy as np
import json
import os
import difflib
import pycountry


directory = "Data1"


# Number of measures taken by date




def load(file):
    return pd.read_csv(os.path.join(directory, file))


df = load("COVID 19 Containment measures data.csv")

keywords = df["Keywords"]
keywords.dropna(inplace=True)

data = []
from collections import Counter
for kw in keywords:
    for k in kw.split(","):
        data.append(k.lstrip())

measures = Counter(data)

print(df.columns)




def create_json(df, fp):
    data = {}
    for country in set(df["Country"].values):
        if type(country) == float:
            continue
        sub_df = df.loc[df["Country"] == country][["Date Start", "Keywords"]]
        sub_df = sub_df[(sub_df["Date Start"].notna()) & (sub_df["Keywords"].notna())]
        measures_taken = []

        per_day_data = {}

        for date, measure in sub_df[["Date Start" ,"Keywords"]].values:
            for m in measure.split(","):
                measures_taken.append(m.lstrip())

            per_day_data[date] = {"Measures Taken": measures_taken, "Total Measures Taken": len(measures_taken)}

        data[country] = per_day_data
    print(json.dumps(data, indent=2))
    #json.dump(data, open(fp, "w"))



def load_json(fp):
    return json.load(open(fp, "r"))



from datetime import date, timedelta, datetime
import time



def getAllDates(data):
    dates = []
    for country in data.values():
        for k in country.keys():
            t = time.mktime(datetime.strptime(k, "%b %d, %Y").timetuple())
            uniform_date = datetime.utcfromtimestamp(t).strftime("%Y/%m/%d")
            dates.append(uniform_date)

    dates = sorted(dates)
    from_date = dates[0]

    from_date = datetime.strptime(from_date, "%Y/%m/%d")
    today = datetime.today()

    delta = today-from_date

    dates = []
    for i in range(delta.days + 1):
        day = from_date + timedelta(days=i)
        dates.append(day)
    return dates


def fix_country(country):
    if country == "Vietnam":
        country = "Viet Nam"
    if country == "Vatican City":
        country = "Holy See (Vatican City State)"
    if country == "Iran":
        country = "Iran, Islamic Republic of"
    if country == "Russia":
        country = "Russian Federation"
    if country == "Taiwan":
        country = "Taiwan, Province of China"
    if country == "Macedonia":
        country = "North Macedonia"
    if country == "Moldova":
        country = "Moldova, Republic of"
    if country == "South Korea" or country == "North Korea":
        country = "Korea, Democratic People's Republic of"

    return country

print(list(pycountry.countries))
def make_data():
    data = load_json("Data1/mitigation_data.json")
    dates = getAllDates(data)

    df = pd.DataFrame()

    for country in data.keys():
        country = fix_country(country)
        c = country

        country = pycountry.countries.get(name=country)
        if country == None:
            print(c)
            country = pycountry.countries.get(common_name=country)




make_data()

'''
fig = go.Figure(
    data=[go.Choropleth(
    locations = df['CODE'],
    z = df['GDP (BILLIONS)'],
    text = df['COUNTRY'],
    )],
    layout=go.Layout(
        xaxis=dict(range=[0, 5], autorange=False),
        yaxis=dict(range=[0, 5], autorange=False),
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames = [go.Frame(data=go.Choropleth(
    locations = df['CODE'],
    z = df['GDP (BILLIONS)'],
    text = df['COUNTRY'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = 'SEK',
    colorbar_title = 'GDP<br>Millions US$',
    ), layout=go.Layout(title_text="End Title"))],
)

fig2 = go.Figure(
    data=[go.Scatter(x=[0, 1], y=[0, 1])],
    layout=go.Layout(
        xaxis=dict(range=[0, 5], autorange=False),
        yaxis=dict(range=[0, 5], autorange=False),
        title="Start Title",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None])])]
    ),
    frames=[go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])]),
            go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])]),
            go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
                     layout=go.Layout(title_text="End Title"))]
)


'''
