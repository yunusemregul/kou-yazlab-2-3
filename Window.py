import pygame

pygame.init()

width = 1024
taskbarHeight = 50
height = width + taskbarHeight


class Window:
    def __init__(self, board):
        self.surface = pygame.display.set_mode((width, height), pygame.NOFRAME)
        self.board = board

        self.draw()

    def draw(self):
        self.surface.fill((22, 22, 22))  # background
        self.drawTaskBar()
        self.drawBoard()

        pygame.display.update()

    def drawTaskBar(self):
        pygame.draw.rect(self.surface, (11, 11, 11), (0, 0, width, taskbarHeight))

    def drawGridLines(self):
        stepSize = width / self.board.size

        for horizontal in range(self.board.size):
            pygame.draw.line(self.surface, (44, 44, 44), (0, taskbarHeight + horizontal * stepSize),
                             (width, taskbarHeight + horizontal * stepSize))

        for vertical in range(self.board.size):
            pygame.draw.line(self.surface, (44, 44, 44), (vertical * stepSize, taskbarHeight),
                             (vertical * stepSize, height))

    def drawCells(self):
        cellSize = width / self.board.size
        font = pygame.font.SysFont(None, int(cellSize) - 12)

        for y in range(self.board.size):
            for x in range(self.board.size):
                start = (x * cellSize, taskbarHeight + y * cellSize)
                cell = self.board.cells[y][x]
                text = font.render(str(cell.reward), True, (255, 255, 255))
                # self.surface.blit(text, (start, start))

                if cell.reward < 0:
                    pygame.draw.rect(self.surface, (237, 106, 90),
                                     (x * cellSize, taskbarHeight + y * cellSize, cellSize, cellSize))

    def drawBoard(self):
        self.drawCells()
        self.drawGridLines()
