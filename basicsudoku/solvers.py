import copy
import os
import sys
import time


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from basicsudoku import SudokuBoard, SudokuBoardException, BOARD_LENGTH, BOARD_LENGTH_SQRT, EMPTY_SPACE, FULL_BOARD_SIZE


class BasicSolver(object):
    def __init__(self, board):
        self.board = board
        self.solve()


    def solve(self):
        """Solve the sudoku puzzle as given in self.board, which is set to a
        SudokuBoard object passed to __init__(). Returns True if a solution is
        found, otherwise returns False.

        There are two steps to solving. First, the possible candidates are
        narrowed down based on the given symbols that the board starts with.

        Second, the remaining possible candidates are searched through until
        a solution is found. Multiple solutions are not detected; the first
        solution found is the one returned. It is important to check the spaces
        with the fewest candidates first, to cut down on the total number of
        combinations that need to be searched.
        """

        start_time = time.time()

        # Each of the 81 spaces on the board has a set of all 9 symbols as
        # candidates for the real symbol that belongs at that space. When this
        # list is reduced to one symbol, we know we've solved that space.
        board_candidates = [[set('123456789') for j in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]

        # Remove the given symbols that the board started with.
        self.remove_givens_from_board_candidates(board_candidates)

        # Search through all the remaining possibilities.
        solution_symbols = self.solve_through_search(board_candidates)

        self.last_solve_time = time.time() - start_time

        if solution_symbols is not None:
            # A solution was found, mark all the symbols on the board object.
            self.board.symbols = solution_symbols
            return True
        else:
            return False


    def remove_givens_from_board_candidates(self, board_candidates):
        """Remove the givens from all peer spaces. This function modifies
        board_candidates in place."""
        for x in range(BOARD_LENGTH):
            for y in range(BOARD_LENGTH):
                symbol = self.board[x, y]
                if symbol != EMPTY_SPACE:
                    self.set_symbol(symbol, board_candidates, x, y)


    def set_symbol(self, symbol, board_candidates, symbol_x, symbol_y):
        """Set the symbol on the solver's SudokuBoard object, then remove that
        symbol from all the peers of the space at symbol_x symbol_y. This may
        cause other spaces to become solved, which will then call set_symbol()
        again. This function modifies board_candidates in palce."""
        symbol = str(symbol)
        board_candidates[symbol_x][symbol_y] = set(symbol) # ensure that the board_candidates only have this symbol here
        self.remove_from_peers(symbol, board_candidates, symbol_x, symbol_y)


    def remove_from_peers(self, candidate, board_candidates, candidate_x, candidate_y):
        """Remove the candidate from the peer spaces of candidate_x candidate_y
        in board_candidates. This function modifies board_candidates in place."""
        candidate = str(candidate)

        # Remove candidate from the row of the xy space.
        for x in range(BOARD_LENGTH):
            if x != candidate_x:
                self.remove_candidate(board_candidates, candidate, x, candidate_y)

        # Remove candidate from the column of the xy space.
        for y in range(BOARD_LENGTH):
            if y != candidate_y:
                self.remove_candidate(board_candidates, candidate, candidate_x, y)

        # Remove candidate from the box of the xy space.
        box_x, box_y = candidate_x // 3, candidate_y // 3 # Get the top left space of the box.
        start_x = box_x * BOARD_LENGTH_SQRT
        start_y = box_y * BOARD_LENGTH_SQRT
        for y in range(start_y, start_y + BOARD_LENGTH_SQRT):
            for x in range(start_x, start_x + BOARD_LENGTH_SQRT):
                if x != candidate_x and y != candidate_y:
                    self.remove_candidate(board_candidates, candidate, x, y)


    def remove_candidate(self, board_candidates, candidate, x, y):
        """Removes the candidate symbol from board_candidates at the x y space. This
         function modifies board_candidates in place."""

        if candidate in board_candidates[x][y]:
            board_candidates[x][y].remove(candidate)
            if len(board_candidates[x][y]) == 1:
                # There is only one possible candidate for this space, menaing
                # we've solved another space. Remove the symbol from the space's
                # peers.
                remaining_symbol = tuple(board_candidates[x][y])[0]
                self.set_symbol(remaining_symbol, board_candidates, x, y)
            elif len(board_candidates[x][y]) == 0:
                raise SudokuBoardException('removing this candidate causes the board to be invalid')


    def solve_through_search(self, board_candidates):
        """Attempts a brute-force search of the possible solutions for the
        board, and returns when found."""

        # Check the space with the fewest candidates, to minimize the overall
        # number of checks needed. (Don't include spaces that only have one
        # candidate, i.e. spaces that are solved.)
        order_of_spaces_to_check = [i for i in range(FULL_BOARD_SIZE) if len(board_candidates[i % BOARD_LENGTH][i // BOARD_LENGTH]) != 1]
        order_of_spaces_to_check.sort(key=lambda i: len(board_candidates[i % BOARD_LENGTH][i // BOARD_LENGTH]), reverse=False)
        if len(order_of_spaces_to_check) == 0:
            # All the spaces have been solved, so lets just return the symbols that they form.
            return self.make_board_from_candidates(board_candidates).symbols
        space_to_check = order_of_spaces_to_check[0]

        x, y = space_to_check % BOARD_LENGTH, space_to_check // BOARD_LENGTH
        candidates = board_candidates[x][y]

        assert len(candidates) > 0, 'board_candidates[%s][%s] has no candidates, which should never happen' % (x, y)

        # Loop through all possible candidates for this space.
        for candidate in candidates:
            # This function is recursive, and testing each candidate in each
            # call will need its own board_candidates.
            board_candidates_copy = copy.deepcopy(board_candidates)

            # Set this candidate as the only possible candidate in the copy
            # of board_candidates, then test to see if the board it produces
            # is valid.
            board_candidates_copy[x][y] = set(candidate)
            try:
                self.remove_from_peers(candidate, board_candidates_copy, x, y)
            except SudokuBoardException:
                # Removing that candidate from the peers has caused a space to
                # have zero candidates, meaning the board will be in an invalid
                # state. So this candidate cannot be the solution and we should
                # move on to the next candidate.
                continue

            board = self.make_board_from_candidates(board_candidates_copy)
            if not board.is_valid_board():
                # This candidate causes the board to become invalid, so this is
                # not the correct solution for this space. Continue on to the
                # next candidate.
                continue

            # If the board is both valid and full, the whole board is solved.
            if board.is_full():
                return board.symbols # BASE CASE

            # Continue searching.
            result = self.solve_through_search(board_candidates_copy) # RECUSIVE CASE
            if result is not None:
                return result # BASE CASE

        # Exhausted all possible candidates and could not find a solution.
        return None # BASE CASE


    def make_board_from_candidates(self, board_candidates):
        """Returns a SudokuBoard object, with the symbols set wherever the
        board_candidates have only one possible candidate."""
        symbols = []
        for i in range(FULL_BOARD_SIZE):
            x, y = i % BOARD_LENGTH, i // BOARD_LENGTH

            assert len(board_candidates[x][y]) > 0, 'Somehow board_candidates at x %s, y %s has no candidates.' % (x, y)

            if len(board_candidates[x][y]) == 1:
                # If there is only one candidate, add it to the symbols list.
                the_one_possible_candidate = tuple(board_candidates[x][y])[0]
                symbols.append(the_one_possible_candidate)
            else:
                # If there are multiple candidates, mark it as an empty space.
                symbols.append(EMPTY_SPACE)

        return SudokuBoard(symbols=''.join(symbols), strict=False)


# Example usage of solving a board:
# import basicsudoku
# print(basicsudoku._b1)
# BasicSolver(basicsudoku._b1).solve()
# print(basicsudoku._b1)