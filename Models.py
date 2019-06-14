import random
import numpy as np

REWARD_APPLE = 5
REWARD_COLLISION = -2
REWARD_APPROACH = 2
MAX_STEPS_WITHOUT_SCORE = 100


class Yard:
    def __init__(self, board_size):
        self.board_size = board_size
        self.snake = Snake(self, board_size)
        self.apple = Apple(self, board_size)
        self.bestGameLog = []
        self.currentGameLog = []
        self.bestScore = 0
        self.snake.respawn()

    def isSnakeEatingApple(self):
        x, y = self.snake.head.getPos()

        if x == self.apple.x and y == self.apple.y:
            return True
        else:
            return False

    def isOnSnake(self, x, y):
        cursor = self.snake.head
        while cursor is not None:
            snakeX, snakeY = cursor.getPos()
            if snakeX == x and snakeY == y:
                return True
            cursor = cursor.next
        return False

    def isOnSnakeBody(self, x, y):
        cursor = self.snake.head.next
        if cursor is not None:
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

    def checkCollision(self, x, y):

        if x <= 0:
            return True
        if x > self.board_size:
            return True
        if y <= 0:
            return True
        if y > self.board_size:
            return True
        if self.isOnSnakeBody(x, y):
            return True
        return False

    def logger(self):
        snapshot = []
        snapshot.append(self.snake.toArray())
        snapshot.append(self.apple.toArray())
        self.currentGameLog.append(snapshot)

    def endGame(self):
        if self.snake.length >= self.bestScore:
            self.bestGameLog = self.currentGameLog
            self.bestScore = self.snake.length
        self.currentGameLog = []


class Apple:
    def __init__(self, yard, board_size):
        self.x = None
        self.y = None
        self.yard = yard
        self.board_size = board_size
        self.respawn()

    def respawn(self):
        x = random.randint(1, self.board_size)
        y = random.randint(1, self.board_size)

        while self.yard.isOnSnake(x, y):
            x = random.randint(1, self.board_size)
            y = random.randint(1, self.board_size)

        self.x = x
        self.y = y

    # print(f" Apple spawned at {x},{y}")

    def toArray(self):
        return self.x, self.y


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

    def __init__(self, yard, board_size):
        self.board_size = board_size
        self.yard = yard
        self.length = 1
        self.head = None
        self.steps = 0
        self.stepsSinceLastScore = 0

    def toArray(self):
        positions = []
        cursor = self.head
        while cursor is not None:
            positions.append(cursor.getPos())
            cursor = cursor.next
        return positions

    def respawn(self):
        self.yard.endGame()
        self.head = Node(random.randint(1, self.board_size),
                         random.randint(1, self.board_size))
        self.length = 1
        self.steps = 0
        self.stepsSinceLastScore = 0
        self.growMode = False

        # print("Snake respawned")

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
        self.stepsSinceLastScore = 0
        curHead = self.head
        x, y = curHead.getPos()
        newX, newY = self.__nodeShift(x, y, dir)
        newHead = Node(newX, newY)
        newHead.setNext(self.head)
        curHead.setPrevious(newHead)
        self.head = newHead
        self.grow()

    def printNodes(self):
        cursor = self.head
        while cursor is not None:
            # print(cursor.getPos())
            cursor = cursor.next

    def __nodeShift(self, x, y, dir):
        if dir == 0:  # up
            y -= 1
        elif dir == 1:  # down
            y += 1
        elif dir == 2:  # left
            x -= 1
        elif dir == 3:  # right
            x += 1
        return (x, y)

    def move(self, dir):
        reward = 0
        gameover = False

        self.yard.logger()

        if self.__doesApproachFood(dir):
            reward = REWARD_APPROACH

        self.steps += 1
        self.stepsSinceLastScore += 1

        if self.growMode is True:
            self.growMove(dir)

        else:
            cursor = self.head
            x, y = self.__nodeShift(*cursor.getPos(), dir)

            while cursor is not None:
                oldX, oldY = cursor.getPos()
                cursor.setPos(x, y)
                x = oldX
                y = oldY
                cursor = cursor.next

            if self.yard.isSnakeEatingApple():
                reward = REWARD_APPLE
                self.grow()
                self.yard.apple.respawn()

        # print(f"Score={self.length}, steps={self.steps}")

        if self.yard.checkCollision(*self.head.getPos()) or self.stepsSinceLastScore > MAX_STEPS_WITHOUT_SCORE:
            reward = REWARD_COLLISION
            gameover = True
        # self.respawn()

        state = self.getState()
        # print(state)
        score = self.length
        steps = self.steps

        if gameover is True:
            self.respawn()

        return state, reward, gameover, score, steps

    def getState(self):
        state = np.zeros(8, dtype=int)
        for i in range(4):
            state[i] = self.yard.checkCollision(*self.vicinityPosition(i))
        state[4:] = self.__foodDirections()

        return self.__listToInt(state)

    def __listToInt(self, lst):
        return int("".join(str(x) for x in lst), 2)

    def __doesApproachFood(self, dir):
        foodDir = self.__foodDirections()
        # print (foodDir)
        if dir == 0 and foodDir[0] > 0:
            return True
        elif dir == 1 and foodDir[1] > 0:
            return True
        elif dir == 2 and foodDir[2] > 0:
            return True
        elif dir == 3 and foodDir[3] > 0:
            return True
        else:
            return False

    def __foodDirections(self):
        state = np.zeros(4, dtype=int)

        distX = self.yard.apple.x - self.head.getPos()[0]
        distY = self.yard.apple.y - self.head.getPos()[1]

        if distY < 0:  # up
            state[0] = 1
        if distY > 0:  # down
            state[1] = 1
        if distX < 0:  # left
            state[2] = 1
        if distX > 0:  # right
            state[3] = 1

        return state

    def vicinityPosition(self, dir):
        x, y = self.head.getPos()
        if dir == 0:
            y -= 1
        elif dir == 1:
            y += 1
        elif dir == 2:
            x -= 1
        elif dir == 3:
            x += 1
        return x, y
