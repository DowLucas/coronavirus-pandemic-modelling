import pandas as pd
from collections import Counter
import json
import pycountry

df = pd.read_csv("Data1/mitigation_date_data.csv")
df.drop(columns=["Unnamed: 0"], inplace=True)
print(df.columns)

def countryInLockdown(df, country_code):
    con_df = df.loc[df["Country Code"] == country_code]
    print(con_df)
    loc_df = con_df.loc[con_df["Measures"].str.contains("distance")]
    print(loc_df)
    
countryInLockdown(df, "USA")