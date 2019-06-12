#!/usr/bin/python

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import sys, random

from Models import *

class Display(QWidget):
    
    def __init__(self, snake):
        super().__init__()
        self.snake = snake
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(0, 0, 1000, 600)
        self.setWindowTitle('Snake')
        self.show()
        

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawNode(qp)
        qp.end()
        
    def drawNode(self, qp):
        qp.setPen(Qt.red)
        size = self.size()
        x,y = snake.getHead().getPos()
        qp.drawRect(x, y, 20 , 20)
        # qp.end()


    def keyPressEvent(self, event):
        gey = event.key()
        # self.func = (None, None)
        if gey == Qt.Key_Up:
            self.snake.move('up')
        elif gey == Qt.Key_Right:
            self.snake.move('right')
        elif gey == Qt.Key_Left:
            self.snake.move('left')
        elif gey == Qt.Key_Down:
            self.snake.move('down')
        self.update()


if __name__ == '__main__':
    snake = Snake(100,5)
    app = QApplication(sys.argv)
    window = Display(snake)
    sys.exit(app.exec_())
