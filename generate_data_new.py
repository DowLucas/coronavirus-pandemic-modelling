import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import datetime
import time
import pycountry

class CountryDict:
    def __init__(self, countries):
        self.countryToCountrycode = {pycountry.countries.get(country).alpha_3: country for country in countries}
        self.countrycodeToCountry = {country: pycountry.countries.get(country).alpha_3 for country in countries}
        self.countryToidx = {pycountry.countries.get(country).alpha_3: idx for idx, country in enumerate(countries)}
        self.idxToCountry = {idx: pycountry.countries.get(country).alpha_3 for idx, country in enumerate(countries)}


    def getIdx(self, country):
        if len(country) == 3:
            country = self.countryToCountrycode[country]
        return self.countryToidx[country]

    def getCountry(self, index):
        return self.idxToCountry[index]

class DataExtractor():
    def __init__(self, directory, files):
        self.dir = directory
        self.files = files
        
    def load_file(self, case_type):
        file = [x for x in self.files if case_type.lower() in x][0]
        return pd.read_csv(os.path.join(self.dir, file))

    def sameCoulumns(self, df1, df2, df3):
        first_and_second = set(df1) == set(df2)
        second_and_third = set(df2) == set(df3)

        if not first_and_second or not second_and_third:
            raise Exception("Columns not the same")
        else:
            return True

    def clean(self, x):
        return 1

    def create_data(self, case_type):
        df_conf = self.load_file("Confirmed")
        df_death = self.load_file("Deaths")
        df_recov = self.load_file("Recovered")

        df_conf["Province/State"] = df_conf["Province/State"].fillna(value="None")
        df_death["Province/State"] = df_death["Province/State"].fillna(value="None")
        df_recov["Province/State"] = df_recov["Province/State"].fillna(value="None")
        print(df_conf.head())


        self.sameCoulumns(df_conf.columns, df_death.columns, df_recov.columns)

        dates = df_conf.columns[4:]
        all_data = {}

        for n in range(len(df_conf)):
            conf_row = df_conf.loc[n]
            country, province = conf_row["Country/Region"], conf_row["Province/State"]
            print(country, province)

            death_row = df_death.loc[(df_death["Country/Region"] == country) & (df_death["Province/State"] == province)]
            recov_row = df_recov.loc[(df_recov["Country/Region"] == country) & (df_recov["Province/State"] == province)]

            for date in dates:
                confs = conf_row[date].item()
                deaths = death_row[date].item()
                try:
                    recovs = recov_row[date].item()
                except:
                    recovs = 0
                #print(type(confs), type(deaths), type(recovs))
                unix = time.mktime(datetime.datetime.strptime(date, "%m/%d/%y").timetuple())
                date = datetime.datetime.fromtimestamp(unix).strftime("%Y/%m/%d")

                if not country in all_data.keys():
                    all_data[country] = {}

                if not province in all_data[country].keys():
                    all_data[country][province] = {}

                if not date in all_data[country][province].keys():
                    all_data[country][province][date] = {
                        "Confirmed": confs,
                        'Deaths': deaths,
                        'Recovered': recovs,
                    }
        json.dump(all_data, open("Data1/data_new.json","w"), indent=2)



de = DataExtractor("Data1", [x for x in os.listdir("Data1") if "time_series" in x])
de.create_data("Confirmed")
