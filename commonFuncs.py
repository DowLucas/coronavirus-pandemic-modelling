import numpy as np
import json, time
from datetime import datetime
import pycountry

def datePairs(dates):
    date_pairs = []
    for n in np.arange(0, len(dates)-1, 1):
        date_pairs.append((dates[n], dates[n+1]))
        if n == len(dates):
            break
    return date_pairs

def newCasesPerDay(province_data):
    data = {}
    dates = list(province_data.keys())
    for n, date in enumerate(dates):
        if n == 0:
            continue
        data[date] = {}
        for case in province_data[date].keys():
            try:
                data[date][case] = province_data[date][case]-province_data[dates[n-1]][case]
            except:
                pass

    return data



def get_doubling_data(province_data, dates):
    #dates = list(dates.keys())
    cases_per_day = newCasesPerDay(province_data)
    date_pairs = datePairs(dates)
    print(cases_per_day)

    data = {"Confirmed": {}, "Deaths": {}, "Recovered": {}}
    for pair in date_pairs:
        if pair[0] not in cases_per_day.keys():
            continue
        for case_type in cases_per_day[pair[0]].keys():
            try:
                rate_delta = cases_per_day[pair[1]][case_type]/cases_per_day[pair[0]][case_type]
            except Exception:
                rate_delta = 0
            try:
                data[case_type][f"{pair[0]}-{pair[1]}"] = rate_delta
            except:
                continue
    print(data["Confirmed"])
    return data

def get_cases_per_day(province_data, dates):
    date_pairs = datePairs(dates)
    data = {"Confirmed": {}, "Deaths": {}, "Recovered": {}}
    for pair in date_pairs:
        if pair[0] not in province_data.keys():
            continue
        for case_type in province_data[pair[0]].keys():
            new_cases = province_data[pair[1]][case_type]-province_data[pair[0]][case_type]
            try:
                data[case_type][f"{pair[0]}-{pair[1]}"] = new_cases
            except:
                continue
    return data

def getPairPerTime(dates, days):
    d = 0
    while (len(dates[d:])) % (days) != 0:
        dates.pop(0)
    weeks = []
    for n in np.arange(0, len(dates), days):
        if n+1 == len(dates):
            break
        weeks.append([dates[n], dates[(n-1)+days]])
    return weeks

def get_cases_per_unit_time(province_data, dates, days=7):
    weeks = getPairPerTime(dates, days)
    data = {"Confirmed": {}, "Deaths": {}, "Recovered": {}}
    for n, week in enumerate(weeks):
        data["Confirmed"][f"Time {n+1}"] = province_data[weeks[n][-1]]["Confirmed"]
        data["Deaths"][f"Time {n+1}"]  = province_data[weeks[n][-1]]["Deaths"]
        data["Recovered"][f"Time {n+1}"] = province_data[weeks[n][-1]]["Recovered"]
    return data

def get_new_cases_per_unit_time(province_data, dates, days=7):
    weeks = getPairPerTime(dates, days)
    data = {"Confirmed": {}, "Deaths": {}, "Recovered": {}}
    for n, week in enumerate(weeks):
        data["Confirmed"][f"Time {n+1}"] = province_data[weeks[n][1]]["Confirmed"] - province_data[weeks[n][0]]["Confirmed"]
        data["Deaths"][f"Time {n+1}"]  = province_data[weeks[n][1]]["Deaths"] - province_data[weeks[n][0]]["Deaths"]
        data["Recovered"][f"Time {n+1}"] = province_data[weeks[n][1]]["Recovered"] - province_data[weeks[n][0]]["Recovered"]
    return data

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

    json.dump(new_data, open("Data1/data_countries_provinces_grouped.json", "w"), indent=2)


def convertTimeFormat(t, f, to):
    t = time.mktime(datetime.strptime(t, f).timetuple())
    return datetime.utcfromtimestamp(t).strftime(to)

def countryConvert(country):
    if country == "United States":
        return "US"
    
    return country

def removeMeasureDividers(values):
    values = list(map(lambda x: x.replace(" | ", ", ")[:-2], values))
    return values

def countryCodeConver(country_code):
    country = pycountry.countries.get(alpha_3=country_code)
    country = countryConvert(country.name)
    return country

def countryCodeCountryDict(country_codes):
    data = {}
    for code in country_codes:
        c = pycountry.countries.get(alpha_3=code)
        name = c.name
        data[code] = name
    return data