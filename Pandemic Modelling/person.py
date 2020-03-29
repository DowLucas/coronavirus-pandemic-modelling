import random
import math
from sklearn import preprocessing
import numpy as np

class Person:
    def __init__(self, x, y, affectRadius, healtime, infectChance, shows_symptoms_chance, incubationIterations):
        self.x = x
        self.y = y
        self.affectRadius = affectRadius
        self.healTime = healtime
        self.infectChance = infectChance
        self.infectedTime = 0
        self.incubationIterations = incubationIterations
        self.age = 0
        self.shows_symptoms_chance = shows_symptoms_chance
        self.showsSymptoms = False
        self.isIsolated = False

        self.state = 0
        self.states = {
            0: "susceptible",
            1: "infected",
            2: "removed",
        }

        self.moveVector = np.random.uniform(-1, 1, 2)


    def __repr__(self):
        return self.states[self.state]

    def update(self, width, height):
        if self.x > width or self.x < 0:
            self.x *= -1
        if self.y > height or self.y < 0:
            self.x *= -1

        self.moveShift = [np.random.uniform(self.moveVector[0]-0.15, self.moveVector[0]+0.15), np.random.uniform(self.moveVector[1]-0.15, self.moveVector[1]+0.15)]
        self.moveVector += self.moveShift
        self.moveVector = preprocessing.normalize(self.moveVector.reshape(1, -1))[0]

        self.x += self.moveVector[0]
        self.y += self.moveVector[1]



        if self.state == 1:
            self.infectedTime += 1

        if self.infectedTime == self.healTime:
            self.state = 2

        if self.infectedTime == self.incubationIterations:
            self.showsSymptoms = np.random.uniform(0, 1) > self.shows_symptoms_chance



    @staticmethod
    def dist(p1, p2):
        return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))

    def infect(self, susceptibles):
        newlyInfected = []
        if self.isIsolated:
            return []

        for succeptible in susceptibles:
            if succeptible == self:
                continue
            if self.dist([self.x, self.y], [succeptible.x, succeptible.y]) < self.affectRadius and np.random.uniform(0, 1) < self.infectChance:
                newlyInfected.append(succeptible)

        return newlyInfected



