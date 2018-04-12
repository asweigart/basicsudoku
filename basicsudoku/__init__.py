"""basicsudoku

A simple, basic Sudoku class in Python. Suitable for programming tutorials or experimentation.

Some definitions used in this module:
    * board - The entire 9x9 sudoku board.
    * length - The length of the square board size, which is 9.
    * space - One of the 81 places a symbol can go on the board.
    * unit - A collection of 9 symbols from a row, column, or box.
    * box - One of the nine 3x3 grids inside the board.
    * column - The symbols going from the top to the bottom of the board.
    * row - The symbols going from left to right on the board.
    * symbols - A single digit from 1 to 9.
    * given - A symbol that is on the board at the start of a puzzle.

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
BOARD_LENGTH_SQRT = 3 # square root of BOARD_LENGTH
FULL_BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH

class SudokuBoard(object):
    def __init__(self, symbols=None, strict=True):
        """Return a new data structure to represent a 9x9 Sudoku board.
        SudokuBoard objects are mutable and can have their symbols modified
        in-place.

        Symbols can be set using a tuple of two integer indexes (0-8 inclusive)
        for the position, while the symbol is an int or str between 1 and 9.

        No matter if set to an int or str, symbols are always stored and
        returned as strings.

        Empty spaces on the board are set to EMPTY_SPACE, which is the '.'
        string.

        * symbols - An optional string of 81 symbols to initially fill the board
        with. EMPTY_SPACE, that is '.', can be a symbol. The symbols argument
        doesn't have to produce a valid board.

        * strict - When strict is set to True, setting a space that causes the
        board to be invalid will raise a SudokuBoard exception.
        """

        # When strict-mode is True, an exception will be raised if an illegal
        # symbol is placed on the board.
        self._strict = strict
        self.clear_board()

        if symbols is not None:
            self.symbols = symbols # use symbols property to populate _board


    @property
    def strict(self):
        return self._strict


    @strict.setter
    def strict(self, value):
        if not isinstance(value, bool):
            raise SudokuBoardException('strict must be set to a bool value')

        # Strict mode raises an exception if the board is in an invalid state,
        # so raise an acception if the board is currently invalid and strict
        # mode is enabled.
        if value and not self.is_valid_board():
            raise SudokuBoardException('strict mode enabled while board was in an invalid state')
        self._strict = value


    @property
    def symbols(self):
        """Returns a string or tuple of all symbols on the board.

        TODO"""
        all_symbols = []
        for y in range(BOARD_LENGTH):
            for x in range(BOARD_LENGTH):
                all_symbols.append(self._board[x][y])

        return ''.join(all_symbols)


    @symbols.setter
    def symbols(self, value):
        # Fill in the spaces with the provided symbols.
        if not isinstance(value, str) or len(value) != FULL_BOARD_SIZE:
            raise SudokuBoardException('symbols must be a string of 81 symbols')

        # Check that all the symbols are valid.
        for symbol in value:
            if not self.is_valid_symbol(symbol):
                raise SudokuBoardException('%r is not valid; symbols must be 1 to 9' % (repr(symbol)))

        # Place the symbol on the board.
        for i, symbol in enumerate(value):
            self._board[i % BOARD_LENGTH][i // BOARD_LENGTH] = symbol

        # If the results in an invalid board while strict mode is enabled, raise an exception.
        if self._strict and not self.is_valid_board():
            self.clear_board()
            raise SudokuBoardException('symbols results in an invalid board while strict mode is enabled')


    def clear_board(self):
        """Sets all spaces on the board to EMPTY_SPACE.
        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
        >>> board.clear_board()
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
        """
        self._board = [[EMPTY_SPACE] * BOARD_LENGTH for i in range(BOARD_LENGTH)] # create an empty board


    def is_valid_symbol(self, symbol):
        """Returns True if symbol is a str between 1 and 9, or is EMPTY_SPACE.
        Otherwise returns False.

        >>> board = SudokuBoard()
        >>> board.is_valid_symbol(1)
        True
        >>> board.is_valid_symbol('1')
        True
        >>> board.is_valid_symbol('9')
        True
        >>> board.is_valid_symbol('A')
        False
        >>> board.is_valid_symbol('01')
        False
        """
        symbol = str(symbol)
        return len(symbol) == 1 and symbol in EMPTY_SPACE + '123456789'


    def is_complete_unit(self, unit):
        """Returns True if unit is a str of all 9 symbols with no repeats.
        Otherwise returns False.

        >>> board = SudokuBoard()
        >>> board.is_complete_unit('123456789')
        True
        >>> board.is_complete_unit('987654321')
        True
        >>> board.is_complete_unit('192837465')
        True
        >>> board.is_complete_unit('111111111')
        False
        >>> board.is_complete_unit('12345678.')
        False
        >>> board.is_complete_unit('.........')
        False
        """
        if not self.is_valid_unit(unit):
            return False

        if EMPTY_SPACE in unit:
            return False

        return len(unit) == BOARD_LENGTH


    def is_valid_unit(self, unit):
        """Returns True if unit is a str of 9 symbols, which can include
        EMPTY_SPACE but doesn't have repeated symbols. Otherwise, returns
        False.

        >>> board = SudokuBoard()
        >>> board.is_valid_unit('123456789')
        True
        >>> board.is_valid_unit('987654321')
        True
        >>> board.is_valid_unit('192837465')
        True
        >>> board.is_valid_unit('111111111')
        False
        >>> board.is_valid_unit('12345678.')
        True
        >>> board.is_valid_unit('.........')
        True
        """

        # Check to make sure unit is valid.
        try:
            if len(unit) != BOARD_LENGTH:
                raise SudokuBoardException('unit must be a sequence with exactly 9 symbols, not %r' % (unit,))
        except TypeError:
            raise SudokuBoardException('unit must be a sequence with exactly 9 symbols, not %r' % (unit,))

        for symbol in unit:
            if not self.is_valid_symbol(symbol):
                raise SudokuBoardException('unit contains an invalid symbol: %r' % (symbol,))

        # Check for any repeat symbols in unit, aside from EMPTY_SPACE.
        symbolSet = set()
        for symbol in unit:
            if symbol != EMPTY_SPACE and symbol in symbolSet:
                return False
            symbolSet.add(symbol)

        return True


    def is_valid_board(self):
        """Returns True if the board is in a valid state (even if incomplete),
        otherwise return False if the board has repeated symbols set to any of
        the rows, columns, or boxes.

        >>> board = SudokuBoard(strict=False)
        >>> board.is_valid_board()
        True
        >>> board[0, 0] = 1
        >>> board[1, 0] = 1 # repeated symbol in same row
        >>> board.is_valid_board()
        False
        """

        # Check each of the columns for validity.
        for x in range(BOARD_LENGTH):
            if not self.is_valid_unit(self.get_column(x)):
                return False

        # Check each of the rows for validity.
        for y in range(BOARD_LENGTH):
            if not self.is_valid_unit(self.get_row(y)):
                return False

        # Check each of the boxes for validity.
        for top in range(BOARD_LENGTH_SQRT):
            for left in range(BOARD_LENGTH_SQRT):
                if not self.is_valid_unit(self.get_box(left, top)):
                    return False

        return True


    def is_full(self):
        """Returns True if there are no empty spaces on the board, otherwise
        returns False.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> board.is_full()
        False
        >>> board = SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
        >>> board.is_full()
        True
        >>> board = SudokuBoard(symbols='1' * 81, strict=False)
        >>> board.is_full()
        True
        """
        for x in range(BOARD_LENGTH):
            for y in range(BOARD_LENGTH):
                if self._board[x][y] == EMPTY_SPACE:
                    return False
        return True


    def is_solved(self):
        """Returns True if the board is currently solved, otherwise returns
        False.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> board.is_solved()
        False
        >>> board = SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
        >>> board.is_solved()
        True
        >>> board = SudokuBoard(symbols='1' * 81, strict=False)
        >>> board.is_solved()
        False
        """
        return self.is_full() and self.is_valid_board()


    def __getitem__(self, key):
        """Returns a single string symbol from a space on the board, as
        specified by key. They key argument can be a tuple of ints for the x
        and y coordinate of the space (with (0, 0) being the top left space) or
        a single int from 0 to 80, inclusive, where the key increases going
        right and then down.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
        >>> board[0, 0]
        '5'
        >>> board[1, 0]
        '3'
        >>> board[2, 0]
        '.'
        >>> board[0, 1]
        '6'
        >>> board[8, 8]
        '9'
        >>> board[0]
        '5'
        >>> board[1]
        '3'
        >>> board[2]
        '.'
        >>> board[9]
        '6'
        >>> board[80]
        '9'
        """

        # If the key is a single integer (used for the iterable protocol)
        if isinstance(key, int):
            if key < 0 or key >= FULL_BOARD_SIZE:
                raise SudokuBoardException('key is out of range, must be between 0 and 80, inclusive')
            return self._board[key % BOARD_LENGTH][key // BOARD_LENGTH]

        # Otherwise, if the key is a tuple or list of two ints.
        if not isinstance(key , (tuple, list)) or len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise SudokuBoardException('key must be a tuple of two integers')

        x, y = key
        if x < 0 or x >= BOARD_LENGTH:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= BOARD_LENGTH:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        return self._board[x][y]


    def __setitem__(self, key, value):
        """Sets a single string symbol from a space on the board, as
        specified by key. They key argument can be a tuple of ints for the x
        and y coordinate of the space (with (0, 0) being the top left space) or
        a single int from 0 to 80, inclusive, where the key increases going
        right and then down.

        The value argument can either be an int or a one-digit string.

        >>> board = SudokuBoard()
        >>> board[0, 0] = 5
        >>> board[1, 0] = 3
        >>> board[8, 8] = 9
        >>> print(board)
        5 3 . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . .
        ------+-------+------
        . . . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . .
        ------+-------+------
        . . . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . 9

        >>> board2 = SudokuBoard()
        >>> board2[0] = 5
        >>> board2[1] = 3
        >>> board2[80] = 9
        >>> print(board2)
        5 3 . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . .
        ------+-------+------
        . . . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . .
        ------+-------+------
        . . . | . . . | . . .
        . . . | . . . | . . .
        . . . | . . . | . . 9
        """
        # Check that the value is a valid symbol.
        if not self.is_valid_symbol(value):
            raise SudokuBoardException('%r is not a valid symbol, symbols must be int or str between 1 and 9' % (value))
        value = str(value)

        # If the key is a single integer (used for the iterable protocol)
        if isinstance(key, int):
            if key < 0 or key >= FULL_BOARD_SIZE:
                raise SudokuBoardException('key is out of range, must be between 0 and 80, inclusive')
            key = (key % BOARD_LENGTH, key // BOARD_LENGTH)

        elif not isinstance(key , tuple) or len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise SudokuBoardException('key must be a tuple of two integers')

        # Separate the x and y coordinates from key.
        x, y = key
        if x < 0 or x >= BOARD_LENGTH:
            raise SudokuBoardException('x index (%s) is out of range' % (x))
        if y < 0 or y >= BOARD_LENGTH:
            raise SudokuBoardException('y index (%s) is out of range' % (y))

        # Set the space to the new symbol.
        old_value = self._board[x][y]
        self._board[x][y] = value

        # Do a board strictness check.
        if self._strict:
            if not self.is_valid_board():
                self._board[x][y] = old_value # restore old value
                raise SudokuBoardException('strict mode is enabled, and this symbol assignment causes the board to become invalid')


    def get_row(self, row):
        """Returns a row of symbols from the board as a list of single-digit
        strings. Rows start from the top and go down.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
        >>> board.get_row(0)
        ['5', '3', '.', '.', '7', '.', '.', '.', '.']
        >>> board.get_row(1)
        ['6', '.', '.', '1', '9', '5', '.', '.', '.']
        >>> board.get_row(8)
        ['.', '.', '.', '.', '8', '.', '.', '7', '9']
        """

        if not isinstance(row, int) or row < 0 or row >= BOARD_LENGTH:
            raise SudokuBoardException('row must be an int between 0 and 8')

        return [self._board[x][row] for x in range(BOARD_LENGTH)]


    def get_column(self, column):
        """Returns a column of symbols from the board as a list of single-digit
        strings. Columns start from the left and go right.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
        >>> board.get_column(0)
        ['5', '6', '.', '8', '4', '7', '.', '.', '.']
        >>> board.get_column(1)
        ['3', '.', '9', '.', '.', '.', '6', '.', '.']
        >>> board.get_column(8)
        ['.', '.', '.', '3', '1', '6', '.', '5', '9']
        """
        if not isinstance(column, int) or column < 0 or column >= BOARD_LENGTH:
            raise SudokuBoardException('column must be an int between 0 and 8')

        return [self._board[column][y] for y in range(BOARD_LENGTH)]


    def get_box(self, box_x, box_y):
        """Returns a box of symbols from the board as a list of single-digit
        strings. boxes start at the top left and go right, then down.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
        >>> _b1.get_box(0, 0)
        ['5', '3', '.', '6', '.', '.', '.', '9', '8']
        >>> _b1.get_box(1, 0)
        ['.', '7', '.', '1', '9', '5', '.', '.', '.']
        >>> _b1.get_box(2, 0)
        ['.', '.', '.', '.', '.', '.', '.', '6', '.']
        >>> _b1.get_box(0, 1)
        ['8', '.', '.', '4', '.', '.', '7', '.', '.']
        """
        if not isinstance(box_x, int) or box_x < 0 or box_x >= BOARD_LENGTH_SQRT:
            raise SudokuBoardException('box_x must be an int between 0 and 2')

        if not isinstance(box_y, int) or box_y < 0 or box_y >= BOARD_LENGTH_SQRT:
            raise SudokuBoardException('box_y must be an int between 0 and 2')

        box = []
        start_x = box_x * BOARD_LENGTH_SQRT
        start_y = box_y * BOARD_LENGTH_SQRT
        for y in range(start_y, start_y + BOARD_LENGTH_SQRT):
            for x in range(start_x, start_x + BOARD_LENGTH_SQRT):
                box.append(self._board[x][y])

        return box


    def get_subgrid_of(self, x, y):
        """Returns the subgrid x and y coordinates based on the given space x
        and y coordinates.

        >>> board = SudokuBoard()
        >>> board.get_subgrid_of(0, 0)
        (0, 0)
        >>> board.get_subgrid_of(1, 0)
        (0, 0)
        >>> board.get_subgrid_of(3, 0)
        (1, 0)
        >>> board.get_subgrid_of(6, 6)
        (2, 2)
        >>> board.get_subgrid_of(5, 8)
        (1, 2)
        """
        return x // 3, y // 3

    def __str__(self):
        """Returns a string representation of the board. There are lines between
        the boxes but no border. It looks something like:

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> str(board)
        '5 3 . | . 7 . | . . .\\n6 . . | 1 9 5 | . . .\\n. 9 8 | . . . | . 6 .\\n------+-------+------\\n8 . . | . 6 . | . . 3\\n4 . . | 8 . 3 | . . 1\\n7 . . | . 2 . | . . 6\\n------+-------+------\\n. 6 . | . . . | 2 8 .\\n. . . | 4 1 9 | . . 5\\n. . . | . 8 . | . 7 9'
        >>> print(board)
        5 3 . | . 7 . | . . .
        6 . . | 1 9 5 | . . .
        . 9 8 | . . . | . 6 .
        ------+-------+------
        8 . . | . 6 . | . . 3
        4 . . | 8 . 3 | . . 1
        7 . . | . 2 . | . . 6
        ------+-------+------
        . 6 . | . . . | 2 8 .
        . . . | 4 1 9 | . . 5
        . . . | . 8 . | . 7 9
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
        """Returns a string that is a representation of a SudokuBoard object.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> repr(board)
        "SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79', strict=True)"
        """
        return "SudokuBoard(symbols=%r, strict=%r)" % (self.symbols, self._strict)


    def __copy__(self):
        """Returns a copy of this object."""
        board_copy = SudokuBoard(symbols=self.symbols, strict=self._strict)
        return board_copy


    def __deepcopy__(self, memo):
        """Returns a deep copy of this object (which is the same as a shallow
        copy for this class)."""
        return self.__copy__()


    def copy(self):
        """Returns a copy of this object."""
        return self.__copy__()


    def __len__(self):
        """Always returns 81, which is the number of spaces in a 9x9 sudoku
        board."""
        return FULL_BOARD_SIZE


    def __iter__(self):
        return iter(self.symbols)

    @property
    def rows(self):
        """Returns an iterator that iterates over the rows in this board.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> for unit in board.rows:
        ...     print(unit)
        ...
        ['5', '3', '.', '.', '7', '.', '.', '.', '.']
        ['6', '.', '.', '1', '9', '5', '.', '.', '.']
        ['.', '9', '8', '.', '.', '.', '.', '6', '.']
        ['8', '.', '.', '.', '6', '.', '.', '.', '3']
        ['4', '.', '.', '8', '.', '3', '.', '.', '1']
        ['7', '.', '.', '.', '2', '.', '.', '.', '6']
        ['.', '6', '.', '.', '.', '.', '2', '8', '.']
        ['.', '.', '.', '4', '1', '9', '.', '.', '5']
        ['.', '.', '.', '.', '8', '.', '.', '7', '9']
        """
        return iter([self.get_row(i) for i in range(BOARD_LENGTH)])

    @property
    def columns(self):
        """Returns an iterator that iterates over the columns in this board.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> for unit in board.columns:
        ...     print(unit)
        ...
        ['5', '6', '.', '8', '4', '7', '.', '.', '.']
        ['3', '.', '9', '.', '.', '.', '6', '.', '.']
        ['.', '.', '8', '.', '.', '.', '.', '.', '.']
        ['.', '1', '.', '.', '8', '.', '.', '4', '.']
        ['7', '9', '.', '6', '.', '2', '.', '1', '8']
        ['.', '5', '.', '.', '3', '.', '.', '9', '.']
        ['.', '.', '.', '.', '.', '.', '2', '.', '.']
        ['.', '.', '6', '.', '.', '.', '8', '.', '7']
        ['.', '.', '.', '3', '1', '6', '.', '5', '9']
        """
        return iter([self.get_column(i) for i in range(BOARD_LENGTH)])

    @property
    def boxes(self):
        """Returns an iterator that iterates over the boxes in this board.

        >>> board = SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
        >>> for unit in board.boxes:
        ...     print(unit)
        ...
        ['5', '3', '.', '6', '.', '.', '.', '9', '8']
        ['.', '7', '.', '1', '9', '5', '.', '.', '.']
        ['.', '.', '.', '.', '.', '.', '.', '6', '.']
        ['8', '.', '.', '4', '.', '.', '7', '.', '.']
        ['.', '6', '.', '8', '.', '3', '.', '2', '.']
        ['.', '.', '3', '.', '.', '1', '.', '.', '6']
        ['.', '6', '.', '.', '.', '.', '.', '.', '.']
        ['.', '.', '.', '4', '1', '9', '.', '8', '.']
        ['2', '8', '.', '.', '.', '5', '.', '7', '9']
        """
        return iter([self.get_box(i % BOARD_LENGTH_SQRT, i // BOARD_LENGTH_SQRT) for i in range(BOARD_LENGTH)])


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
