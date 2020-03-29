import numpy as np
import math
from person import Person
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


HEAL_TIME_IN_DAYS = 20
INCUBATION_IN_DAYS = 2

AFFECT_RADIUS = 30
INFECT_CHANCE = 0.001
DAYS = 365
ITERATIONS_PER_DAY = 24
HEAL_ITERATIONS = ITERATIONS_PER_DAY*HEAL_TIME_IN_DAYS
POPULATION = 100
WIDTH = 500
HEIGHT = 500
NO_SYMPTOMS_CHANCE = 0
INCUBATION_ITERATIONS = INCUBATION_IN_DAYS * ITERATIONS_PER_DAY


DATA_COLLECT = []

print(HEAL_ITERATIONS)

class Society():
    def __init__(self, pop_size, width, height):
        self.society_width = width
        self.socity_height = height


        self.population = [Person(0, 0, AFFECT_RADIUS, HEAL_ITERATIONS, INFECT_CHANCE, NO_SYMPTOMS_CHANCE, INCUBATION_ITERATIONS) for _ in range(pop_size)]
        self.succeptibles = self.population[1:]
        self.infected = [self.population[0]]
        self.infected[0].state = 1
        self.removed = []
        self.isolated = []
        self.isolateStarted = False
        
    def moveNewlyInfected(self, newly_infected):
        for infected in newly_infected:
            infected.state = 1
            index = self.succeptibles.index(infected)
            self.infected.append(infected)
            self.succeptibles.pop(index)        
    
    # Time function, 24 iterations = 1 day 
    def runDay(self, iterations_per_day=24):
        for _ in range(iterations_per_day):
            
            for succeptible in self.succeptibles:
                succeptible.update(self.society_width, self.socity_height)
            
            for infected in self.infected:
                if infected.state == 2:
                    index = self.infected.index(infected)
                    self.removed.append(infected)
                    self.infected.pop(index)


                infected.update(self.society_width, self.socity_height)
                newly_infected = infected.infect(self.succeptibles)
                self.moveNewlyInfected(newly_infected)

            for isolated in self.isolated:
                if isolated.state == 2:
                    self.isolated.pop(self.isolated.index(isolated))
                    self.removed.append(isolated)

                isolated.update(self.society_width, self.socity_height)



            DATA_COLLECT.append([len(self.succeptibles), len(self.infected), len(self.removed)])
        self.isolate(50)


        print(len(self.succeptibles), len(self.infected), len(self.removed), self.numIsolated())
            
    def runNumDays(self, num_days, iterations_per_day=24):
        for _ in range(num_days):
            if len(self.infected) == 0:
                return
            self.runDay(iterations_per_day)

    def numIsolated(self):
        return len(list(filter(lambda x: x.isIsolated == True, self.infected)))

    def isolate(self, capacity=10):
        if len(self.infected) > capacity or self.isolateStarted:
            self.isolateStarted = True

            for infected in self.infected:
                if infected.showsSymptoms:
                    infected.isIsolated = True


society = Society(POPULATION, WIDTH, HEIGHT)

society.runNumDays(DAYS, ITERATIONS_PER_DAY)
DATA_COLLECT = np.array(DATA_COLLECT)
print(DATA_COLLECT.shape)

fig = go.Figure(data=[
    go.Bar(name="Infected", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 1], hovertext=[f"{x} Infected" for x in DATA_COLLECT[:, 1]]),
    go.Bar(name="Susceptible", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:,0], hovertext=[f"{x} Susceptible" for x in DATA_COLLECT[:,0]]),
    go.Bar(name="Removed", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 2], hovertext=[f"{x} Removed" for x in DATA_COLLECT[:,2]])
])

fig2 = go.Figure(data=[
    go.Scatter(name="Infected", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 1]),
    go.Scatter(name="Susceptible", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 0]),
    go.Scatter(name="Removed", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 2])
])


fig.update_layout(barmode='stack', bargap=0)
fig.show()
fig2.show()










        
    