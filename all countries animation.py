import numpy as np
import pandas as pd
import plotly.express as px
import os
import json
import commonFuncs
import plotly.graph_objects as go



commonFuncs.reconstructData()

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

    x = list(commonFuncs.get_cases_per_unit_time(country_data, dates, 7)["Confirmed"].values())
    y = list(commonFuncs.get_new_cases_per_unit_time(country_data, dates, 7)["Confirmed"].values())
    time_pairs = np.array(commonFuncs.getPairPerTime(dates, 7))
    time_pairs = time_pairs[:,1]

    x = np.array(x)
    x[x == 0] = 1

    y = np.array(y)
    y[y == 0] = 1

    sub_df = pd.DataFrame(columns=["x", "y", "con", "t", "date"])
    sub_df["x"] = x
    sub_df["y"] = y
    sub_df["con"] = [country for _ in range(len(x))]
    sub_df["t"] = [t for t in range(len(x))]
    sub_df["date"] = time_pairs
    df = pd.concat([sub_df, df], ignore_index=True)

# Get top countries
countries = list(data.keys())
tops = []
for con in countries:
    con_max = max(df.loc[df["con"] == con]["x"])
    print(con, con_max)
    tops.append((con, con_max))

top10 = list(sorted(tops, key=lambda x: x[1]))[-10:]
top10countries = list(map(lambda x: x[0], top10))
top10countries.append("Sweden")
print(top10countries)
df = df[df["con"].isin(top10countries)]


range_x = max(df["x"].values.flatten())*2
range_y = max(df["y"].values.flatten())*2


fig = go.Figure()

for con in top10countries:
    xs = df.loc[df["con"] == con]["x"].values
    ys = df.loc[df["con"] == con]["y"].values
    texts = ["" for _ in range(len(xs)-1)]
    texts.append(con)
    print(xs)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines+markers+text", name=con, text=texts
    ))
fig.update_layout(
    title="Log Graph depicting Week Average new cases over total reported cases",
    xaxis_type="log",
    yaxis_type="log",
    yaxis_title="New Confirmed Cases (7 day period)",
    xaxis_title="Total confirmed Cases (7 day period)",
    font = dict(
        family="Roboto",
        size=19,
        color="#000"
    )
)

fig.show()

quit()

fig = px.line(df, x="x", y="y", hover_name="date", color="con", log_x=True, log_y=True, #trendline="lowess",
                 range_x=[0.5, range_x], range_y=[0.5, range_y]
   )

fig.show()





