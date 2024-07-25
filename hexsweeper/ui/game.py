from typing import Tuple, Optional
from math import cos, sin, radians

import pygame as pg

from hexsweeper.base.board import Board
from hexsweeper.base.enums import State, UncoverResult
from hexsweeper.ui.theme import Theme


class Hexsweeper:
    def __init__(self, screen: pg.Surface, board: Board, theme: Theme):
        # Those two will get initialized with @board.setter
        # Ratio of width and height of the board
        self._size_ratio: Tuple[float, float] = None
        self._tile_size: int = None

        self.screen: pg.Surface = screen
        self.theme: Theme = theme

        self.board: Board = board

        self._board_collision = None

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board: Board):
        self._board = new_board

        width, height = self._board.get_size()

        self._size_ratio = (
            width + height / 2,
            height * (3**0.5) / 2,
        )
        self._tile_size = min(
            round((self.screen.get_width() * 0.9) / self._size_ratio[0]),
            round((self.screen.get_height() * 0.9) / self._size_ratio[1]),
        )

        # Upper left cell position
        self._anchor = [
            (self.screen.get_width() - self._size_ratio[0] * self._tile_size) // 2,
            (self.screen.get_height() - self._size_ratio[1] * self._tile_size) // 2,
        ]
        # Accounting for the horizontal offset of board scew
        self._anchor[0] += self._tile_size * (height - 1) / 2

        # Offsets per x and y unit
        self._row_offset = [
            -self._tile_size / 2,
            self._tile_size / 2 * (3**0.5),
        ]
        self._column_offset = [
            self._tile_size,
            0,
        ]

        self.theme.scale = self.theme.initial_scale * (self._tile_size / 160)
        self._board_collision = None

    def _draw_polygon(
        self,
        center: Tuple[float, float],
        color: Tuple[int, int, int],
        radius: float,
        width: float,
        surface=None,
    ) -> None:
        """Draws a polygon on self.screen"""

        if surface == None:
            surface = self.screen
        
        width = round(width)
        radius -= width // 2
        polygon_points = [
            (
                center[0] + (radius * cos(radians(90 + 60 * i))),
                center[1] + (radius * sin(radians(90 + 60 * i))),
            )
            for i in range(6)
        ]
        pg.draw.polygon(
            surface,
            color,
            polygon_points,
            width,
        )

    def _world_to_board(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        cell_pos = self._board_collision.get_at((x, y))
        if (cell_pos[0] == 0):
            return None
        return (cell_pos[0] - 1, cell_pos[1] - 1)

    def click(self, x: int, y: int):
        x, y = self._world_to_board(x, y)
        self.board.uncover(x, y)

    def draw(self) -> None:
        """Update the screen"""

        self.screen.fill(self.theme.background)
        width, height = self.board.get_size()

        size_ratio = self._size_ratio
        tile_size = self._tile_size

        theme = self.theme

        update_collision = False
        if not self._board_collision:
            update_collision = True
            self._board_collision = pg.Surface(self.screen.get_size())

        for y in range(height):
            for x in range(width):
                tile = self._board.get_tile(x, y)
                center = [
                    self._anchor[0]
                    + self._tile_size / 2
                    + self._row_offset[0] * y
                    + self._column_offset[0] * x,
                    self._anchor[1]
                    + self._tile_size / 2
                    + self._row_offset[1] * y
                    + self._column_offset[1] * x,
                ]

                if update_collision:
                    self._draw_polygon(
                        center,
                        (x+1, y+1, 0),
                        tile_size / 2,
                        0,
                        surface=self._board_collision,
                    )

                if tile.state == State.COVERED:
                    self._draw_polygon(
                        center,
                        theme.cover_inner,
                        tile_size / 2,
                        0,
                    )
                    self._draw_polygon(
                        center,
                        theme.shadow,
                        tile_size / 2,
                        (theme.shadow_width + theme.cover_outline_width) * theme.scale,
                    )
                    self._draw_polygon(
                        center,
                        theme.cover_outline,
                        tile_size / 2,
                        theme.cover_outline_width * theme.scale,
                    )
                if tile.state == State.UNCOVERED:
                    self._draw_polygon(
                        center,
                        theme.inner,
                        tile_size / 2,
                        0,
                    )
                    self._draw_polygon(
                        center,
                        theme.inner_outline,
                        tile_size / 2,
                        theme.inner_outline_width * theme.scale,
                    )
