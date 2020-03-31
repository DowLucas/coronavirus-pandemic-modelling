import pandas as pd
import numpy as np
import json
import os
import pycountry
from tqdm import tqdm
import plotly.graph_objs as go
import plotly.express as px
from generate_data_new import CountryDict

directory = "Data1"

# Number of measures taken by date


def load_csv(file):
    return pd.read_csv(os.path.join(directory, file))

def load_json(file):
    return json.load(open(os.path.join(directory, file), "r"))

df = load_csv("COVID 19 Containment measures data.csv")

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



from datetime import date, timedelta, datetime
import time



def getAllDates(data=None, format=None):
    if data == None:
        data = load_json("mitigation_data.json")
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
    if format:
        return list(map(lambda x: datetime.strftime(x, format), dates))
    else:
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
    data = load_json("mitigation_data.json")
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


    df.to_csv("Data1/mitigation_date_data.csv")

#make_data()

def load_mitigation_date_data(fp):
    return pd.read_csv(fp)




def make_animation2(scope="world"):
    data = load_json("mitigation_data.json")
    dates = getAllDates(data)
    df = load_csv("mitigation_date_data.csv")
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

#make_animation2()


def convertDateFormat(date, format):
    t = time.mktime(datetime.strptime(date, "%b %d, %Y").timetuple())
    new_date = datetime.utcfromtimestamp(t).strftime(format)
    return new_date





def quantize_mitigations(measures):
    df = pd.DataFrame(columns=["Strategy"])

    df["Strategy"] = list(measures.keys())
    print(df.head())


def date_implemented(country_code):
    df = load_csv("mitigation_date_data.csv")
    df_country = df.loc[df["Country Code"] == country_code]
    df_country_and_measures = df_country.loc[df["Measures"] != "No new mitigation"].drop(columns=["Unnamed: 0"], axis=1)
    dates = getAllDates(format="%Y/%m/%d")

    print(df_country_and_measures.head(), df_country_and_measures.columns)

    data = load_json("data_new.json")
    countries = list(data.keys())
    cd = CountryDict(countries)
    country_name = cd.countrycodeToCountry[country_code]

    country_data = data[country_name]
    provinces = country_data.keys()

    values_to_remove = []

    Y = np.empty((len(provinces), len(dates), 3), dtype=np.int32)

    #print(country_dates, dates)

    for i, province in enumerate(provinces):
        province_data = country_data[province]
        data_dates = list(province_data.keys())
        val_remove = 0
        while dates[-1] != data_dates[-1]:
            val_remove += 1
            dates.pop(-1)
        values_to_remove.append(val_remove)
        for j, date in enumerate(dates):
            if date not in data_dates:
                Y[i][j] = [0,0,0]
            else:
                Y[i][j] = [x for x in province_data[date].values()]

    print(dates)
    for n, N in enumerate(values_to_remove):
        Y = Y[n][:-N]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=Y[:,0],
            mode='lines+markers',
            name="Confirmed Cases",
            text=df_country["Date"]
        )
    )
    fig.add_trace(
        go.Scatter(
            y=Y[:,1],
            mode='lines+markers',
            name="Confirmed Deaths",
        )
    )
    fig.add_trace(
        go.Scatter(
            y=Y[:,2],
            mode='lines+markers',
            name="Confirmed Recoveries",
        )
    )



    height_of_lines = max(Y.flatten())
    lines_X = [dates.index(convertDateFormat(row["Date"], format="%Y/%m/%d")) for n, row in df_country_and_measures.iterrows()]


    for n, row in df_country_and_measures.iterrows():
        date = convertDateFormat(row["Date"], format="%Y/%m/%d")
        x = dates.index(date)
        fig.add_shape(
            dict(
                type="line",
                x0=x,
                y0=0,
                x1=x,
                y1=height_of_lines,
                line=dict(
                    color="RoyalBlue",
                    width=2,
                    dash="dot",
                )
            ))

    fig.update_shapes(dict(xref='x', yref='y'))
    fig.show()

#date_implemented("ITA")









