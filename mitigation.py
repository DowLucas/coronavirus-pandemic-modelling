import pandas as pd
import numpy as np
import json
import os
import difflib
import pycountry
from tqdm import tqdm
import plotly.graph_objs as go
import chart_studio
import chart_studio.plotly as py


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


def fixUSStates(data):

    US_states = list(filter(lambda k: ":" in k, data.keys()))
    print(US_states)
    US_data = {}

    tmp = []

    for state in US_states:
        for date, measure_data in data[state].items():
            if date not in US_data.keys():
                US_data[date] = measure_data
            else:
                for measure in measure_data["Measures Taken"]:
                    US_data[date]["Measures Taken"].append(measure)

                US_data[date]["Total Measures Taken"] += measure_data["Total Measures Taken"]

        del data[state]
    
    data["USA"] = US_data
    #print(json.dumps(data,  indent=2))
    return data

def create_json(df, fp):
    data = {}
    for country in set(df["Country"].values):
        if type(country) == float:
            continue
        sub_df = df.loc[df["Country"] == country][["Date Start", "Keywords"]]
        sub_df = sub_df[(sub_df["Date Start"].notna()) & (sub_df["Keywords"].notna())]


        per_day_data = {}

        for date, measure in sub_df[["Date Start" ,"Keywords"]].values:
            measures_taken = []
            for m in measure.split(","):
                measures_taken.append(m.lstrip())

            per_day_data[date] = {"Measures Taken": measures_taken, "Total Measures Taken": len(measures_taken)}

        data[country] = per_day_data

    json.dump(data, open(fp, "w"), indent=2)

create_json(df, "Data1/mitigation_data.json")

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
    if country == "USA":
        country = "United States"

    return country




def make_data():
    data = load_json("Data1/mitigation_data.json")
    data = fixUSStates(data)
    #print(json.dumps(data, indent=2))
    dates = getAllDates(data)
    df = pd.DataFrame()

    print(len(list(filter(lambda x: "US" in x, data.keys()))))

    for country in tqdm(data.keys()):
        country_name = country
        country = fix_country(country)

        country = pycountry.countries.get(name=country)


        if country == None:
            continue
        else:
            country_code = country.alpha_3

        if country.name == "United States":
            print(country_name)

        num_measures = 0
        for date in dates:
            measures_on_the_day = 'No new mitigation'

            date = date.strftime("%b %d, %Y")

            if date in data[country_name].keys():
                num_measures += data[country_name][date]["Total Measures Taken"]
                measures_on_the_day = data[country_name][date]["Measures Taken"]
                measures_on_the_day = "".join([m+" | " for m in measures_on_the_day])

            #print(date, num_measures)
            df = df.append({"Country Code": country_code, "Date": date, "Num Measures": num_measures, "Measures": measures_on_the_day}, ignore_index=True)

        #print(df.loc[df["Country Code"] == "USA"]["Num Measures"].values)


    #df.to_csv("Data1/mitigation_date_data.csv")

#make_data()

def load_mitigation_date_data(fp):
    return pd.read_csv(fp)


#make_data()
df = load_mitigation_date_data("Data1/mitigation_date_data.csv")
print(df.loc[df["Country Code"] == "USA"]["Num Measures"].values)
#quit()
def make_animation():
    data = load_json("Data1/mitigation_data.json")
    dates = getAllDates(data)

    print(df.head())

    dates = list(map(lambda date: date.strftime("%b %d, %Y"), dates))

    sdate = dates[0]
    print(sdate)
    test_df = df.loc[df["Date"] == sdate]

    zmax = 50
    zmin = 0
    print(zmax)

    # Create frame data
    frames = []
    for date in dates[1:]:
        df_date = df.loc[df["Date"] == date]
        frames.append(
            go.Frame(data=[go.Choropleth(
                locations=df_date["Country Code"],
                z=df_date["Num Measures"],
                text=df_date["Measures"],
                zmax=zmax,
                zmin=zmin,
                colorscale="aggrnyl",
            )])
        )


    fig = go.Figure(data=[go.Choropleth(
        locations=test_df["Country Code"],
        z=test_df["Num Measures"],
        text=test_df["Measures"],
        zmax=zmax,
        zmin=0,
        colorscale="aggrnyl",
    )],
        layout=go.Layout(
            xaxis=dict(range=[0, 5], autorange=False),
            yaxis=dict(range=[0, 5], autorange=False),
            title="Start Animation",
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                              method="animate",
                              args=[None])])]
        ),
        frames = frames
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        title="Number of measures taken by countries over time"
    )
    fig.show()




def make_animation2(scope="world"):
    data = load_json("Data1/mitigation_data.json")
    dates = getAllDates(data)
    df = load_mitigation_date_data("Data1/mitigation_date_data.csv")
    print(df.head())


    fig = px.choropleth(
        df,
        locations="Country Code",
        color="Num Measures",
        hover_name="Measures",
        animation_frame="Date",
        color_continuous_scale=px.colors.sequential.matter,
        range_color=(0, 50),
        scope=scope
    )
    fig.layout.update(
        title="Number of mitigation measure taken by different countries over time",
        transition={'duration': 5000},
    )
    fig.show()
    #py.plot(fig, filename="mitigation over time", auto_open=True)

make_animation2()

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
