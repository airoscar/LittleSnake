from Models import *
import random
import numpy as np
import time

class QLearner:

    def __init__(self, game, epsilon, gamma, epochs, UI):
        self.game = game
        self.epsilon = epsilon
        self.gamma = gamma
        self.epochs = epochs
        self.UI = UI
        self.qTable = []
        self.scores = []
        self.initialize()
        self.train()
        self.run()

    def initialize(self):
        numStates = 2 ** 8
        numActions = 4  # 4 directions that the snake can move
        self.qTable = np.zeros((numStates, numActions))

    def train(self):

        print("Training started...")

        for gameInstance in range(self.epochs):

            # initial move
            state, reward, gameover, score, steps = self.game.snake.move(random.randint(0,3))

            while not gameover:
                action = self.__actionEncoder(state)
                future_state, reward, gameover, score, steps = self.game.snake.move(action)
                self.UI.update()
                self.qTable[state, action] = reward + self.gamma * np.max(self.qTable[future_state,:])
                state = future_state
                # print(state)
            # print(f"Train session: score {score}, steps {steps}")
        print("Training finished")

        self.printQTable()


    def run(self):

        print("Testing...")

        for i in range(50):

            gameover = False
            state = self.game.snake.getState()
            action = np.argmax(self.qTable[state, :])

            while not gameover:
                self.UI.update()
                state, reward, gameover, score, steps = self.game.snake.move(action)
                action = np.argmax(self.qTable[state, :])

            self.scores.append(score)

            print(f"Game {i}, score: {score}, steps: {steps}")
        print(f"Highest score: {max(self.scores)}")


    def printQTable(self):
        for row in self.qTable:
            print(row)


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
