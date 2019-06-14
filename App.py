#!/usr/bin/python

from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, pyqtSlot
import sys

from ML import *
from Models import *

UNIT_SIZE = 20
GAME_SIZE = 16
GAME_MARGIN = 20
EPSILON = 0.3
GAMMA = 0.9
TRAIN_EPOCHS = 5000
TEST_EPOCHS = 50

class GameDisplay(QWidget):
    
    def __init__(self, snake, apple):
        super(QWidget, self).__init__()
        self.snake = snake
        self.apple = apple
        self.enableInput = True
        self.initUI()
        
    def initUI(self):      
        display_size = GAME_SIZE * UNIT_SIZE + GAME_MARGIN * 2
        self.setGeometry(0, 0, display_size, display_size)
        self.setWindowTitle('Snake')
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawYard(qp)
        self.drawApple(qp)
        self.drawSnake(qp)
        qp.end()

    def drawYard(self, qp):
        qp.setPen(Qt.green)
        yard_size = GAME_SIZE * UNIT_SIZE
        qp.drawRect(GAME_MARGIN, GAME_MARGIN, yard_size, yard_size)

    def drawApple(self, qp):
        qp.setPen(Qt.red)
        x = self.apple.x * UNIT_SIZE
        y = self.apple.y * UNIT_SIZE
        qp.drawEllipse(x, y, UNIT_SIZE, UNIT_SIZE)

        
    def drawSnake(self, qp):
        qp.setPen(Qt.black)
        cursor = self.snake.head

        while cursor is not None:
            x,y = cursor.getPos()
            x *= UNIT_SIZE
            y *= UNIT_SIZE
            # print(f'draw node {i}: x={x}, y={y}')
            qp.drawRect(x, y, UNIT_SIZE, UNIT_SIZE)
            cursor = cursor.next


    def keyPressEvent(self, event):
        if self.enableInput is True:
            gey = event.key()
            if gey == Qt.Key_Up:
                self.snake.move(0)
            elif gey == Qt.Key_Down:
                self.snake.move(1)
            elif gey == Qt.Key_Left:
                self.snake.move(2)
            elif gey == Qt.Key_Right:
                self.snake.move(3)
            elif gey == Qt.Key_G:
                self.snake.grow()
            elif gey == Qt.Key_A:
                self.apple.respawn()
            elif gey == Qt.Key_R:
                self.snake.respawn()
                self.apple.respawn()
            self.update()
            # print(f"Score: {self.snake.length}, Steps: {self.snake.steps}")


class Controls(QWidget):
    def __init__(self, gameDisplay, learner):
        super(QWidget, self).__init__()
        self.gameDisplay = gameDisplay
        self.learner = learner

        vbox = QVBoxLayout()
        epsilonLabel = QLabel("Epsilon")
        self.epsilonInput = QLineEdit(self)
        self.epsilonInput.setText(str(EPSILON))
        gammaLabel = QLabel("Gamma")
        self.gammaInput = QLineEdit(self)
        self.gammaInput.setText(str(GAMMA))
        epochLabel = QLabel("Number of Train Sessions")
        self.epochInput = QLineEdit(self)
        self.epochInput.setText(str(TRAIN_EPOCHS))
        self.trainButton = QPushButton("Train", self)
        testLabel = QLabel("Number of Test Sessions")
        self.testEpochsInput = QLineEdit(self)
        self.testEpochsInput.setText(str(TEST_EPOCHS))
        self.testButton = QPushButton("Test", self)
        self.replayButton = QPushButton("Replay", self)

        self.trainButton.clicked.connect(self.trainButtonPressed)
        self.testButton.clicked.connect(self.testButtonPressed)

        vbox.addWidget(epsilonLabel)
        vbox.addWidget(self.epsilonInput)
        vbox.addWidget(gammaLabel)
        vbox.addWidget(self.gammaInput)
        vbox.addWidget(epochLabel)
        vbox.addWidget(self.epochInput)
        vbox.addWidget(self.trainButton)
        vbox.addWidget(testLabel)
        vbox.addWidget(self.testEpochsInput)
        vbox.addWidget(self.testButton)
        vbox.addWidget(self.replayButton)

        self.setLayout(vbox)
        self.show()

    @pyqtSlot()
    def trainButtonPressed(self):
        self.gameDisplay.enableInput = False
        epsilon = self.epsilonInput.text()
        gamma = self.gammaInput.text()
        epochs = self.epochInput.text()
        self.learner.epsilon = float(epsilon)
        self.learner.gamma = float(gamma)
        self.learner.epochs = int(epochs)
        self.qTable = []
        self.learner.train()
        self.gameDisplay.enableInput = True

    @pyqtSlot()
    def testButtonPressed(self):
        self.gameDisplay.enableInput = False
        value = self.testEpochsInput.text()
        self.learner.testEpochs = int(value)
        self.learner.run()
        self.gameDisplay.enableInput = True




if __name__ == '__main__':

    app = QApplication(sys.argv)
    yard = Yard(GAME_SIZE)
    snake = yard.getSnake()
    apple = yard.getApple()
    gameBoard = GameDisplay(snake, apple)

    learner = QLearner(yard, 0.3, 0.9, 5000, 50, gameBoard)
    controls = Controls(gameBoard, learner)

    sys.exit(app.exec_())
