import numpy as np
import random


BOARD_SIZE = 25
COAST_FORWARD = True


class Game:
	def __init__(self, board_size):
		self.yard = np.zeros([board_size, board_size], dtype=int)
		self.snake = Snake(board_size)


class Node:
	def __init__(self, x, y):
		self.next = None
		self.previous = None
		self.x = x
		self.y = y

	def setPos(self, x, y):
		self.x = x
		self.y = y

	def hasNext(self):
		if self.next is None:
			return False
		else:
			return True

	def setNext(self, nextNode):
		self.next = nextNode

	def setPrevious(self, prevNode):
		self.previous = prevNode

	def getPos(self):
		return (self.x, self.y)


class Snake:
	def __init__(self, board_size, display_unit):
		self.head = Node(random.randint(0,board_size), random.randint(0,board_size))
		self.length = 1
		self.board_size = board_size
		self.display_unit = display_unit

	def direction(self):
		pass

	def updateLength(self):
		if self.head is None:
			return 0

		cursor = self.head
		i = 1
		while cursor.hasNext:
			i += 1
			cursor = cursor.nextNode
		return i
		
	def grow(self, dir):
		self.length += 1
		curHead = self.head
		x,y = curHead.getPos()
		newX,newY = self.__nodeShift(x,y,dir)
		newHead = Node(newX,newY)
		newHead.setNext(self.head)
		curHead.setPrevious(newHead)
		self.head = newHead
		self.printNodes()

	def printNodes(self):
		cursor = self.head
		while cursor is not None:
			print(cursor.getPos())
			cursor = cursor.next


	def __nodeShift(self, x, y, dir):
		if dir == 'up':
			y -= self.display_unit
		elif dir == 'down':
			y += self.display_unit
		elif dir == 'left':
			x -= self.display_unit
		elif dir == 'right':
			x += self.display_unit
		return (x,y)

	def move(self, dir):

		cursor = self.head
		x,y = self.__nodeShift(*cursor.getPos(), dir)

		while cursor is not None:

			oldX, oldY = cursor.getPos()
			cursor.setPos(x,y)
			x = oldX
			y = oldY
			cursor = cursor.next

		self.printNodes()

