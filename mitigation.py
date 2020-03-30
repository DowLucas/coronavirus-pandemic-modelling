import pandas as pd
import numpy as np
import json
import os
import difflib


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

data = {}


def create_json(df, fp):
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
    json.dump(data, open(fp, "w"))


create_json(df, "Data1/mitigation_data.json")




        
    

