from random import randint
from typing import Tuple, List, Optional
from queue import Queue

from hexsweeper.base.enums import State, UncoverResult
from hexsweeper.base.tile import Tile


class GroupInfo:
    def __init__(self, tiles: List[Tile]):
        self.tiles: List[Tile] = tiles
        self.tiles_amount: int = len(tiles)

        self.mines: List[Tile] = [tile for tile in tiles if tile.is_mine]
        self.mines_amount: int = len(self.mines)

        self.flags: List[Tile] = [tile for tile in tiles if tile.state == State.FLAGGED]
        self.flags_amount: int = len(self.flags)


class Board:
    def __init__(
        self,
        width: int,
        height: int,
        mine_count: int,
    ):
        self.width: int = width
        self.height: int = height
        self.mine_count: int = mine_count

        self.field: List[List[Tile]] = None
        self._generate_field()

    def get_size(self) -> Tuple[int, int]:
        """Get the size of the board.

        Returns `(width, height)`"""
        return (self.width, self.height)

    def flag(self, x: int, y: int) -> bool:
        """
        Flag a tile on the field.

        If a tile doesn't exist or uncovered, returns False
        Otherwise returns True
        """

        tile = self.get_tile(x, y)
        if tile == None:
            return False
        if tile.state == State.UNCOVERED:
            return False

        tile.state = State.FLAGGED if tile.state == State.COVERED else State.COVERED
        self._set_tile(x, y, tile)
        return True

    def uncover(self, x: int, y: int) -> UncoverResult:
        """
        Uncover a tile

        If a tile doesn't exist on given position returns `UncoverResult.NOTVALID`
        If a tile is flagged or uncovered returns `UncoverResult.NOTVALID`
        If a tile is a mine returns `UncoverResult.MISTAKE`
        Otherwise returns `UncoverResult.SUCCESS`
        """

        tile = self.get_tile(x, y)
        if tile == None or tile.state != State.COVERED:
            return UncoverResult.NOTVALID

        if tile.is_mine:
            return UncoverResult.MISTAKE

        queue = Queue()
        queue.put(tile)
        while not queue.empty():
            t: Tile = queue.get()
            if t.state == State.COVERED:
                if t.value == 0:
                    for n in self._get_neighbors(t.x, t.y).tiles:
                        queue.put(n)
                t.state = State.UNCOVERED
                self._set_tile(t.x, t.y, t)

        return UncoverResult.SUCCESS

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Returns a tile on given `x` and `y`

        If a tile doesn't exist, returns None
        """

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return self.field[y][x]

    def _set_tile(self, x: int, y: int, tile: Tile) -> None:
        """Replaces a tile on given `x` and `y` if possible"""

        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        self.field[y][x] = tile

    def _get_neighbors(self, x: int, y: int) -> GroupInfo:
        """
        Returns GroupInfo object that contains information about neighboring tiles

        Tile neighbors are x:
             x x .
             x T x
             . x x

        Because scewing the board makes it look like this:
              x x .
             x T x
            . x x
        """

        tiles = []
        for offset_x in range(-1, 2):
            for offset_y in range(-1, 2):
                # Bottom left
                if offset_x == -1 and offset_y == 1:
                    continue
                # Upper right
                if offset_x == 1 and offset_y == -1:
                    continue
                # Tile itself
                if offset_x == 0 and offset_y == 0:
                    continue

                tile = self.get_tile(x + offset_x, y + offset_y)
                if tile != None:
                    tiles.append(tile)

        return GroupInfo(tiles)

    def _generate_mine(self) -> None:
        """Generates a new mine"""

        tiles_amount = self.width * self.height
        if self.mine_count + 1 > tiles_amount:
            return
        while True:
            rx = randint(0, self.width - 1)
            ry = randint(0, self.height - 1)
            if self.field[ry][rx].is_mine:
                continue
            self.field[ry][rx].is_mine = True
            for n in self._get_neighbors(rx, ry).tiles:
                n.value += 1
                self._set_tile(n.x, n.y, n)
            break

    def _generate_field(self) -> None:
        """Generates the field"""

        self.field = []
        mines_everywhere = self.mine_count >= (self.width * self.height)
        for y in range(self.height):
            row = [
                Tile(mines_everywhere, State.COVERED, x, y) for x in range(self.width)
            ]
            self.field.append(row)

        if not mines_everywhere:
            for _ in range(self.mine_count):
                self._generate_mine()
