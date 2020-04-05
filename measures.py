import pandas as pd
from collections import Counter
import json, time
import pycountry
import graph_data
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import commonFuncs

def checkMeasuredUsed(df, country_code, measures):

    con_df = df.loc[df["Country Code"] == country_code]
    con_df["Measures"].replace("No new mitigation", np.nan, inplace=True)
    con_df.dropna(inplace=True)

    loc_df = con_df.loc[con_df["Measures"].str.contains('|'.join(measures))]
    loc_df["Measures"] = commonFuncs.removeMeasureDividers(loc_df["Measures"].values)
    assert len(loc_df) >= 1, Exception("Length of migationtion DataFrame is 0, Mitigation taken by {}:\n{}".format(country_code, con_df["Measures"].values))
    print(loc_df["Measures"].values)
    
    return loc_df


def getGrowthDataFromCountryCode(country_code):
    country = pycountry.countries.get(alpha_3=country_code)
    if not country:

        raise Exception("Country Not Found")
    country = commonFuncs.countryConvert(country.name)

    growth_data = graph_data.getGrowthData(country)
    return growth_data

def graphGrowthRateWithMitigations(df, country_code, measures):
    loc_df = checkMeasuredUsed(df, country_code, measures)

    growth_data = getGrowthDataFromCountryCode(country_code)
    if growth_data == False:
        raise Exception("Country {} not found in dateset, countries:\n{}".format(country_code, set(df["Country Code"])))
    else:
        growth_data = growth_data["Confirmed"]
    
    Xs = list(growth_data.keys())
    Ys = np.array(list(growth_data.values()))

    Ys = np.trim_zeros(Ys)
    Xs = list(map(lambda x: x.split("-")[1], Xs[len(Xs)-len(Ys):]))

    assert len(Xs) == len(Ys)

    plt.plot([x for x in range(len(Ys))], Ys)
    plt.scatter([x for x in range(len(Ys))], Ys, c="black", alpha=0.5)
    plt.grid(True)
    plt.xticks(ticks=[_ for _ in range(len(Xs))], labels=[x for x in Xs], rotation=90)


    colors = ["k", "r"]
    cn = 0
    for n, row in loc_df.iterrows():
        date = commonFuncs.convertTimeFormat(row["Date"], "%b %d, %Y", "%Y/%m/%d")
        if date not in Xs:
            continue

        measure = row["Measures"]

        x_line = Xs.index(date)-1
        plt.axvline(x_line, color=colors[cn%2], label=measure, alpha=0.5, linestyle="--")
        cn+=1
    
    plt.legend(title="Mitigation measures in order of implementation")
    plt.title("Growth Rate of confirmed cases over time including mitigations taken by {}".format(commonFuncs.countryCodeConver(country_code)))
    plt.ylabel("Growth Rate")
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv("Data1/mitigation_date_data.csv")
    df.drop(columns=["Unnamed: 0"], inplace=True)
    graphGrowthRateWithMitigations(df, "NOR", [])



