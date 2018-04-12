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


    def get_box_of(self, x, y):
        """Returns the box x and y coordinates based on the given space x
        and y coordinates.

        >>> board = SudokuBoard()
        >>> board.get_box_of(0, 0)
        (0, 0)
        >>> board.get_box_of(1, 0)
        (0, 0)
        >>> board.get_box_of(3, 0)
        (1, 0)
        >>> board.get_box_of(6, 6)
        (2, 2)
        >>> board.get_box_of(5, 8)
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


# Some sample puzzles from Peter Norvig's http://norvig.com/sudoku.html

easy50 = '''..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..
2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3
......9.7...42.18....7.5.261..9.4....5.....4....5.7..992.1.8....34.59...5.7......
.3..5..4...8.1.5..46.....12.7.5.2.8....6.3....4.1.9.3.25.....98..1.2.6...8..6..2.
.2.81.74.7....31...9...28.5..9.4..874..2.8..316..3.2..3.27...6...56....8.76.51.9.
1..92....524.1...........7..5...81.2.........4.27...9..6...........3.945....71..6
.43.8.25.6.............1.949....4.7....6.8....1.2....382.5.............5.34.9.71.
48...69.2..2..8..19..37..6.84..1.2....37.41....1.6..49.2..85..77..9..6..6.92...18
...9....2.5.1234...3....16.9.8.......7.....9.......2.5.91....5...7439.2.4....7...
..19....39..7..16..3...5..7.5......9..43.26..2......7.6..1...3..42..7..65....68..
...1254....84.....42.8......3.....95.6.9.2.1.51.....6......3.49.....72....1298...
.6234.75.1....56..57.....4.....948..4.......6..583.....3.....91..64....7.59.8326.
3..........5..9...2..5.4....2....7..16.....587.431.6.....89.1......67.8......5437
63..........5....8..5674.......2......34.1.2.......345.....7..4.8.3..9.29471...8.
....2..4...8.35.......7.6.2.31.4697.2...........5.12.3.49...73........1.8....4...
361.259...8.96..1.4......57..8...471...6.3...259...8..74......5.2..18.6...547.329
.5.8.7.2.6...1..9.7.254...6.7..2.3.15.4...9.81.3.8..7.9...762.5.6..9...3.8.1.3.4.
.8...5........3457....7.8.9.6.4..9.3..7.1.5..4.8..7.2.9.1.2....8423........1...8.
..35.29......4....1.6...3.59..251..8.7.4.8.3.8..763..13.8...1.4....2......51.48..
...........98.51...519.742.29.4.1.65.........14.5.8.93.267.958...51.36...........
.2..3..9....9.7...9..2.8..5..48.65..6.7...2.8..31.29..8..6.5..7...3.9....3..2..5.
..5.....6.7...9.2....5..1.78.415.......8.3.......928.59.7..6....3.4...1.2.....6..
.4.....5...19436....9...3..6...5...21.3...5.68...2...7..5...2....24367...3.....4.
..4..........3...239.7...8.4....9..12.98.13.76..2....8.1...8.539...4..........8..
36..2..89...361............8.3...6.24..6.3..76.7...1.8............418...97..3..14
5..4...6...9...8..64..2.........1..82.8...5.17..5.........9..84..3...6...6...3..2
..72564..4.......5.1..3..6....5.8.....8.6.2.....1.7....3..7..9.2.......4..63127..
..........79.5.18.8.......7..73.68..45.7.8.96..35.27..7.......5.16.3.42..........
.3.....8...9...5....75.92..7..1.5..8.2..9..3.9..4.2..1..42.71....2...8...7.....9.
2..17.6.3.5....1.......6.79....4.7.....8.1.....9.5....31.4.......5....6.9.6.37..2
.......8.8..7.1.4..4..2..3.374...9......3......5...321.1..6..5..5.8.2..6.8.......
.......85...21...996..8.1..5..8...16.........89...6..7..9.7..523...54...48.......
6.8.7.5.2.5.6.8.7...2...3..5...9...6.4.3.2.5.8...5...3..5...2...1.7.4.9.4.9.6.7.1
.5..1..4.1.7...6.2...9.5...2.8.3.5.1.4..7..2.9.1.8.4.6...4.1...3.4...7.9.2..6..1.
.53...79...97534..1.......2.9..8..1....9.7....8..3..7.5.......3..76412...61...94.
..6.8.3...49.7.25....4.5...6..317..4..7...8..1..826..9...7.2....75.4.19...3.9.6..
..5.8.7..7..2.4..532.....84.6.1.5.4...8...5...7.8.3.1.45.....916..5.8..7..3.1.6..
...9..8..128..64...7.8...6.8..43...75.......96...79..8.9...4.1...36..284..1..7...
....8....27.....54.95...81...98.64...2.4.3.6...69.51...17...62.46.....38....9....
...6.2...4...5...1.85.1.62..382.671...........194.735..26.4.53.9...2...7...8.9...
...9....2.5.1234...3....16.9.8.......7.....9.......2.5.91....5...7439.2.4....7...
38..........4..785..9.2.3...6..9....8..3.2..9....4..7...1.7.5..495..6..........92
...158.....2.6.8...3.....4..27.3.51...........46.8.79..5.....8...4.7.1.....325...
.1.5..2..9....1.....2..8.3.5...3...7..8...5..6...8...4.4.1..7.....7....6..3..4.5.
.8.....4....469...4.......7..59.46...7.6.8.3...85.21..9.......5...781....6.....1.
9.42....7.1..........7.65.....8...9..2.9.4.6..4...2.....16.7..........3.3....57.2
...7..8....6....31.4...2....24.7.....1..3..8.....6.29....8...7.86....5....2..6...
..1..7.9.59..8...1.3.....8......58...5..6..2...41......8.....3.1...2..79.2.7..4..
.....3.17.15..9..8.6.......1....7.....9...2.....5....4.......2.5..6..34.34.2.....
3..2........1.7...7.6.3.5...7...9.8.9...2...4.1.8...5...9.4.3.1...7.2........8..6'''.split('\n')

top95 = '''4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
52...6.........7.13...........4..8..6......5...........418.........3..2...87.....
6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1....
48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....
....14....3....2...7..........9...3.6.1.............8.2.....1.4....5.6.....7.8...
......52..8.4......3...9...5.1...6..2..7........3.....6...1..........7.4.......3.
6.2.5.........3.4..........43...8....1....2........7..5..27...........81...6.....
.524.........7.1..............8.2...3.....6...9.5.....1.6.3...........897........
6.2.5.........4.3..........43...8....1....2........7..5..27...........81...6.....
.923.........8.1...........1.7.4...........658.........6.5.2...4.....7.....9.....
6..3.2....5.....1..........7.26............543.........8.15........4.2........7..
.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...
..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..
3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....
1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......
6..3.2....4.....1..........7.26............543.........8.15........4.2........7..
....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.
45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..
.237....68...6.59.9.....7......4.97.3.7.96..2.........5..47.........2....8.......
..84...3....3.....9....157479...8........7..514.....2...9.6...2.5....4......9..56
.98.1....2......6.............3.2.5..84.........6.........4.8.93..5...........1..
..247..58..............1.4.....2...9528.9.4....9...1.........3.3....75..685..2...
4.....8.5.3..........7......2.....6.....5.4......1.......6.3.7.5..2.....1.9......
.2.3......63.....58.......15....9.3....7........1....8.879..26......6.7...6..7..4
1.....7.9.4...72..8.........7..1..6.3.......5.6..4..2.........8..53...7.7.2....46
4.....3.....8.2......7........1...8734.......6........5...6........1.4...82......
.......71.2.8........4.3...7...6..5....2..3..9........6...7.....8....4......5....
6..3.2....4.....8..........7.26............543.........8.15........8.2........7..
.47.8...1............6..7..6....357......5....1..6....28..4.....9.1...4.....2.69.
......8.17..2........5.6......7...5..1....3...8.......5......2..4..8....6...3....
38.6.......9.......2..3.51......5....3..1..6....4......17.5..8.......9.......7.32
...5...........5.697.....2...48.2...25.1...3..8..3.........4.7..13.5..9..2...31..
.2.......3.5.62..9.68...3...5..........64.8.2..47..9....3.....1.....6...17.43....
.8..4....3......1........2...5...4.69..1..8..2...........3.9....6....5.....2.....
..8.9.1...6.5...2......6....3.1.7.5.........9..4...3...5....2...7...3.8.2..7....4
4.....5.8.3..........7......2.....6.....5.8......1.......6.3.7.5..2.....1.8......
1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......
1....6.8..64..........4...7....9.6...7.4..5..5...7.1...5....32.3....8...4........
249.6...3.3....2..8.......5.....6......2......1..4.82..9.5..7....4.....1.7...3...
...8....9.873...4.6..7.......85..97...........43..75.......3....3...145.4....2..1
...5.1....9....8...6.......4.1..........7..9........3.8.....1.5...2..4.....36....
......8.16..2........7.5......6...2..1....3...8.......2......7..3..8....5...4....
.476...5.8.3.....2.....9......8.5..6...1.....6.24......78...51...6....4..9...4..7
.....7.95.....1...86..2.....2..73..85......6...3..49..3.5...41724................
.4.5.....8...9..3..76.2.....146..........9..7.....36....1..4.5..6......3..71..2..
.834.........7..5...........4.1.8..........27...3.....2.6.5....5.....8........1..
..9.....3.....9...7.....5.6..65..4.....3......28......3..75.6..6...........12.3.8
.26.39......6....19.....7.......4..9.5....2....85.....3..2..9..4....762.........4
2.3.8....8..7...........1...6.5.7...4......3....1............82.5....6...1.......
6..3.2....1.....5..........7.26............843.........8.15........8.2........7..
1.....9...64..1.7..7..4.......3.....3.89..5....7....2.....6.7.9.....4.1....129.3.
.........9......84.623...5....6...453...1...6...9...7....1.....4.5..2....3.8....9
.2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5
9.4..5...25.6..1..31......8.7...9...4..26......147....7.......2...3..8.6.4.....9.
...52.....9...3..4......7...1.....4..8..453..6...1...87.2........8....32.4..8..1.
53..2.9...24.3..5...9..........1.827...7.........981.............64....91.2.5.43.
1....786...7..8.1.8..2....9........24...1......9..5...6.8..........5.9.......93.4
....5...11......7..6.....8......4.....9.1.3.....596.2..8..62..7..7......3.5.7.2..
.47.2....8....1....3....9.2.....5...6..81..5.....4.....7....3.4...9...1.4..27.8..
......94.....9...53....5.7..8.4..1..463...........7.8.8..7.....7......28.5.26....
.2......6....41.....78....1......7....37.....6..412....1..74..5..8.5..7......39..
1.....3.8.6.4..............2.3.1...........758.........7.5...6.....8.2...4.......
2....1.9..1..3.7..9..8...2.......85..6.4.........7...3.2.3...6....5.....1.9...2.5
..7..8.....6.2.3...3......9.1..5..6.....1.....7.9....2........4.83..4...26....51.
...36....85.......9.4..8........68.........17..9..45...1.5...6.4....9..2.....3...
34.6.......7.......2..8.57......5....7..1..2....4......36.2..1.......9.......7.82
......4.18..2........6.7......8...6..4....3...1.......6......2..5..1....7...3....
.4..5..67...1...4....2.....1..8..3........2...6...........4..5.3.....8..2........
.......4...2..4..1.7..5..9...3..7....4..6....6..1..8...2....1..85.9...6.....8...3
8..7....4.5....6............3.97...8....43..5....2.9....6......2...6...7.71..83.2
.8...4.5....7..3............1..85...6.....2......4....3.26............417........
....7..8...6...5...2...3.61.1...7..2..8..534.2..9.......2......58...6.3.4...1....
......8.16..2........7.5......6...2..1....3...8.......2......7..4..8....5...3....
.2..........6....3.74.8.........3..2.8..4..1.6..5.........1.78.5....9..........4.
.52..68.......7.2.......6....48..9..2..41......1.....8..61..38.....9...63..6..1.9
....1.78.5....9..........4..2..........6....3.74.8.........3..2.8..4..1.6..5.....
1.......3.6.3..7...7...5..121.7...9...7........8.1..2....8.64....9.2..6....4.....
4...7.1....19.46.5.....1......7....2..2.3....847..6....14...8.6.2....3..6...9....
......8.17..2........5.6......7...5..1....3...8.......5......2..3..8....6...4....
963......1....8......2.5....4.8......1....7......3..257......3...9.2.4.7......9..
15.3......7..4.2....4.72.....8.........9..1.8.1..8.79......38...........6....7423
..........5724...98....947...9..3...5..9..12...3.1.9...6....25....56.....7......6
....75....1..2.....4...3...5.....3.2...8...1.......6.....1..48.2........7........
6.....7.3.4.8.................5.4.8.7..2.....1.3.......2.....5.....7.9......1....
....6...4..6.3....1..4..5.77.....8.5...8.....6.8....9...2.9....4....32....97..1..
.32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6.
...5.3.......6.7..5.8....1636..2.......4.1.......3...567....2.8..4.7.......2..5..
.5.3.7.4.1.........3.......5.8.3.61....8..5.9.6..1........4...6...6927....2...9..
..5..8..18......9.......78....4.....64....9......53..2.6.........138..5....9.714.
..........72.6.1....51...82.8...13..4.........37.9..1.....238..5.4..9.........79.
...658.....4......12............96.7...3..5....2.8...3..19..8..3.6.....4....473..
.2.3.......6..8.9.83.5........2...8.7.9..5........6..4.......1...1...4.22..7..8.9
.5..9....1.....6.....3.8.....8.4...9514.......3....2..........4.8...6..77..15..6.
.....2.......7...17..3...9.8..7......2.89.6...13..6....9..5.824.....891..........
3...8.......7....51..............36...2..4....7...........6.13..452...........8..'''.split('\n')

hardest = '''85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.
..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..
12..4......5.69.1...9...5.........7.7...52.9..3......2.9.6...5.4..9..8.1..3...9.4
...57..3.1......2.7...234......8...4..7..4...49....6.5.42...3.....7..9....18.....
7..1523........92....3.....1....47.8.......6............9...5.6.4.9.7...8....6.1.
1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3..
1...34.8....8..5....4.6..21.18......3..1.2..6......81.52..7.9....6..9....9.64...2
...92......68.3...19..7...623..4.1....1...7....8.3..297...8..91...5.72......64...
.6.5.4.3.1...9...8.........9...5...6.4.6.2.7.7...4...5.........4...8...1.5.2.3.4.
7.....4...2..7..8...3..8.799..5..3...6..2..9...1.97..6...3..9...3..4..6...9..1.35
....7..2.8.......6.1.2.5...9.54....8.........3....85.1...3.2.8.4.......9.7..6....'''.split('\n')

if __name__ == '__main__':
    doctest.testmod()
