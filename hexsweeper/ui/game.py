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
        self._mistakes: int = 0
        self._font = pg.font.SysFont("JetBrains Mono", self._tile_size // 2)

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
        self._font = pg.font.SysFont("", self._tile_size // 2)

    def _draw_hexagon(
        self,
        center: Tuple[float, float],
        color: Tuple[int, int, int],
        radius: float,
        width: float,
        surface=None,
    ) -> None:
        """Draws a polygon on self.screen"""

        collision = True
        if surface == None:
            collision = False
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
        if (
            x < 0
            or y < 0
            or x >= self.screen.get_width()
            or y >= self.screen.get_height()
        ):
            return None
        cell_pos = self._board_collision.get_at((x, y))
        if sum(cell_pos) == 255 * 3:
            return None
        x = cell_pos[0] + ((cell_pos[1] >> 4) << 8)
        y = cell_pos[2] + ((cell_pos[1] % 16) << 8)
        return (x, y)

    def uncover(self, x: int, y: int):
        pos = self._world_to_board(x, y)
        if pos == None:
            return
        result = self.board.uncover(*pos)
        if result == UncoverResult.MISTAKE:
            self._mistakes += 1

    def flag(self, x: int, y: int):
        pos = self._world_to_board(x, y)
        if pos == None:
            return
        self.board.flag(*pos)

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
                    self._draw_hexagon(
                        center,
                        (x % 256, (((x >> 8) << 4) + (y >> 8)), y % 256),
                        tile_size / 2,
                        0,
                        surface=self._board_collision,
                    )

                hexs = []

                if tile.state in [State.COVERED, State.FLAGGED]:
                    inner_color = (
                        theme.cover_inner
                        if tile.state == State.COVERED
                        else theme.flag_inner
                    )
                    hexs.append((inner_color, 0))
                    shadow = [abs(c - 70) for c in inner_color]
                    hexs.append(
                        (
                            shadow,
                            max(
                                (theme.shadow_width + theme.cover_outline_width)
                                * theme.scale,
                                1,
                            ),
                        )
                    )
                    hexs.append(
                        (
                            theme.cover_outline,
                            max(theme.cover_outline_width * theme.scale, 1),
                        )
                    )

                if tile.state == State.UNCOVERED:
                    hexs.append((theme.inner, 0))
                    hexs.append(
                        (
                            theme.inner_outline,
                            max(theme.inner_outline_width * theme.scale, 1),
                        )
                    )

                for h in hexs:
                    self._draw_hexagon(center, h[0], tile_size / 2, h[1])

                if tile.state == State.UNCOVERED:
                    value_render = self._font.render(str(tile.value), True, theme.text)
                    value_pos = [
                        center[0] - value_render.get_width() / 2,
                        center[1] - value_render.get_height() / 2,
                    ]
                    self.screen.blit(value_render, value_pos)

        mistakes_text = self._font.render(
            f"Mistakes: {self._mistakes}", True, theme.text
        )
        mistakes_text_pos = [
            (self.screen.get_width() - mistakes_text.get_width()) / 2,
            5,
        ]
        self.screen.blit(mistakes_text, mistakes_text_pos)
