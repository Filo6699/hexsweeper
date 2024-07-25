from typing import Tuple

from hexsweeper.base.enums import State


class Tile:
    def __init__(self, is_mine: bool, state: State, x: int, y: int):
        self.is_mine: bool = is_mine
        self.value: int = 0
        self.state: State = state
        self.x: int = x
        self.y: int = y

    @property
    def pos(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self) -> str:
        if self.is_mine:
            return f"<Tile pos{self.pos} MINE {self.state}>"
        else:
            return f"<Tile pos{self.pos} {self.value} {self.state}>"
