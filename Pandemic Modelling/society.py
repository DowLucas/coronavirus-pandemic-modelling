import numpy as np
import math
from person import Person
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


HEAL_TIME_IN_DAYS = 14
INCUBATION_IN_DAYS = 7
AFFECT_RADIUS = 25-(25*0.25)
INFECT_CHANCE = 0.005#-(0.005*0.25)
DAYS = 365
ITERATIONS_PER_DAY = 24
HEAL_ITERATIONS = ITERATIONS_PER_DAY*HEAL_TIME_IN_DAYS
POPULATION = 500
WIDTH = 300
HEIGHT = 300
NO_SYMPTOMS_CHANCE = 0
INCUBATION_ITERATIONS = INCUBATION_IN_DAYS * ITERATIONS_PER_DAY
USE_ISOLATION = False


DATA_COLLECT = []

print(INFECT_CHANCE)

class Society():
    def __init__(self, pop_size, width, height, society_isolate):
        self.society_width = width
        self.socity_height = height
        self.use_isolation = society_isolate


        self.population = [Person(np.random.randint(0, width), np.random.randint(0, height), AFFECT_RADIUS, HEAL_ITERATIONS, INFECT_CHANCE, NO_SYMPTOMS_CHANCE, INCUBATION_ITERATIONS) for _ in range(pop_size)]
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
            if self.use_isolation:
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
        if not self.use_isolation:
            return
        if len(self.infected) > capacity or self.isolateStarted:
            self.isolateStarted = True

            for infected in self.infected:
                if infected.showsSymptoms:
                    infected.isIsolated = True


society = Society(POPULATION, WIDTH, HEIGHT, USE_ISOLATION)

society.runNumDays(DAYS, ITERATIONS_PER_DAY)
DATA_COLLECT = np.array(DATA_COLLECT)
print(DATA_COLLECT.shape)

fig = go.Figure(data=[
    go.Bar(name="Infected", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 1]/POPULATION, hovertext=[f"{x} Infected" for x in DATA_COLLECT[:, 1]]),
    go.Bar(name="Susceptible", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:,0]/POPULATION, hovertext=[f"{x} Susceptible" for x in DATA_COLLECT[:,0]]),
    go.Bar(name="Removed", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 2]/POPULATION, hovertext=[f"{x} Removed" for x in DATA_COLLECT[:,2]])
])

fig2 = go.Figure(data=[
    go.Scatter(name="Infected", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 1]/POPULATION),
    go.Scatter(name="Susceptible", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 0]/POPULATION),
    go.Scatter(name="Removed", x=np.arange(len(DATA_COLLECT)), y=DATA_COLLECT[:, 2]/POPULATION)
])


fig.update_layout(
    title="SIR Model 25% Lower Infect Radius",
    font=dict(
        family="Roboto",
        size=19,
        color="#000"
    ),
    xaxis_title="Iterations",
    yaxis_title="Proportion of Population",
    barmode='stack',
    bargap=0,
)

fig.show()
fig2.show()










        
    