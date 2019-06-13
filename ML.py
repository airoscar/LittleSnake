from Models import *
import random
import numpy as np


class QLearner:

    def __init__(self, epsilon, gamma, epochs):
        self.epsilon = epsilon
        self.gamma = gamma
        self.epochs = epochs
        self.rTable = []
        self.qTable = []

    def initializeQTable(self):
        numStates = 2 ** 8
        numActions = 4  # 4 directions that the snake can move
        self.qTable = np.zeros((numStates, numActions))

    def initializeRTable(self):
        pass

    def epsilonDecider(self):

        if random.uniform(0, 1) < self.epsilon:  # random action
            pass
        else:  # action with max future reward value
            pass


    
