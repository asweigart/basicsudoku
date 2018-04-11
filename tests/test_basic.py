from __future__ import division, print_function

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import basicsudoku

runningOnPython2 = sys.version_info[0] == 2


def test_ctor():
    # Test the basic constructor.
    board = basicsudoku.SudokuBoard()
    assert board.get_symbols() == '.................................................................................'

    # Test with default values for the keyword arguments.
    board = basicsudoku.SudokuBoard(symbols=None, strict=True, solved=False)
    assert board.get_symbols() == '.................................................................................'

    # Test with default values for the keyword arguments.
    board = basicsudoku.SudokuBoard(None, True, False)
    assert board.get_symbols() == '.................................................................................'
    assert board.strict == True
    #assert board.is_solved() == True


def test_ctor_symbols_arg():
    # Test the `symbols` keyword argument.
    board = basicsudoku.SudokuBoard(symbols='.................................................................................')
    assert board.get_symbols() == '.................................................................................'

    # Test the EMPTY_SPACE constant is '.'
    board = basicsudoku.SudokuBoard(symbols=basicsudoku.EMPTY_SPACE * 81)
    assert board.get_symbols() == '.' * 81

    # Test with full, real symbols.
    board = basicsudoku.SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
    assert board.get_symbols() == '534678912672195348198342567859761423426853791713924856961537284287419635345286179'

    # Test with partial, real symbols.
    board = basicsudoku.SudokuBoard(symbols='4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
    assert board.get_symbols() == '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    # Test too few symbols.
    with pytest.raises(basicsudoku.SudokuBoardException):
        basicsudoku.SudokuBoard(symbols='...')

    # Test too many symbols.
    with pytest.raises(basicsudoku.SudokuBoardException):
        basicsudoku.SudokuBoard(symbols='.................................................................................1')

    # Test invalid symbols.
    with pytest.raises(basicsudoku.SudokuBoardException):
        basicsudoku.SudokuBoard(symbols='X................................................................................')


def test_ctor_strict_arg():
    # Strict mode enabled.
    board = basicsudoku.SudokuBoard(strict=True)
    board[0, 0] = '1'

    # Setting an invalid symbol should raise an exception.
    with pytest.raises(basicsudoku.SudokuBoardException):
        board[0, 1] = '1'

    # Strict mode disabled.
    board = basicsudoku.SudokuBoard(strict=False)
    board[0, 0] = '1'
    board[0, 1] = '1'

    # Strict mode enabled raises an exception for invalid symbols argument.
    with pytest.raises(basicsudoku.SudokuBoardException):
        basicsudoku.SudokuBoard(symbols='1' * 81, strict=True)


def test_ctor_solved_arg():
    pass
    #board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79', solved=True)
    #assert board.get_symbols() == '534678912672195348198342567859761423426853791713924856961537284287419635345286179'


def test_get_set():
    board = basicsudoku.SudokuBoard()
    assert board[0, 0] == basicsudoku.EMPTY_SPACE

    board[0, 0] = 1
    assert board[0, 0] == '1'

    board[0, 0] = '1'
    assert board[0, 0] == '1'

    with pytest.raises(basicsudoku.SudokuBoardException):
        board[9, 0] = '1'

    with pytest.raises(basicsudoku.SudokuBoardException):
        board[0, 9] = '1'

    with pytest.raises(basicsudoku.SudokuBoardException):
        board[0, 0] = '10'


def test_is_valid_symbol():
    board = basicsudoku.SudokuBoard()
    assert board.is_valid_symbol('1') == True
    assert board.is_valid_symbol('9') == True
    assert board.is_valid_symbol('16') == False
    assert board.is_valid_symbol('X') == False


def test_is_complete_group():
    board = basicsudoku.SudokuBoard()
    assert board.is_complete_group('123456789') == True # complete group
    assert board.is_complete_group('987654321') == True # complete group, different order
    assert board.is_complete_group('112345678') == False # repeated '1' symbol
    assert board.is_complete_group('12345678.') == False # empty space

    # Passing a non-string for the group
    with pytest.raises(basicsudoku.SudokuBoardException):
        board.is_complete_group(42)

    # Test too few symbols in group.
    with pytest.raises(basicsudoku.SudokuBoardException):
        board.is_complete_group('123')

    # Test too many symbols in group.
    with pytest.raises(basicsudoku.SudokuBoardException):
        board.is_complete_group('1234567890')


def test_is_valid_board():
    board = basicsudoku.SudokuBoard(strict=False)
    assert board.is_valid_board() == True

    board[0, 0] = '1'
    assert board.is_valid_board() == True

    # Test putting the same symbol in the same row.
    board[8, 0] = '1'
    assert board.is_valid_board() == False

    # Test putting the same symbol in the same subgrid.
    board[8, 0] = basicsudoku.EMPTY_SPACE
    board[0, 1] = '1'
    assert board.is_valid_board() == False

    # Test putting the same symbol in the same column.
    board[0, 1] = basicsudoku.EMPTY_SPACE
    board[0, 8] = '1'
    assert board.is_valid_board() == False

    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.is_valid_board() == True

    board = basicsudoku.SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
    assert board.is_valid_board() == True


def test_is_full():
    board = basicsudoku.SudokuBoard()
    assert board.is_full() == False

    board[0, 0] = '1'
    assert board.is_full() == False

    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.is_full() == False

    board = basicsudoku.SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
    assert board.is_full() == True

    board[0, 0] = basicsudoku.EMPTY_SPACE
    assert board.is_full() == False


def test_is_solved():
    board = basicsudoku.SudokuBoard()
    assert board.is_solved() == False

    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.is_solved() == False

    board = basicsudoku.SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179')
    assert board.is_solved() == True


def test_get_row():
    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.get_row(0) == ['5', '3', '.', '.', '7', '.', '.', '.', '.']
    assert board.get_row(1) == ['6', '.', '.', '1', '9', '5', '.', '.', '.']
    assert board.get_row(2) == ['.', '9', '8', '.', '.', '.', '.', '6', '.']

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_row(0.0)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_row(-1)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_row(9)


def test_get_column():
    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.get_column(0) == ['5', '6', '.', '8', '4', '7', '.', '.', '.']
    assert board.get_column(1) == ['3', '.', '9', '.', '.', '.', '6', '.', '.']
    assert board.get_column(2) == ['.', '.', '8', '.', '.', '.', '.', '.', '.']

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_column(0.0)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_column(-1)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_column(9)


def test_get_subgrid():
    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.get_subgrid(0, 0) == ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    assert board.get_subgrid(0, 1) == ['8', '.', '.', '4', '.', '.', '7', '.', '.']
    assert board.get_subgrid(1, 0) == ['.', '7', '.', '1', '9', '5', '.', '.', '.']

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_subgrid(0.0 , 0)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_subgrid(0, 0.0)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_subgrid(-1 , 0)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_subgrid(0, 3)

    with pytest.raises(basicsudoku.SudokuBoardException):
        board.get_subgrid(3, 0)


def test_get_symbols():
    # Test an empty board.
    board = basicsudoku.SudokuBoard()
    assert board.get_symbols() == '.' * 81

    # Test a board with a few symbols set.
    board[0, 0] = '1'
    board[1, 0] = '2'
    board[8, 8] = '3'
    assert board.get_symbols() == '12.......' + ('.' * 63) + '........3'

    # Test a partially filled-in board.
    board = basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    assert board.get_symbols() == '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'

    # Test a completely filled-in but invalid board.
    board = basicsudoku.SudokuBoard(symbols='1' * 81, strict=False)
    assert board.get_symbols() == '1' * 81


def test_str():
    s = str(basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'))
    assert s == """5 3 . | . 7 . | . . .
6 . . | 1 9 5 | . . .
. 9 8 | . . . | . 6 .
------+-------+------
8 . . | . 6 . | . . 3
4 . . | 8 . 3 | . . 1
7 . . | . 2 . | . . 6
------+-------+------
. 6 . | . . . | 2 8 .
. . . | 4 1 9 | . . 5
. . . | . 8 . | . 7 9"""

    s = str(basicsudoku.SudokuBoard(symbols='534678912672195348198342567859761423426853791713924856961537284287419635345286179'))
    assert s == """5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+------
8 5 9 | 7 6 1 | 4 2 3
4 2 6 | 8 5 3 | 7 9 1
7 1 3 | 9 2 4 | 8 5 6
------+-------+------
9 6 1 | 5 3 7 | 2 8 4
2 8 7 | 4 1 9 | 6 3 5
3 4 5 | 2 8 6 | 1 7 9"""


def test_repr():
    r = repr(basicsudoku.SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'))
    assert r == "SudokuBoard(symbols='53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')"


if __name__ == '__main__':
    pytest.main()
