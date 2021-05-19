from Cell import Cell
from Action import Action
from random import shuffle
from Constants import REWARDS


class Board:
    def __init__(self, size):
        self.size = size
        self.cells = [None] * size

        blockIndexes = self.generateRandomIndexes(percent=30)

        for y in range(size):
            self.cells[y] = [None] * size

            for x in range(size):
                self.cells[y][x] = Cell((x, y))

                index = y * size + x

                if index in blockIndexes:
                    self.cells[y][x].reward = REWARDS["block"]

                self.cells[y][x].actions = self.calculateActionsForXY(x, y)

        engelTxt = open("engel.txt", "w")

        for y in range(size):
            for x in range(size):
                engelTxt.write(self.cells[y][x].toString() + "\t")
            engelTxt.write("\n")

        engelTxt.close()

    def getCell(self, pos) -> Cell:
        x, y = pos
        return self.cells[y][x]

    def isCellABlock(self, pos):
        return self.getCell(pos).reward == REWARDS["block"]

    def calculateActionsForXY(self, x, y):
        actions = []

        if x > 0:
            actions.append(Action('left'))
        if x < (self.size - 1):
            actions.append(Action('right'))
        if y > 0:
            actions.append(Action('top'))
        if y < (self.size - 1):
            actions.append(Action('bottom'))
        if x > 0 and y > 0:
            actions.append(Action('topleft'))
        if x < (self.size - 1) and y > 0:
            actions.append(Action('topright'))
        if x > 0 and y < (self.size - 1):
            actions.append(Action('bottomleft'))
        if x < (self.size - 1) and y < (self.size - 1):
            actions.append(Action('bottomright'))

        return actions

    def generateRandomIndexes(self, percent):
        toGenerateAmount = int((self.size ** 2) * percent / 100)
        indexes = [i for i in range(self.size ** 2)]

        shuffle(indexes)

        indexes = indexes[:toGenerateAmount]
        indexes = set(indexes)

        return indexes
