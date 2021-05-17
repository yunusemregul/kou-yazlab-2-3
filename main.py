import pygame
from Board import Board
from Window import Window
from Player import Player

gameBoard = Board(size=25)
player = Player(gameBoard)
window = Window(board=gameBoard, player=player)

while True:
    if player.startPos and player.endPos:
        player.move()
        window.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            window.onClick(pos)
