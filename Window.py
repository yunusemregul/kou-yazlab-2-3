import pygame

from Board import Board
from Player import Player
from Cell import Cell
from Action import Action
from Constants import REWARDS

pygame.init()

width = 1280
taskbarHeight = 50
height = width + taskbarHeight


class Window:
    def __init__(self, board, player):
        self.player: Player = player
        self.surface = pygame.display.set_mode((width, height))
        self.board: Board = board
        self.cellSize = width / self.board.size

        self.draw()

    def getClickedCellPos(self, screenpos):
        if screenpos[1] <= taskbarHeight:
            return False

        return int(screenpos[0] / self.cellSize), int((screenpos[1] - taskbarHeight) / self.cellSize)

    def getCellScreenpos(self, pos):
        return pos[0] * self.cellSize, taskbarHeight + pos[1] * self.cellSize

    def onClick(self, pos):
        if not self.player.startPos:
            clickedCellPos = self.getClickedCellPos(pos)

            if clickedCellPos:
                if not self.board.isCellABlock(clickedCellPos):
                    self.player.setStart(clickedCellPos)
                    print("başlangıç seçildi")
                else:
                    print("duvarlar başlangıç olarak seçilemez")
            else:
                print("seçilen hücre geçerli bir hücre değil")
        elif not self.player.endPos:
            clickedCellPos = self.getClickedCellPos(pos)

            if clickedCellPos:
                if clickedCellPos != self.player.startPos:
                    if not self.board.isCellABlock(clickedCellPos):
                        self.player.setEnd(self.getClickedCellPos(pos))
                        self.board.getCell(clickedCellPos).reward = REWARDS["end"]
                        print("bitiş seçildi")
                    else:
                        print("duvarlar bitiş olarak seçilemez")
                else:
                    print("başlangıç bitişle aynı olamaz")
            else:
                print("seçilen hücre geçerli bir hücre değil")

        self.draw()

    def draw(self):
        self.surface.fill((22, 22, 22))  # background
        self.drawTaskBar()
        self.drawBoard()
        self.drawPlayer()
        pygame.display.update()

    def drawTaskBar(self):
        pygame.draw.rect(self.surface, (11, 11, 11), (0, 0, width, taskbarHeight))

    def drawGridLines(self):
        stepSize = self.cellSize

        for horizontal in range(self.board.size):
            pygame.draw.line(self.surface, (44, 44, 44), (0, taskbarHeight + horizontal * stepSize),
                             (width, taskbarHeight + horizontal * stepSize))

        for vertical in range(self.board.size):
            pygame.draw.line(self.surface, (44, 44, 44), (vertical * stepSize, taskbarHeight),
                             (vertical * stepSize, height))

    def drawCells(self):
        cellSize = self.cellSize
        font = pygame.font.SysFont(None, int(cellSize) - 12)

        for y in range(self.board.size):
            for x in range(self.board.size):
                start = (x * cellSize, taskbarHeight + y * cellSize)
                cell: Cell = self.board.cells[y][x]
                text = font.render(str(cell.reward), True, (255, 255, 255))
                # self.surface.blit(text, (start, start))

                if self.board.isCellABlock(cell.pos):
                    pygame.draw.rect(self.surface, (68, 1, 34),
                                     (x * cellSize, taskbarHeight + y * cellSize, cellSize, cellSize))

                if cell.pos in self.player.finalPath:
                    pygame.draw.rect(self.surface, (1, 68, 34),
                                     (x * cellSize, taskbarHeight + y * cellSize, cellSize, cellSize))

                maxAction = cell.getMaxAction()

                if maxAction.reward != 0:
                    pygame.draw.line(self.surface, (0, 255, 0), (start[0] + cellSize / 2, start[1] + cellSize / 2),
                                     (start[0] + cellSize / 2 + maxAction.directionVector[0] * (cellSize / 3),
                                      start[1] + cellSize / 2 + maxAction.directionVector[1] * (cellSize / 3)),
                                     3)

                if cell.pos in self.player.totalVisited:
                    for action in cell.actions:
                        if action.reward < 0:
                            pygame.draw.line(self.surface, (255, 0, 0),
                                             (start[0] + cellSize / 2, start[1] + cellSize / 2),
                                             (start[0] + cellSize / 2 + action.directionVector[0] * (cellSize / 4),
                                              start[1] + cellSize / 2 + action.directionVector[1] * (cellSize / 4)))

    def drawBoard(self):
        self.drawCells()
        self.drawGridLines()

    def drawPlayer(self):
        if self.player.startPos:
            startCellX, startCellY = self.getCellScreenpos(self.player.startPos)

            # oyuncu başlangıç
            pygame.draw.circle(self.surface, (31, 158, 137),
                               (startCellX + self.cellSize / 2, startCellY + self.cellSize / 2),
                               self.cellSize / 3)

        if self.player.endPos:
            endCellX, endCellY = self.getCellScreenpos(self.player.endPos)

            # oyuncu hedef
            pygame.draw.circle(self.surface, (55, 91, 141),
                               (endCellX + self.cellSize / 2, endCellY + self.cellSize / 2),
                               self.cellSize / 3)

        if self.player.startPos and self.player.endPos:
            # episode
            font = pygame.font.SysFont(None, 32)
            text = font.render("Episode: %d" % self.player.episode,
                               True, (255, 255, 255))
            self.surface.blit(text, (5, 17))

            posX, posY = self.getCellScreenpos(self.player.pos)

            # oyuncu
            pygame.draw.circle(self.surface, (240, 229, 30),
                               (posX + self.cellSize / 2, posY + self.cellSize / 2),
                               self.cellSize / 4)
        else:
            font = pygame.font.SysFont(None, 32)
            text = font.render("Lütfen %s konumunu seçiniz." % ("başlangıç" if not self.player.startPos else "bitiş"),
                               True, (255, 255, 255))
            self.surface.blit(text, (5, 17))
