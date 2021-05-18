import random

from Cell import Cell
from Action import Action
from Constants import EPSILON, DISCOUNT


class Player:
    def __init__(self, board):
        self.board = board
        self.startPos = None
        self.pos = None
        self.endPos = None
        self.episode = 0

    def EpsilonGreedy(self, cell):
        if random.random() <= EPSILON:
            return random.choice(cell.actions)
        else:
            return cell.getMaxAction()

    def getNextCell(self, pos, action) -> Cell:
        return self.board.getCell((pos[0] + action.directionVector[0], pos[1] + action.directionVector[1]))

    def move(self):
        cell = self.board.getCell(self.pos)
        action = self.EpsilonGreedy(cell)
        nextCell = self.getNextCell(self.pos, action)

        action.reward += nextCell.reward + DISCOUNT * nextCell.getMaxAction().reward

        # sonraki hücre duvarsa veya sonraki hücre hedef konumsa yeni bir episodeye başla
        if nextCell.reward < 0 or self.endPos == nextCell.pos:
            self.pos = self.startPos
            self.episode += 1
        else:
            self.pos = nextCell.pos

    def setStart(self, pos):
        self.startPos = pos
        self.pos = self.startPos

    def setEnd(self, pos):
        self.endPos = pos
