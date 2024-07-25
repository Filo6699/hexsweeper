import pygame as pg

from hexsweeper import Hexsweeper, Board, Theme


pg.init()
screen = pg.display.set_mode(flags=pg.FULLSCREEN)

width = 10
height = 5

theme = Theme()
board = Board(width, height, 10)
game = Hexsweeper(screen, board, theme)


def update_game():
    global game
    game.board = Board(width, height, 10)


clock = pg.time.Clock()
game.draw()

while True:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            exit()
        if e.type == pg.KEYDOWN:
            if e.unicode == "y":
                height += 1
                update_game()
            if e.unicode == "j":
                width += 1
                update_game()
            if e.unicode == "n":
                height -= 1
                update_game()
            if e.unicode == "g":
                width -= 1
                update_game()
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            game.click(*e.pos)

    game.draw()
    pg.display.flip()

    clock.tick(60)
