from hexsweeper.board import Board

board = Board(10, 10, 10)

rows = len(board.field)
for row in board.field:
    print(" "*rows, end="")
    rows -= 1
    for t in row:
        char = '.' if t.is_mine else str(t.value)
        print(char + " ", end="")
    print()
