import numpy as np
import pandas as pd
import json
from commonFuncs import *

def getGrowthData(country):
    reconstructData()
    data = json.load(open("Data1/data_countries_provinces_grouped.json", "r"))
    
    if country not in data.keys():  
        return False
    
    country_data = data[country]
    dates = list(country_data.keys())
    doubling_data = get_doubling_data(country_data, dates)
    return doubling_data

if __name__ == "__main__":
    getGrowthData("Sweden")
