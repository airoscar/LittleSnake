from Models import *
import random
import numpy as np


class QLearner:

    def __init__(self, game, epsilon, gamma, epochs, UI):
        self.game = game
        self.epsilon = epsilon
        self.gamma = gamma
        self.epochs = epochs
        self.UI = UI
        self.qTable = []

        self.initialize()
        self.run()

    def initialize(self):
        numStates = 2 ** 8
        numActions = 4  # 4 directions that the snake can move
        self.qTable = np.zeros((numStates, numActions))

    def run(self):

        for gameInstance in range(self.epochs):
            self.game.snake.respawn()
            # initial move
            state, reward, gameover, score, steps = self.game.snake.move(random.randint(0,3))

            while not gameover:
                action = self.__actionEncoder(state)
                future_state, reward, gameover, score, steps = self.game.snake.move(action)
                # self.UI.update()
                self.qTable[state, action] = reward + self.gamma * np.max(self.qTable[future_state,:])
                state = future_state

            print(f"Gameover: score {score}, steps {steps}")



    def __epsilonSwtich(self):
        """Returns True or False based on epsilon threshold and randomness"""
        if random.uniform(0, 1) < self.epsilon:  # random action
            return True
        else:  # action with max future reward value
            return False

    def __actionEncoder(self, state):
        """Returns an action given a state"""

        if self.__epsilonSwtich():
            return random.randint(0,3)
        else:
            return np.argmax(self.qTable[state, :])
