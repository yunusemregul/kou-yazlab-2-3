import math
import random

from Cell import Cell
from Action import Action
from Constants import EPSILON, DISCOUNT, REWARDS, STOP_AFTER_X_EPISODES_WITH_NO_CHANGES


class Player:
    def __init__(self, board, plotterController):
        self.board = board
        self.startPos = None
        self.pos = None
        self.endPos = None
        self.totalVisited = set()
        self.finalPath = set()
        self.finalPathDistance = math.inf
        self.steps = 0
        self.episode = 0
        self.plotterController = plotterController
        self.notChangedSinceEpisodes = 0
        self.done = False

    def epsilonGreedy(self):
        cell = self.board.getCell(self.pos)

        if self.finalPathDistance != math.inf and random.random() <= EPSILON:
            # print("keşif yaptım")
            return random.choice(cell.actions)
        else:
            # print("maxı seçtim")
            return cell.getMaxAction()

    def getNextCell(self, pos, action) -> Cell:
        return self.board.getCell((pos[0] + action.directionVector[0], pos[1] + action.directionVector[1]))

    def move(self):
        self.totalVisited.add(self.pos)
        action = self.epsilonGreedy()
        nextCell = self.getNextCell(self.pos, action)

        action.reward += nextCell.reward + DISCOUNT * nextCell.getMaxAction().reward - action.reward

        # sonraki hücre duvarsa veya sonraki hücre hedef konumsa yeni bir episodeye başla
        if self.board.isCellABlock(nextCell.pos) or self.endPos == nextCell.pos:
            # print("%s çarpıldı %d puan eklendi" % (("hedefe" if self.endPos == nextCell.pos else "duvara"),
            #                                       nextCell.reward + DISCOUNT * nextCell.getMaxAction().reward))

            if self.finalPathDistance != math.inf:
                self.notChangedSinceEpisodes += 1

                if self.notChangedSinceEpisodes >= STOP_AFTER_X_EPISODES_WITH_NO_CHANGES:
                    self.done = True

            self.plotterController.sendData({
                "step": self.steps,
                "cost": (REWARDS["end"] if self.endPos == nextCell.pos else REWARDS["block"]),
                "episode": self.episode,
                "done": self.done
            })
            self.pos = self.startPos
            self.episode += 1
            self.steps = 0

            if self.endPos == nextCell.pos:
                self.totalVisited.add(nextCell.pos)

            if self.endPos in self.totalVisited:
                finalPath, distance = self.calculateFinalPath()

                if self.finalPathDistance == math.inf:
                    self.finalPath = finalPath
                    self.finalPathDistance = distance
                    self.notChangedSinceEpisodes = 0
                else:
                    if distance < self.finalPathDistance:
                        self.finalPath = finalPath
                        self.finalPathDistance = distance
                        self.notChangedSinceEpisodes = 0

        else:
            self.pos = nextCell.pos
            self.steps += 1

    def calculateFinalPath(self):
        if self.endPos not in self.totalVisited:
            return set(), math.inf

        if self.board.getCell(self.pos).getMaxAction().reward <= 0:
            return set(), math.inf

        finalPath = set()
        distance = 0
        curPos = self.startPos
        finalPath.add(curPos)

        while curPos != self.endPos and len(finalPath) < len(self.totalVisited) * 2:
            cell = self.board.getCell(curPos)
            maxAction: Action = cell.getMaxAction()

            if maxAction.directionVector[0] == 0 or maxAction.directionVector[1] == 0:
                distance += 1  # köşegenden gidilmiyosa toplam mesafeye 1 ekliyoruz
            else:
                distance += 1.414  # köşegenden gidiliyorsa kök 2 ekliyoruz toplam mesafeye

            nextCell = self.getNextCell(curPos, maxAction)
            finalPath.add(nextCell.pos)
            curPos = nextCell.pos

        return finalPath, distance

    def setStart(self, pos):
        self.startPos = pos
        self.pos = self.startPos

    def setEnd(self, pos):
        self.endPos = pos
