import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go

class PopulationExtract:
    dir = "populationData"
    def __init__(self, file):
        self.df = pd.read_csv(os.path.join(self.dir, file))
        print(self.df.head())

    def getCountryPopulationData(self, country, year=2018):
        df = self.df.loc[(self.df["Country Name"] == country)]
        return int(df[str(year)].values[0])

pe = PopulationExtract("API_SP.POP.TOTL_DS2_en_csv_v2_887275.csv")
pop = pe.getCountryPopulationData("Italy")
data = {'2020/01/22': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/23': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/24': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/25': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/26': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/27': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/28': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/29': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/30': {'Confirmed': 0, 'Deaths': 0, 'Recovered': 0}, '2020/01/31': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/01': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/02': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/03': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/04': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/05': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/06': {'Confirmed': 2, 'Deaths': 0, 'Recovered': 0}, '2020/02/07': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/08': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/09': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/10': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/11': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/12': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/13': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/14': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/15': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/16': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/17': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/18': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/19': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/20': {'Confirmed': 3, 'Deaths': 0, 'Recovered': 0}, '2020/02/21': {'Confirmed': 20, 'Deaths': 1, 'Recovered': 0}, '2020/02/22': {'Confirmed': 62, 'Deaths': 2, 'Recovered': 1}, '2020/02/23': {'Confirmed': 155, 'Deaths': 3, 'Recovered': 2}, '2020/02/24': {'Confirmed': 229, 'Deaths': 7, 'Recovered': 1}, '2020/02/25': {'Confirmed': 322, 'Deaths': 10, 'Recovered': 1}, '2020/02/26': {'Confirmed': 453, 'Deaths': 12, 'Recovered': 3}, '2020/02/27': {'Confirmed': 655, 'Deaths': 17, 'Recovered': 45}, '2020/02/28': {'Confirmed': 888, 'Deaths': 21, 'Recovered': 46}, '2020/02/29': {'Confirmed': 1128, 'Deaths': 29, 'Recovered': 46}, '2020/03/01': {'Confirmed': 1694, 'Deaths': 34, 'Recovered': 83}, '2020/03/02': {'Confirmed': 2036, 'Deaths': 52, 'Recovered': 149}, '2020/03/03': {'Confirmed': 2502, 'Deaths': 79, 'Recovered': 160}, '2020/03/04': {'Confirmed': 3089, 'Deaths': 107, 'Recovered': 276}, '2020/03/05': {'Confirmed': 3858, 'Deaths': 148, 'Recovered': 414}, '2020/03/06': {'Confirmed': 4636, 'Deaths': 197, 'Recovered': 523}, '2020/03/07': {'Confirmed': 5883, 'Deaths': 233, 'Recovered': 589}, '2020/03/08': {'Confirmed': 7375, 'Deaths': 366, 'Recovered': 622}, '2020/03/09': {'Confirmed': 9172, 'Deaths': 463, 'Recovered': 724}, '2020/03/10': {'Confirmed': 10149, 'Deaths': 631, 'Recovered': 724}, '2020/03/11': {'Confirmed': 12462, 'Deaths': 827, 'Recovered': 1045}, '2020/03/12': {'Confirmed': 12462, 'Deaths': 827, 'Recovered': 1045}, '2020/03/13': {'Confirmed': 17660, 'Deaths': 1266, 'Recovered': 1439}, '2020/03/14': {'Confirmed': 21157, 'Deaths': 1441, 'Recovered': 1966}, '2020/03/15': {'Confirmed': 24747, 'Deaths': 1809, 'Recovered': 2335}, '2020/03/16': {'Confirmed': 27980, 'Deaths': 2158, 'Recovered': 2749}, '2020/03/17': {'Confirmed': 31506, 'Deaths': 2503, 'Recovered': 2941}, '2020/03/18': {'Confirmed': 35713, 'Deaths': 2978, 'Recovered': 4025}, '2020/03/19': {'Confirmed': 41035, 'Deaths': 3405, 'Recovered': 4440}, '2020/03/20': {'Confirmed': 47021, 'Deaths': 4032, 'Recovered': 4440}, '2020/03/21': {'Confirmed': 53578, 'Deaths': 4825, 'Recovered': 6072}, '2020/03/22': {'Confirmed': 59138, 'Deaths': 5476, 'Recovered': 7024}, '2020/03/23': {'Confirmed': 63927, 'Deaths': 6077, 'Recovered': 7024}, '2020/03/24': {'Confirmed': 69176, 'Deaths': 6820, 'Recovered': 8326}, '2020/03/25': {'Confirmed': 74386, 'Deaths': 7503, 'Recovered': 9362}, '2020/03/26': {'Confirmed': 80589, 'Deaths': 8215, 'Recovered': 10361}}


arr = []
for n, key in enumerate(data.keys()):
    infected = data[key]["Confirmed"]
    removed = (data[key]["Recovered"]+data[key]["Deaths"])
    suceptible = pop - (removed)
    infected -= (removed)
    arr.append([suceptible, infected, removed])

arr = np.array(arr)
print(arr)

fig = go.Figure(data=[
    go.Bar(name="Infected", x=np.arange(len(arr)), y=arr[:, 1], hovertext=[f"{x} Infected" for x in arr[:, 1]]),
    #go.Bar(name="Susceptible", x=np.arange(len(arr)), y=arr[:,0], hovertext=[f"{x} Susceptible" for x in arr[:,0]]),
    go.Bar(name="Removed", x=np.arange(len(arr)), y=arr[:, 2], hovertext=[f"{x} Removed" for x in arr[:,2]])
])

fig.update_layout(barmode='stack', bargap=0)
fig.show()