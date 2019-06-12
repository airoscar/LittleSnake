
import random


class Yard:
	def __init__(self, board_size, display_unit):
		self.board_size = board_size
		self.snake = Snake(self, board_size, display_unit)
		self.apple = Apple(self, board_size)

	def isSnakeEatingApple(self):
		x,y = self.snake.head.getPos()

		if x == self.apple.x and y == self.apple.y:
			return True
		else:
			return False

	def isOnSnake(self, x,y):
		cursor = self.snake.head
		while cursor is not None:
			snakeX, snakeY = cursor.getPos()
			if snakeX == x and snakeY == y:
				return True
			cursor = cursor.next
		return False

	def getSnake(self):
		return self.snake

	def getApple(self):
		return self.apple


class Apple:
	def __init__(self, yard, board_size):
		self.x = None
		self.y = None
		self.yard = yard
		self.board_size = board_size
		self.respawn()

	def respawn(self):

		x = random.randint(0, self.board_size)
		y = random.randint(0, self.board_size)
		print(x, y)

		while self.yard.isOnSnake(x,y):

			x = random.randint(0, self.board_size)
			y = random.randint(0, self.board_size)
			print(x, y)

		self.x = x
		self.y = y


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
	def __init__(self, yard, board_size, display_unit):
		self.head = Node(random.randint(0,board_size), random.randint(0,board_size))
		self.length = 1
		self.board_size = board_size
		self.display_unit = display_unit
		self.yard = yard
		self.growMode = False

	def direction(self):
		pass

	def updateLength(self):
		if self.head is None:
			return 0

		cursor = self.head
		i = 1
		while cursor.hasNext():
			i += 1
			cursor = cursor.next
		return i

	def grow(self):
		self.growMode = not self.growMode
		
	def growMove(self, dir):
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

		if self.growMode is True:
			self.growMove(dir)

		else:
			cursor = self.head
			x,y = self.__nodeShift(*cursor.getPos(), dir)

			while cursor is not None:

				oldX, oldY = cursor.getPos()
				cursor.setPos(x,y)
				x = oldX
				y = oldY
				cursor = cursor.next

			if self.yard.isSnakeEatingApple():
				self.grow()
				self.yard.apple.respawn()

