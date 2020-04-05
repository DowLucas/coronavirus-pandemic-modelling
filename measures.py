import pandas as pd
from collections import Counter
import json
import pycountry
from graph_data import *


def checkMeasuredUsed(df, country_code, measures):
    
    con_df = df.loc[df["Country Code"] == country_code]
    con_df["Measures"].replace("No new mitigation", np.nan, inplace=True)
    con_df.dropna(inplace=True)
    print(con_df["Measures"])

    loc_df = con_df.loc[con_df["Measures"].str.contains('|'.join(measures))]
    print(loc_df)
    return loc_df if len(loc_df) >= 1 else False
    
def graphGrowthRateWithMitigations(df, country_code, measures):
    df = checkMeasuredUsed(df, country_code, measures)
    print(type(df))
    if type(df) == bool:
        print("Nothing for mitigation found")
        return False

    country = pycountry.countries.get(alpha_3=country_code)
    country = country.name
    print(country)

    growth_data = graph_data.getGrowthData()


if __name__ == "__main__":
    df = pd.read_csv("Data1/mitigation_date_data.csv")
    df.drop(columns=["Unnamed: 0"], inplace=True)
    graphGrowthRateWithMitigations(df, "SWE", ["gathering"])


