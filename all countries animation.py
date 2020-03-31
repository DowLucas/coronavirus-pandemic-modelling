import numpy as np
import pandas as pd
import plotly.express as px
import os
import json

data = json.load(open("Data1/data_new.json", "r"))

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











