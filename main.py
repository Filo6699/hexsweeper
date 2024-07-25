import pygame as pg

from hexsweeper import Hexsweeper, Board, Theme
from hexsweeper.base.enums import UncoverResult


pg.init()
screen = pg.display.set_mode(flags=pg.FULLSCREEN)
test = pg.Surface(screen.get_size(), flags=pg.SRCALPHA)

width = 14
height = 9
mine_count = 10

theme = Theme()
theme.background = (240, 240, 240)
theme.text = (0, 0, 0)
theme.inner = (230, 230, 230)
theme.inner_outline_width = 8
theme.inner_outline = (210, 210, 210)
theme.cover_outline_width = 8
board = Board(width, height, mine_count)
game = Hexsweeper(test, board, theme)


def update_game():
    global game
    game.board = Board(width, height, mine_count)


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
        if e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:  # left click
                uncover_result = game.uncover(*e.pos)
            if e.button == 3:  # right click
                game.flag(*e.pos)

    game.draw()
    game.screen.set_alpha(110)
    screen.blit(game.screen, (0, 0))
    pg.display.flip()

    clock.tick(60)
