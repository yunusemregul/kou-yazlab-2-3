import pygame
from Player import Player

pygame.init()

width = 1024
taskbarHeight = 50
height = width + taskbarHeight


class Window:
    def __init__(self, board, player):
        self.player = player
        self.surface = pygame.display.set_mode((width, height))
        self.board = board
        self.cellSize = width / self.board.size

        self.draw()

    def getClickedCell(self, pos):
        if pos[1] <= taskbarHeight:
            return False

        return int(pos[0] / self.cellSize), int((pos[1] - taskbarHeight) / self.cellSize)

    def getCellPos(self, pos):
        return (pos[0] * self.cellSize, taskbarHeight + pos[1] * self.cellSize)

    def onClick(self, pos):
        if not self.player.startPos:
            clickedCell = self.getClickedCell(pos)

            if clickedCell:
                if not self.board.isCellABlock(clickedCell):
                    self.player.setStart(clickedCell)
                    print("başlangıç seçildi")
                else:
                    print("duvarlar başlangıç olarak seçilemez")
            else:
                print("seçilen hücre geçerli bir hücre değil")
        elif not self.player.endPos:
            clickedCell = self.getClickedCell(pos)

            if clickedCell:
                if clickedCell != self.player.startPos:
                    if not self.board.isCellABlock(clickedCell):
                        self.player.setEnd(self.getClickedCell(pos))
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
                cell = self.board.cells[y][x]
                text = font.render(str(cell.reward), True, (255, 255, 255))
                # self.surface.blit(text, (start, start))

                if cell.reward < 0:
                    pygame.draw.rect(self.surface, (68, 1, 34),
                                     (x * cellSize, taskbarHeight + y * cellSize, cellSize, cellSize))

    def drawBoard(self):
        self.drawCells()
        self.drawGridLines()

    def drawPlayer(self):
        if self.player.startPos and self.player.endPos:
            startCellX, startCellY = self.getCellPos(self.player.startPos)
            posX, posY = self.getCellPos(self.player.pos)
            endCellX, endCellY = self.getCellPos(self.player.endPos)
            # oyuncu başlangıç
            pygame.draw.circle(self.surface, (31, 158, 137),
                               (startCellX + self.cellSize / 2, startCellY + self.cellSize / 2),
                               self.cellSize / 3)

            # oyuncu
            pygame.draw.circle(self.surface, (240, 229, 30),
                               (posX + self.cellSize / 2, posY + self.cellSize / 2),
                               self.cellSize / 4)

            # hedef
            pygame.draw.circle(self.surface, (55, 91, 141),
                               (endCellX + self.cellSize / 2, endCellY + self.cellSize / 2),
                               self.cellSize / 3)
        else:
            font = pygame.font.SysFont(None, 32)
            text = font.render("Lütfen başlangıç ve bitiş konumlarını seçiniz.", True, (255, 255, 255))
            self.surface.blit(text, (5, 17))
