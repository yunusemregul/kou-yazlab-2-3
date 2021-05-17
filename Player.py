import random

epsilon = 0.5

class Player:
    def __init__(self, board):
        self.board = board
        self.startPos = None
        self.pos = None
        self.endPos = None

    def EpsilonGreedy(self, cell):
        if random.random() < epsilon:
            return random.choice(cell.actions)
        else:
            return cell.getMaxAction()

    def applyAction(self, action):
        self.pos = (self.pos[0] + action.directionVector[0], self.pos[1] + action.directionVector[1])

    def move(self):
        cell = self.board.getCell(self.pos)
        action = self.EpsilonGreedy(cell)
        self.applyAction(action)

    def setStart(self, pos):
        self.startPos = pos
        self.pos = self.startPos

    def setEnd(self, pos):
        self.endPos = pos
