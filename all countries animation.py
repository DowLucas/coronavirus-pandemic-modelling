import numpy as np
import pandas as pd
import plotly.express as px
import os
import json
import commonFuncs


def reconstructData():
    data = json.load(open("Data1/data_new.json", "r"))
    new_data = {}
    # Grouping all countries
    for coun, data_coun in data.items():
        country_dict = {}
        if len(data_coun.keys()) > 1:
            for prov, data_prov in data_coun.items():
                for date, data_case in data_prov.items():
                    if date not in country_dict.keys():
                        country_dict[date] = data_case
                    else:
                        for case_type, d in data_case.items():
                            country_dict[date][case_type] += d

        else:
            country_dict = data_coun["None"]


        new_data[coun] = country_dict

    json.dump(new_data, open("Data1/data_countries_provinces_grouped.json", "w"))

reconstructData()

def getList(country_data, type="Confirmed"):
    l = []
    for key, val in country_data.items():
        l.append(int(val[type]))
    return l

data = json.load(open("Data1/data_countries_provinces_grouped.json", "r"))

df = pd.DataFrame(columns=["x", "y", "con", "t", "date"])

X = []
Y = []
for country in list(data.keys()):
    country_data = data[country]

    dates = list(country_data.keys())
    print(len(dates))

    x = list(commonFuncs.get_cases_per_unit_time(country_data, dates, 7)["Confirmed"].values())
    y = list(commonFuncs.get_new_cases_per_unit_time(country_data, dates, 7)["Confirmed"].values())
    time_pairs = np.array(commonFuncs.getPairPerTime(dates, 7))
    time_pairs = time_pairs[:,1]

    x = np.array(x)
    x[x == 0] = 1

    y = np.array(y)
    y[y == 0] = 1

    print(x, y)

    sub_df = pd.DataFrame(columns=["x", "y", "con", "t", "date"])
    sub_df["x"] = x
    sub_df["y"] = y
    sub_df["con"] = [country for _ in range(len(x))]
    sub_df["t"] = [t for t in range(len(x))]
    sub_df["date"] = time_pairs



    df = pd.concat([sub_df, df], ignore_index=True)


range_x = max(df["x"].values.flatten())*2
range_y = max(df["y"].values.flatten())*2


fig = px.scatter(df, x="x", y="y", hover_name="date", animation_frame="t", log_x=True, log_y=True, text="con", trendline="lowess",
                 range_x=[0.5, range_x], range_y=[0.5, range_y]
   )

fig.show()





