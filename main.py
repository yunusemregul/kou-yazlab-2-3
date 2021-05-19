import time

import pygame
from Board import Board
from Window import Window
from Player import Player
from Plotter import PlotterController
from Constants import MAPSIZE, SHOWPERSTEP

if __name__ == "__main__":
    plotterContoller = PlotterController()
    gameBoard = Board(size=MAPSIZE)
    player = Player(gameBoard, plotterContoller)
    window = Window(board=gameBoard, player=player)

    firstTime = True

    while True:
        if player.startPos and player.endPos and not player.done:
            for i in range(SHOWPERSTEP):
                player.move()
            window.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                window.onClick(pos)
