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
import math

EMPTY_SPACE = '.'


class SudokuBoard(object):
    def __init__(self, symbols=None, size=9, strict=True, solved=False):
        """TODO

        * symbols - An optional sequence of symbols to initially fill the board
        with. The symbols must be valid for the board size, and size^2 symbols
        must be provided. EMPTY_SPACE can be a symbol. The symbols argument
        doesn't have to produce a valid board. If the size is 1, 4, or 9, symbols
        can be a string. For larger boards (where symbols are more than one
        character long), symbols must be a non-string sequence. If symbols is
        specified, it will override the size argument.

        * size - An integer of the length & height of the board, which is 9
        by default. The size must be a square number (i.e. 1, 4, 9, 16, 25, etc.)
        The spaces will be increased to accomodate multidigit symbols.

        * strict - When strict is set to True, setting a space that causes the
        board to be invalid will raise a SudokuBoard exception.

        * solved - If True, the board will be set to random, completed state. If
        there are multiple solutions, a random one will be selected.
        """

        if symbols is not None:
            size = int(math.sqrt(len(symbols)))

        if not isinstance(size, int) or size < 0 or math.sqrt(size) % 1 != 0:
            raise SudokuBoardException('SudokuBoard size must be a square integer, such as 9, 16, 25, etc')
        self.size = size
        self.size_sqrt = int(math.sqrt(self.size))

        # When strict-mode is True, an exception will be raised if an illegal
        # symbol is placed on the board.
        self.strict = strict
        self._board = [[EMPTY_SPACE] * self.size for i in range(self.size)] # create an empty board

        if symbols is not None:
            # Fill in the spaces with the provided symbols.
            if isinstance(symbols, str) and self.size > 9:
                raise SudokuBoardException('symbols argument cannot be string if size is greater than 9, use a non-string sequence instead')

            if len(symbols) != self.size ** 2:
                raise SudokuBoardException('symbols argument must contain %s symbols' % (self.size ** 2))

            for i, symbol in enumerate(symbols):
                symbol = str(symbol)
                if not self.is_valid_symbol(symbol):
                    raise SudokuBoardException('%r is not a valid symbol for a %s x %s board' % (repr(symbol), self.size, self.size))
                self._board[i % self.size][i // self.size] = symbol

        if solved:
            self.solve()


    def is_valid_symbol(self, symbol):
        if symbol == EMPTY_SPACE:
            return True

        if not str(symbol).isdigit():
            return False

        return symbol == EMPTY_SPACE or 1 <= int(symbol) <= self.size


    def is_complete_group(self, group):
        if not self.is_valid_group(group):
            return False

        if EMPTY_SPACE in group:
            return False

        return len(set(group)) == len(group)


    def is_valid_group(self, group):
        try:
            if len(group) != self.size:
                raise SudokuBoardException('group must be a sequence with exactly %s items' % (self.size))
        except TypeError:
            raise SudokuBoardException('group must be a sequence with exactly %s items' % (self.size))

        for symbol in group:
            if not self.is_valid_symbol(symbol):
                raise SudokuBoardException('group contains an invalid symbol')

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
        for x in range(self.size):
            if not self.is_valid_group(self.get_column(x)):
                return False

        # Check each of the rows for validity.
        for y in range(self.size):
            if not self.is_valid_group(self.get_row(y)):
                return False

        # Check each of the subgrids for validity.
        for top in range(self.size_sqrt):
            for left in range(self.size_sqrt):
                if not self.is_valid_group(self.get_subgrid(left, top)):
                    return False

        return True


    def is_full(self):
        for x in range(self.size):
            for y in range(self.size):
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
        if x < 0 or x >= self.size:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= self.size:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        return self._board[x][y]


    def __setitem__(self, key, value):
        if not isinstance(key , tuple) or len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise SudokuBoardException('key must be a tuple of two integers')

        x, y = key
        if x < 0 or x >= self.size:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= self.size:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        value = str(value) # value can be a string or an int
        if not self.is_valid_symbol(value):
            raise SudokuBoardException('%r is not a valid symbol, symbols must be int or str between 1 and %s' % (value, self.size - 1))

        old_value = self._board[x][y]
        self._board[x][y] = value

        if self.strict:
            if self.is_valid_board() == False:
                self._board[x][y] = old_value # restore old value
                raise SudokuBoardException('strict mode is enabled, and this symbol assignment causes the board to become invalid')


    def get_row(self, row):
        if not isinstance(row, int) or row < 0 or row >= self.size:
            raise SudokuBoardException('row must be an int between 0 and %s' % (self.size - 1))

        return [self._board[x][row] for x in range(self.size)]


    def get_column(self, column):
        if not isinstance(column, int) or column < 0 or column >= self.size:
            raise SudokuBoardException('column must be an int between 0 and %s' % (self.size - 1))

        return [self._board[column][y] for y in range(self.size)]


    def get_subgrid(self, subgrid_x, subgrid_y):
        if not isinstance(subgrid_x, int) or subgrid_x < 0 or subgrid_x >= self.size_sqrt:
            raise SudokuBoardException('subgrid_x must be an int between 0 and %s' % (self.size_sqrt - 1))

        if not isinstance(subgrid_y, int) or subgrid_y < 0 or subgrid_y >= self.size_sqrt:
            raise SudokuBoardException('subgrid_y must be an int between 0 and %s' % (self.size_sqrt - 1))

        subgrid = []
        start_x = subgrid_x * self.size_sqrt
        start_y = subgrid_y * self.size_sqrt
        for y in range(start_y, start_y + self.size_sqrt):
            for x in range(start_x, start_x + self.size_sqrt):
                subgrid.append(self._board[x][y])

        return subgrid


    def get_symbols(self):
        """Returns a string or tuple of all size^2 symbols on the board.

        TODO"""
        symbols = []
        for y in range(self.size):
            for x in range(self.size):
                symbols.append(self._board[x][y])

        if self.size <= 9:
            # Return the symbols as a string.
            return ''.join(symbols)
        else:
            # Otherwise, since the symbols can be multiple-digits long, return a tuple.
            return tuple(symbols)


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
        symbol_length = len(str(self.size_sqrt))

        all_rows = []

        for y in range(self.size):
            row = list(self.get_row(y))

            # Add vertical separators to the row.
            for i in range(self.size - 1 - self.size_sqrt, -1, -self.size_sqrt):
                row.insert(i + 1, '|')

            # Go through the row and make sure it is properly spaced if
            # symbols can have multiple digits.
            if self.size > 9:
                for i, symbol in enumerate(row):
                    row[i] = symbol.rjust(symbol_length)

            all_rows.append(' '.join(row))

            # Add a horizontal separator, if needed.
            if (y + 1) % self.size_sqrt == 0 and y != (self.size - 1):
                all_rows.append('-' * (symbol_length * self.size_sqrt + self.size_sqrt) +
                                '+' +
                                '-' * (symbol_length * self.size_sqrt + self.size_sqrt + 1) +
                                '+' +
                                '-' * (symbol_length * self.size_sqrt + self.size_sqrt))

        return '\n'.join(all_rows)


    def __repr__(self):
        return "SudokuBoard(symbols=%r)" % (self.get_symbols(),)


    def solve(self):
        pass


class SudokuBoardException(Exception):
    """For simplicity, the basicsudoku module only has one exception. Any
    Python built-in exceptions raised from basicsudoku should be considered
    bugs.
    """
    pass


b1 = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
b2 = SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')


if __name__ == '__main__':
    doctest.testmod()
