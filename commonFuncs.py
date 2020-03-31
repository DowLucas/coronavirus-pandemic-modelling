import numpy as np

def datePairs(dates):
    date_pairs = []
    for n in np.arange(0, len(dates)-1, 1):
        date_pairs.append((dates[n], dates[n+1]))
        if n == len(dates):
            break
    return date_pairs

def get_doubling_data(province_data, dates):
    #dates = list(dates.keys())

    date_pairs = datePairs(dates)

    data = {"Confirmed": {}, "Deaths": {}, "Recovered": {}}
    for pair in date_pairs:
        if pair[0] not in province_data.keys():
            continue
        for case_type in province_data[pair[0]].keys():
            try:
                rate_delta = province_data[pair[1]][case_type]/province_data[pair[0]][case_type]
            except Exception:
                rate_delta = 0
            try:
                data[case_type][f"{pair[0]}-{pair[1]}"] = rate_delta
            except:
                continue

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