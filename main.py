import pygame
from Board import Board
from Window import Window
from Cell import Cell

gameBoard = Board(size=25)
window = Window(board=gameBoard)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
