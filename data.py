import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json
from matplotlib.gridspec import GridSpec
from matplotlib import style
import time
import datetime
import cv2
from tqdm import tqdm
from commonFuncs import *

def load_data():
    data = json.load(open("Data1/data_new.json", "r"))
    return data


def get_all_countries(data):
    return data.keys()

def get_date_dict(country_data):
    dates_list = []
    for province in country_data.keys():
        province_data = country_data[province]
        dates = list(province_data.keys())

        for date in dates:
            if date not in dates_list:
                dates_list.append(date)

    dates_list.sort()
    return {date: x for x, date in enumerate(dates_list)}


def get_key(val, d):
    for key, value in d.items():
         if val == value:
             return key

def get_most_case_provinces(country_data):
    all_province_cases = []

    for key, data in country_data.items():
        cases = list(map(lambda date: data[date]["Confirmed"], data.keys()))[-1]
        all_province_cases.append((key, cases))

    all_province_cases.sort(key=lambda x: x[1], reverse=True)

    return list(map(lambda x: x[0], all_province_cases))[:10]


def createVideoAnimation(country, provinces, country_data):
    os.mkdir("animations") if not os.path.exists("animations") else None
    os.mkdir("tmp_images") if not os.path.exists("tmp_images") else None


    for province in provinces:
        province_data = country_data[province]

        dates = list(province_data.keys())
        new_cases = get_cases_per_day(province_data, dates)

        confirmed_cases = np.array(list(map(lambda data: data["Confirmed"], province_data.values())))[:-1]

        for frame in tqdm(range(1, len(confirmed_cases))):
            plt.plot(confirmed_cases[:frame], list(new_cases["Confirmed"].values())[:frame], label=country)
            plt.scatter(confirmed_cases[:frame][-1], list(new_cases["Confirmed"].values())[:frame][-1], s=15, alpha=.2, c="black")

            plt.xscale("log")
            plt.yscale("log")

            plt.xlabel("Total Confirmed Cases")
            plt.ylabel("New Confirmed cases per day")

            plt.legend(title="Province/State")

            plt.grid(True, which="both")

            img_dir = f"tmp_images/{country}_{frame}.png"
            
            plt.savefig(img_dir)
            img = cv2.imread(img_dir)

            #os.remove(img_dir)
            plt.clf()

def changeOfRateGraph(country, provinces, country_data):
    fig = plt.figure(figsize=(10, 5))
    gs = GridSpec(nrows=2, ncols=2)

    ax_casesRate = fig.add_subplot(gs[:, 1])
    ax_deathsRate = fig.add_subplot(gs[0, 0])
    ax_recoveredRate = fig.add_subplot(gs[1, 0])

    for province in provinces:
        province_data = country_data[province]

        dates = list(province_data.keys())
        doubling_data = doubling_data(province_data, dates)

        confirmed_cases = np.array(list(map(lambda data: data["Confirmed"], province_data.values())))[:-1]
        deaths = np.array(list(map(lambda data: data["Deaths"], province_data.values())))[:-1]
        recovered = np.array(list(map(lambda data: data["Recovered"], province_data.values())))[:-1]

        ax_casesRate.plot(confirmed_cases, list(doubling_data["Confirmed"].values()), label=country)
        ax_casesRate.scatter(confirmed_cases, list(doubling_data["Confirmed"].values()), s=15, alpha=.2, c="black")

        ax_deathsRate.plot(deaths, list(doubling_data["Deaths"].values()))
        ax_deathsRate.scatter(deaths, list(doubling_data["Deaths"].values()), s=15, alpha=.2, c="black", label=country)

        ax_recoveredRate.plot(recovered, list(doubling_data["Recovered"].values()))
        ax_recoveredRate.scatter(recovered, list(doubling_data["Recovered"].values()), s=15, alpha=.2, c="black", label=country)


    ax_casesRate.grid(True, which="both")
    ax_deathsRate.grid(True)
    ax_recoveredRate.grid(True)

    plt.show()

def newCaseGraph(country, provinces, country_data):

    fig = plt.figure(figsize=(10, 5))
    gs = GridSpec(nrows=2, ncols=2)

    ax_caseDay = fig.add_subplot(gs[:, 1])
    ax_deathsDay = fig.add_subplot(gs[0, 0])
    ax_recoveredDay = fig.add_subplot(gs[1, 0])

    for province in provinces:
        province_data = country_data[province]

        dates = list(province_data.keys())
        new_cases = get_cases_per_day(province_data, dates)
        print(new_cases)

        confirmed_cases = np.array(list(map(lambda data: data["Confirmed"], province_data.values())))[:-1]
        deaths = np.array(list(map(lambda data: data["Deaths"], province_data.values())))[:-1]
        recovered = np.array(list(map(lambda data: data["Recovered"], province_data.values())))[:-1]

        ax_caseDay.plot(confirmed_cases, list(new_cases["Confirmed"].values()), label=country)
        ax_caseDay.scatter(confirmed_cases, list(new_cases["Confirmed"].values()), s=15, alpha=.2, c="black")

        ax_deathsDay.plot(deaths, list(new_cases["Deaths"].values()))
        ax_deathsDay.scatter(deaths, list(new_cases["Deaths"].values()), s=15, alpha=.2, c="black", label=country)

        ax_recoveredDay.plot(recovered, list(new_cases["Recovered"].values()))
        ax_recoveredDay.scatter(recovered, list(new_cases["Recovered"].values()), s=15, alpha=.2, c="black", label=country)


    ax_caseDay.set_xscale("log")
    ax_caseDay.set_yscale("log")

    ax_deathsDay.set_xscale("log")
    ax_deathsDay.set_yscale("log")

    ax_recoveredDay.set_xscale("log")
    ax_recoveredDay.set_yscale("log")

    ax_caseDay.set_xlabel("Total Confirmed Cases")
    ax_caseDay.set_ylabel("New Confirmed cases per day")

    ax_deathsDay.set_xlabel("Total Deaths")
    ax_deathsDay.set_ylabel("New Deaths per day")

    ax_recoveredDay.set_xlabel("Total Recoveries")
    ax_recoveredDay.set_ylabel("New Recoveries per day")

    ax_caseDay.legend(title="Province/State")

    ax_caseDay.grid(True, which="both")
    ax_deathsDay.grid(True)
    ax_recoveredDay.grid(True)

    plt.show()

def time_graphs(country, provinces, country_data, date_dict, show_log_graph=True):
    fig = plt.figure(figsize=(10, 5))
    gs = GridSpec(nrows=2, ncols=2)

    ax_cases = fig.add_subplot(gs[:, 1])
    ax_deaths = fig.add_subplot(gs[0, 0], sharex=ax_cases)
    ax_recovered = fig.add_subplot(gs[1, 0], sharex=ax_cases)

    #print(json.dumps(country_data, indent=2))
    provinces = country_data.keys()

    for province in provinces:
        province_data = country_data[province]
        print(province_data)

        dates = list(province_data.keys())

        if "," in province:
            continue

        confirmed_cases = np.array(list(map(lambda data: data["Confirmed"], province_data.values())))
        deaths = np.array(list(map(lambda data: data["Deaths"], province_data.values())))
        recovered = np.array(list(map(lambda data: data["Recovered"], province_data.values())))

        # Removing all confirmed dates with 0
        try:
            index = max([n for n, x in enumerate(confirmed_cases) if x == 0])+1
        except:
            index = 0
        confirmed_cases = confirmed_cases[index:] if show_log_graph else confirmed_cases

        xs = [date_dict[date] for date in dates]

        ax_cases.plot(xs[index:] if show_log_graph else xs, confirmed_cases, label=province if province != "None" else country)
        ax_cases.scatter(xs[index:] if show_log_graph else xs, confirmed_cases, alpha=.5, color="black", s=15)

        ax_deaths.plot(xs, deaths, label=province if province != "None" else country)
        ax_deaths.scatter(xs, deaths, alpha=.5, color="black", s=15)

        ax_recovered.plot(xs, recovered, label=province if province != "None" else country)
        ax_recovered.scatter(xs, recovered, alpha=.5, color="black", s=15)

    ticks = [n for n in np.arange(0, len(date_dict), 5)]

    ax_cases.set_xticks(ticks)
    ax_cases.set_xticklabels([get_key(n, date_dict) for n in ticks], rotation=30)
    ax_deaths.set_xticks(ticks)
    ax_deaths.set_xticklabels(["" for n in ticks], rotation=30)
    ax_recovered.set_xticks(ticks)
    ax_recovered.set_xticklabels([get_key(n, date_dict) for n in ticks], rotation=30)

    ax_deaths.axes.get_xaxis().set_visible(False)

    ax_cases.set_title("Confirmed Cases of COVID-19")
    ax_deaths.set_title("Confirmed Deaths of COVID-19")
    ax_recovered.set_title("Confirmed Recoveries of COVID-19", y=-0.1)

    ax_cases.legend(title="State/Province")

    if show_log_graph:
        ax_cases.set_yscale("log")


    ax_cases.grid(True, which="both")
    ax_deaths.grid(True)
    ax_recovered.grid(True)

    ax_recovered.xaxis.tick_top()
    plt.show()


def evaluate_country(country):
    data = load_data()
    countries = get_all_countries(data)
    print(f"There are currently {len(countries)} regions affected by the CoronaVirus")

    assert country in countries

    country_data = data[country]
    date_dict = get_date_dict(country_data)
    provinces = country_data.keys()
    if len(provinces) > 10:
        provinces = get_most_case_provinces(country_data)

    #createVideoAnimation(country, provinces, country_data)
    time_graphs(country, provinces, country_data, date_dict, True)


evaluate_country("Italy")


