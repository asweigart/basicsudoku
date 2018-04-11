# TODO - Create "implementations" that use this: a flask app, a tkinter app, a turtle.py app, a pygame app

"""basicsudoku

A simple, basic Sudoku class in Python. Suitable for programming tutorials or experimentation.

Some definitions:
    * grid/board
    * size
    * group (a collection of size symbols)
    * subgrid/box/block/region
    * column
    * row
    * symbols
    * given



>>> board = SudokuBoard()
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
>>> board[0, 0] = 4
>>> board[6, 0] = 8
>>> board[8, 0] = 5
>>> print(board)
4 . . | . . . | 8 . 5
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
"""

import doctest

EMPTY_SPACE = '.'
BOARD_LENGTH = 9
BOARD_LENGTH_SQRT = 3
FULL_BOARD_SIZE = 81

class SudokuBoard(object):
    def __init__(self, symbols=None, strict=True, solved=False):
        """Return a new data structure to represent a 9x9 Sudoku board.
        SudokuBoard objects are mutable and can have their symbols modified
        in-place.

        Symbols can be set using a tuple of two integer indexes (0-8 inclusive)
        for the position, while the symbol is an int or str between 1 and 9.

        Empty spaces on the board are set to EMPTY_SPACE, which is the '.'
        string.

        * symbols - An optional string of 81 symbols to initially fill the board
        with. EMPTY_SPACE, that is '.', can be a symbol. The symbols argument
        doesn't have to produce a valid board.

        * strict - When strict is set to True, setting a space that causes the
        board to be invalid will raise a SudokuBoard exception.

        * solved - If True, the board will be set to random, completed state. If
        there are multiple solutions, a random one will be selected.
        """

        # When strict-mode is True, an exception will be raised if an illegal
        # symbol is placed on the board.
        self._strict = strict
        self.clear_board()

        if symbols is not None:
            # Fill in the spaces with the provided symbols.
            if not isinstance(symbols, str) or len(symbols) != FULL_BOARD_SIZE:
                raise SudokuBoardException('symbols argument must be a string of 81 symbols')

            # Check that all the symbols are valid.
            for symbol in symbols:
                if not self.is_valid_symbol(symbol):
                    raise SudokuBoardException('%r is not valid; symbols must be 1 to 9' % (repr(symbol)))

            # Place the symbol on the board.
            for i, symbol in enumerate(symbols):
                self._board[i % BOARD_LENGTH][i // BOARD_LENGTH] = symbol

            # If the symbols argument results in an invalid board while strict mode is enabled, raise an exception.
            if self._strict and not self.is_valid_board():
                self.clear_board()
                raise SudokuBoardException('symbols argument results in an invalid board while strict mode is enabled')

        # Solve the board, if needed.
        if solved:
            self.solve()

    @property
    def strict(self):
        return self._strict

    @strict.setter
    def strict(self, value):
        if not isinstance(value, bool):
            raise SudokuBoardException('strict must be set to a bool value')
        self._strict = value


    def clear_board(self):
        """Sets all spaces on the board to EMPTY_SPACE."""
        self._board = [[EMPTY_SPACE] * BOARD_LENGTH for i in range(BOARD_LENGTH)] # create an empty board


    def is_valid_symbol(self, symbol):
        return len(symbol) == 1 and symbol in EMPTY_SPACE + '123456789'


    def is_complete_group(self, group):
        if not self.is_valid_group(group):
            return False

        if EMPTY_SPACE in group:
            return False

        return len(group) == BOARD_LENGTH


    def is_valid_group(self, group):
        # Check to make sure group is valid.
        try:
            if len(group) != BOARD_LENGTH:
                raise SudokuBoardException('group must be a sequence with exactly 9 symbols, not %r' % (group,))
        except TypeError:
            raise SudokuBoardException('group must be a sequence with exactly 9 symbols, not %r' % (group,))

        for symbol in group:
            if not self.is_valid_symbol(symbol):
                raise SudokuBoardException('group contains an invalid symbol: %r' % (symbol,))

        # Check for any repeat symbols in group, aside from EMPTY_SPACE.
        symbolSet = set()
        for symbol in group:
            if symbol != EMPTY_SPACE and symbol in symbolSet:
                return False
            symbolSet.add(symbol)

        return True


    def is_valid_board(self):
        """Returns True if the board is in a valid state (even if incomplete),
        otherwise return False if the board has invalid symbols set to any of the
        spaces."""

        # Check each of the columns for validity.
        for x in range(BOARD_LENGTH):
            if not self.is_valid_group(self.get_column(x)):
                return False

        # Check each of the rows for validity.
        for y in range(BOARD_LENGTH):
            if not self.is_valid_group(self.get_row(y)):
                return False

        # Check each of the subgrids for validity.
        for top in range(BOARD_LENGTH_SQRT):
            for left in range(BOARD_LENGTH_SQRT):
                if not self.is_valid_group(self.get_subgrid(left, top)):
                    return False

        return True


    def is_full(self):
        """Returns True if there are no empty spaces on the board, otherwise
        returns False."""
        for x in range(BOARD_LENGTH):
            for y in range(BOARD_LENGTH):
                if self._board[x][y] == EMPTY_SPACE:
                    return False
        return True


    def is_solved(self):
        """Returns True if the board is currently solved, otherwise returns False."""
        return self.is_full() and self.is_valid_board()


    def __getitem__(self, key):
        if not isinstance(key , tuple) or len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise SudokuBoardException('key must be a tuple of two integers')

        x, y = key
        if x < 0 or x >= BOARD_LENGTH:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= BOARD_LENGTH:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        return self._board[x][y]


    def __setitem__(self, key, value):
        if not isinstance(key , tuple) or len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise SudokuBoardException('key must be a tuple of two integers')

        x, y = key
        if x < 0 or x >= BOARD_LENGTH:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= BOARD_LENGTH:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        value = str(value) # value can be a string or an int
        if not self.is_valid_symbol(value):
            raise SudokuBoardException('%r is not a valid symbol, symbols must be int or str between 1 and 9' % (value))

        old_value = self._board[x][y]
        self._board[x][y] = value

        if self._strict:
            if self.is_valid_board() == False:
                self._board[x][y] = old_value # restore old value
                raise SudokuBoardException('strict mode is enabled, and this symbol assignment causes the board to become invalid')


    def get_row(self, row):
        if not isinstance(row, int) or row < 0 or row >= BOARD_LENGTH:
            raise SudokuBoardException('row must be an int between 0 and 8')

        return [self._board[x][row] for x in range(BOARD_LENGTH)]


    def get_column(self, column):
        if not isinstance(column, int) or column < 0 or column >= BOARD_LENGTH:
            raise SudokuBoardException('column must be an int between 0 and 8')

        return [self._board[column][y] for y in range(BOARD_LENGTH)]


    def get_subgrid(self, subgrid_x, subgrid_y):
        if not isinstance(subgrid_x, int) or subgrid_x < 0 or subgrid_x >= BOARD_LENGTH_SQRT:
            raise SudokuBoardException('subgrid_x must be an int between 0 and 2')

        if not isinstance(subgrid_y, int) or subgrid_y < 0 or subgrid_y >= BOARD_LENGTH_SQRT:
            raise SudokuBoardException('subgrid_y must be an int between 0 and 2')

        subgrid = []
        start_x = subgrid_x * BOARD_LENGTH_SQRT
        start_y = subgrid_y * BOARD_LENGTH_SQRT
        for y in range(start_y, start_y + BOARD_LENGTH_SQRT):
            for x in range(start_x, start_x + BOARD_LENGTH_SQRT):
                subgrid.append(self._board[x][y])

        return subgrid


    def get_symbols(self):
        """Returns a string or tuple of all size^2 symbols on the board.

        TODO"""
        symbols = []
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                symbols.append(self._board[x][y])

        return ''.join(symbols)


    def __str__(self):
        """Returns a string representation of the board. There are lines between
        the subgrids but no border. It looks something like:

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
        """
        all_rows = []

        for y in range(BOARD_LENGTH):
            row = self.get_row(y)

            # Add vertical separators to the row.
            row.insert(3, '|')
            row.insert(7, '|')

            all_rows.append(' '.join(row))

            # Add a horizontal separator, if needed.
            if y == 2 or y == 5:
                all_rows.append('------+-------+------')

        return '\n'.join(all_rows)


    def __repr__(self):
        return "SudokuBoard(symbols=%r)" % (self.get_symbols(),)


    def solve(self):
        pass


    def __copy__(self):
        """Returns a copy of this object."""
        return SudokuBoard(symbols=self.get_symbols())


    def __deepcopy__(self):
        """Returns a deep copy of this object (which is the same as a shallow
        copy for this class)."""
        return self.__copy__()


    def copy(self):
        """Returns a copy of this object."""
        return self.__copy__()


class SudokuBoardException(Exception):
    """For simplicity, the basicsudoku module only has one exception. Any
    Python built-in exceptions raised from basicsudoku should be considered
    bugs.
    """
    pass


# Some sample SudokuBoard objects for testing/debugging purposes.
_b1 = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
_b2 = SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')


if __name__ == '__main__':
    doctest.testmod()
