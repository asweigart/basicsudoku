# basicsudoku
A simple, basic Sudoku class in Python. Suitable for programming tutorials or experimentation.

The `basicsudoku` module provides just the data structure for a 9x9 sudoku board, along with a basic solver. This module can be used

## Installation

`pip install basicsudoku`

## Getting Started

```
>>> import basicsudoku
>>> board = basicsudoku.SudokuBoard() # Get a blank board.
>>> print(board)
>>> print(board)
. . . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . .
------+-------+------
. . . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . .
------+-------+------
. . . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . .
>>> board[0, 0] = 1
>>> board[1, 0] = '2'
>>> board[8, 8] = 3
>>> print(board)
1 2 . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . .
------+-------+------
. . . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . .
------+-------+------
. . . | . . . | . . .
. . . | . . . | . . .
. . . | . . . | . . 3
>>> board.symbols
'12..............................................................................3'
>>> board.symbols = '2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3'
>>> print(board)
2 . . | . 8 . | 3 . .
. 6 . | . 7 . | . 8 4
. 3 . | 5 . . | 2 . 9
------+-------+------
. . . | 1 . 5 | 4 . 8
. . . | . . . | . . .
4 . 2 | 7 . 6 | . . .
------+-------+------
3 . 1 | . . 7 | . 4 .
7 2 . | . 4 . | . 6 .
. . 4 | . 1 . | . . 3

>>> solver = basicsudoku.BasicSolver(board)
>>> print(board)
2 4 5 | 9 8 1 | 3 7 6
1 6 9 | 2 7 3 | 5 8 4
8 3 7 | 5 6 4 | 2 1 9
------+-------+------
9 7 6 | 1 2 5 | 4 3 8
5 1 3 | 4 9 8 | 6 2 7
4 8 2 | 7 3 6 | 9 5 1
------+-------+------
3 9 1 | 6 5 7 | 8 4 2
7 2 8 | 3 4 9 | 1 6 5
6 5 4 | 8 1 2 | 7 9 3

>>> board2 = basicsudoku.SudokuBoard(symbols='2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3')
>>> print(board2)
2 . . | . 8 . | 3 . .
. 6 . | . 7 . | . 8 4
. 3 . | 5 . . | 2 . 9
------+-------+------
. . . | 1 . 5 | 4 . 8
. . . | . . . | . . .
4 . 2 | 7 . 6 | . . .
------+-------+------
3 . 1 | . . 7 | . 4 .
7 2 . | . 4 . | . 6 .
. . 4 | . 1 . | . . 3
```

## Definitions

* *board* - The full 9 x9 board, consisting of 81 spaces.
* *space* - One of the 81 places on the board where a symbol can be placed.
* *symbol* - A number from 1 to 9 that is placed on the board. A space can also be empty.
* *length* - The length of the board (either height or width), which is 9 in standard Sudoku.
* *unit* - A collection of 9 symbols from a row, column, or box.
* *box* - One of the nine 3x3 subgrids on the board.
* *column* - Nine vertical spaces on the board.
* *row* - Nine horizontal spaces on the board.
* *given* - A symbol that is on the board at the start of a puzzle.
* *peer* - The spaces in the same row, column, or box as a specified space.

## API

The `basicsudoku` module is meant to be easy to learn. All methods have descriptive docstrings and the code is well-commented.

### Create a Sudoku Board

Creating an empty Sudoku board:

```
>>> board = basicsudoku.SudokuBoard()
```

Prepopulate a board with symbols:

```
>>> board = basicsudoku.SudokuBoard(symbols='2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3')
```

Disable strict mode (strict mode causes an exception to be raised if you place a symbol on the board that makes it invalid.)

```
>>> board = basicsudoku.SudokuBoard(strict=False)
```

Or:

```
>>> board = basicsudoku.SudokuBoard()
>>> board.strict = False
```

### Set and Get Symbols

You can assign integers or strings from 1 to 9 to an xy tuple index:

```
>>> board = basicsudoku.SudokuBoard()
>>> board[0, 0] = '1'
>>> board[0, 0]
'1'
>>> board[1, 0] = 2
>>> board[1, 0]
'2'
```

You can use the `symbols` attribute to get or set all of the symbols at once:

```
>>> board = basicsudoku.SudokuBoard()
>>> board.symbols = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
>>> print(board)
4 . . | . . . | 8 . 5
. 3 . | . . . | . . .
. . . | 7 . . | . . .
------+-------+------
. 2 . | . . . | . 6 .
. . . | . 8 . | 4 . .
. . . | . 1 . | . . .
------+-------+------
. . . | 6 . 3 | . 7 .
5 . . | 2 . . | . . .
1 . 4 | . . . | . . .
```

You can also get a unit (9 symbols) from a row, column, or box with these methods:

```
>>> board = basicsudoku.SudokuBoard(symbols='4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
>>> print(board)
4 . . | . . . | 8 . 5
. 3 . | . . . | . . .
. . . | 7 . . | . . .
------+-------+------
. 2 . | . . . | . 6 .
. . . | . 8 . | 4 . .
. . . | . 1 . | . . .
------+-------+------
. . . | 6 . 3 | . 7 .
5 . . | 2 . . | . . .
1 . 4 | . . . | . . .

>>> board.get_row(0)
['4', '.', '.', '.', '.', '.', '8', '.', '5']
>>> board.get_row(1)
['.', '3', '.', '.', '.', '.', '.', '.', '.']
>>> board.get_column(0)
['4', '.', '.', '.', '.', '.', '.', '5', '1']
>>> board.get_box(0, 0)
['4', '.', '.', '.', '3', '.', '.', '.', '.']
>>> board.get_box(1, 0)
['.', '.', '.', '.', '.', '.', '7', '.', '.']
```

### Validation Checks

By default, `SudokuBoard` objects are in *strict mode*, meaning any symbols added to the board that make the board *invalid* (this is, have duplicate symbols in the same row, column, or box) will cause a `SudokuBoardException` to be raised. You can set the keyword argument `strict=False` in the constructor method call to disable this. There are also several validation checking methods:

* `is_valid_symbol(self, symbol)` - Returns True if symbol is a str between 1 and 9, or is EMPTY_SPACE.
* `is_complete_unit(self, unit)` - Returns True if unit is a str of all 9 symbols with no repeats.
* `is_valid_unit(self, unit)` - Returns True if unit is a str of 9 symbols, which can include EMPTY_SPACE but doesn't have repeated symbols.
* `is_valid_board(self)` - Returns True if the board is in a valid state (even if incomplete), otherwise return False if the board has repeated symbols set to any of the rows, columns, or boxes.
* `is_full(self)` - Returns True if there are no empty spaces on the board.
* `is_solved(self)` - Returns True if the board is currently solved.

### Iterator

You can iterate over the symbols in the board, starting from the top left and going right, then down. For example:

```
>>> board = basicsudoku.SudokuBoard(symbols='4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
>>> for symbol in board:
...     print(symbol, end=' ')
...
4 . . . . . 8 . 5 . 3 . . . . . . . . . . 7 . . . . . . 2 . . . . . 6 . . . . . 8 . 4 . . . . . . 1 . . . . . . . 6 . 3 . 7 . 5 . . 2 . . . . . 1 . 4 . . . . . .
```

## Solving Sudoku Puzzles

The `BasicSolver` class is passed a `SudokuBoard` object and immediately solves it.

```
>>> board = SudokuBoard(symbols='4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
>>> print(board)
4 . . | . . . | 8 . 5
. 3 . | . . . | . . .
. . . | 7 . . | . . .
------+-------+------
. 2 . | . . . | . 6 .
. . . | . 8 . | 4 . .
. . . | . 1 . | . . .
------+-------+------
. . . | 6 . 3 | . 7 .
5 . . | 2 . . | . . .
1 . 4 | . . . | . . .
>>> solver = BasicSolver(board)
>>> print(board)
4 1 7 | 3 6 9 | 8 2 5
6 3 2 | 1 5 8 | 9 4 7
9 5 8 | 7 2 4 | 3 1 6
------+-------+------
8 2 5 | 4 3 7 | 1 6 9
7 9 1 | 5 8 6 | 4 3 2
3 4 6 | 9 1 2 | 7 5 8
------+-------+------
2 8 9 | 6 4 3 | 5 7 1
5 7 3 | 2 9 1 | 6 8 4
1 6 4 | 8 7 5 | 2 9 3
```

## Included Sudoku Puzzles

The puzzles provided by Peter Norvig's sudoku page are included. The `basicsudoku.easy50` list contains 50 easy puzzles, the `basicsudoku.top95` list contains 95 puzzles, and `basicsudoku.hardest` contains 11 very difficult puzzles. Pass the 81-character strings in these lists to the `symbols` keyword argument in the `SudokuBoard` constructor to load them onto the board.

## Unit Tests

The module has pytest unit tests in the *tests/test_basic.py* file, as well as doctests in the main module's docstrings. The coverage.py tool can be run over the module as well, and the latest report is in the *htmlcov/index.html* file.

## Roadmap

In the future I plan on adding a puzzle generator, with variable difficulty setting. I'd also like the solver to detect if there are multiple solutions to a board.

`basicsudoku` is written for readability, not performance. There are many places where the performance could be improved, especially in the solver. There are no plans for improving the performance. This module was made as a learning tool, not as an efficient sudoku solver (of which there are already many).