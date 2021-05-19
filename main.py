import time

import pygame
from Board import Board
from Window import Window
from Player import Player
from Constants import MAPSIZE, SHOWPERSTEP

gameBoard = Board(size=MAPSIZE)
player = Player(gameBoard)
window = Window(board=gameBoard, player=player)

firstTime = True

while True:
    if player.startPos and player.endPos:
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
