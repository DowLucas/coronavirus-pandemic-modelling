import numpy as np
import pandas as pd
import plotly.express as px
import os
import json
import commonFuncs


def reconstructData():
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

def getList(country_data, type="Confirmed"):
    l = []
    for key, val in country_data.items():
        l.append(int(val[type]))
    return l

data = json.load(open("Data1/data_countries_provinces_grouped.json", "r"))

test_data = data["Sweden"]

dates = list(test_data.keys())

x = list(commonFuncs.get_cases_per_week(test_data, dates)["Confirmed"].values())
y = getList(test_data)[:-1]

print(x, y)

fig = px.scatter(
    x=x,
    y=y
)


fig.update_layout(xaxis_type="log", yaxis_type="log")
fig.show()







