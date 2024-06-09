import itertools
import operator as op
import time
from exceptions.malformed import MalformedSudoku
import copy
from structures.namedtuples import EmptyPosition, Position

class SudokuSolver:
    NUMBERS = set(range(1, 10))

    TOTAL_LINES = 9

    QUADRANT_DEFINITION = [
        (range(i, i + 3), range(j, j + 3))
        for i, j in itertools.product(range(0, 9, 3), repeat=2)
    ]
    
    
    def __init__(self, original_sudoku: list[list]):
        self.original_sudoku = original_sudoku
        self.execution_time = None


    def print_sudoku(self, first_sudoku, current_sudoku):
        """Print last and current sudoku

        Args:
            first_sudoku (_type_): Sudoku to be modified
            current_sudoku (_type_): Current sudoku solution
        """

        total_empty = len(self.get_empty_positions(current_sudoku))
        (
            print("Sudoku resolvido!")
            if not total_empty
            else print("Sudoku não resolvido!")
        )

        print("Original -> Atual")
        for i in range(self.TOTAL_LINES):
            print(f"{first_sudoku[i]} -> {current_sudoku[i]}")

        print(f"Posições vazias: {total_empty}")

    def find_quadrant(self, i: int, j: int) -> tuple[range, range]:
        """
        Find quadrant by i,j matrix position

        Args:
            i (int): Line position
            j (int): Column position

        Returns:
            tuple[range, range]: Ranges to find all quadrant numbers
        """
        return next(
            (
                quadrant
                for quadrant in self.QUADRANT_DEFINITION
                if i in quadrant[0] and j in quadrant[1]
            )
        )

    def get_column_numbers(self, sudoku, column) -> set[int]:
        """Get column numbers

        Args:
            sudoku (_type_): Sudoku
            column (_type_): Column number

        Returns:
            set[int]: Set of all column numbers
        """
        return (
            sudoku[i][column]
            for i in range(0, self.TOTAL_LINES)
            if sudoku[i][column] != 0
        )

    @staticmethod
    def get_line_numbers(sudoku, line):
        """Return all line numbers

        Args:
            sudoku (_type_): Sudoku
            line (_type_): Line position

        Returns:
            _type_: All non zero numbers from line
        """
        return filter(lambda x: x, sudoku[line])

    @staticmethod
    def get_quadrant_numbers(sudoku: list[list], quadrant: tuple[range, range]) -> dict:
        """Return set with all quadrant numbers

        Args:
            sudoku (list[list]): Sudoku to find numbers
            quadrant (tuple[range, range]): Positions to find numbers

        Returns:
            set[int]: Set with all quadrant numbers
        """
        return {
            sudoku[i][j] for i, j in itertools.product(*quadrant) if sudoku[i][j] != 0
        }

    def find_existing_numbers(self, sudoku: list[list], i: int, j: int) -> set[int]:
        """Find all existing numbers based on i, j sudoku position


        Args:
            sudoku (list[list]): Sudoku to find numbers
            i (int): Line position
            j (int): Column position

        Returns:
            set[int]: All existing numbers from quadrant, line and column
        """
        quadrant_numbers: set[int] = self.get_quadrant_numbers(
            sudoku, self.find_quadrant(i, j)
        )
        line_numbers: set[int] = self.get_line_numbers(sudoku, i)
        column_numbers: set[int] = self.get_column_numbers(sudoku, j)

        existing_numbers = (
            set(quadrant_numbers) | set(line_numbers) | set(column_numbers)
        )

        return set(filter(lambda x: x, existing_numbers))

    def get_empty_positions(self, sudoku: list[list]) -> list[EmptyPosition]:
        """Get unfilled values from sudoku

        Args:
            sudoku (list[list]): Original sudoku

        Returns:
            list[EmptyPosition]: List of positions unfilled
        """
        empty_positions = {}
        return {
            (i, j): {}
            for i in range(self.TOTAL_LINES)
            for j in range(len(sudoku[i]))
            if sudoku[i][j] == 0
        }

    def line_exclusion_inference(
        self, sudoku, i, quadrant, other_positions, possible_numbers
    ):
        """Sudoku technique for line exclusion em number

        Args:
            sudoku (_type_): Sudoku
            i (_type_): Line
            quadrant (_type_): Quadrant description
            other_positions (_type_): Other positions from quadrant
            possible_numbers (_type_): All possible numbers from empty position

        Returns:
            Optional int: Chosen number if possible, else None
        """
        chosen_number = None
        line_positions_filled = [
            column for line, column in other_positions if line == i
        ]

        if len(line_positions_filled) == 2:
            lines_to_verify = [line for line in quadrant[0] if line != i]

            # Check each possible number
            for existing_number in possible_numbers:
                exists_on_first_line = existing_number in sudoku[lines_to_verify[0]]
                exists_on_second_line = existing_number in sudoku[lines_to_verify[1]]

                if exists_on_first_line and exists_on_second_line:
                    chosen_number = existing_number
                    break

        return chosen_number

    def column_exclusion_inference(
        self, sudoku, j, quadrant, other_positions, possible_numbers
    ):
        """Sudoku technique for column exclusion em number

        Args:
            sudoku (list[list]): Sudoku
            j (int): Line
            quadrant (tuple): Quadrant description
            other_positions (list): Other positions from quadrant
            possible_numbers (set): All possible numbers from empty position

        Returns:
            Optional int: Chosen number if possible, else None
        """
        chosen_number = None
        column_positions_filled = [
            line for line, column in other_positions if column == j
        ]
        if len(column_positions_filled) == 2:
            columns_to_verify = [column for column in quadrant[1] if column != j]
            for existing_number in possible_numbers:
                exists_on_first_column = existing_number in self.get_column_numbers(
                    sudoku, columns_to_verify[0]
                )
                exists_on_second_column = existing_number in self.get_column_numbers(
                    sudoku, columns_to_verify[1]
                )

                if exists_on_first_column and exists_on_second_column:
                    chosen_number = existing_number
                    break

        return chosen_number

    def line_and_column_exclusion_inference(
        self, sudoku, i:  int, j:int, quadrant:tuple, possible_numbers:set
    ):
        """Sudoku technique for line AND column exclusion em number

        Args:
            sudoku (list[list]): Sudoku
            i (int): Line
            j (int): Column
            quadrant (tuple): Quadrant description
            other_positions (list): Other positions from quadrant
            possible_numbers (set): All possible numbers from empty position

        Returns:
            Optional int: Chosen number if possible, else None
        """
        lines_to_verify = [line for line in quadrant[0] if line != i]

        columns_to_verify = [
            column for column in quadrant[1] if column != j if not sudoku[i][column]
        ]
        chosen_number = None
        for existing_number in possible_numbers:
            exist_on_first_line = existing_number in sudoku[lines_to_verify[0]]
            exist_on_second_line = existing_number in sudoku[lines_to_verify[1]]

            exists_on_empty_column = all(
                [
                    existing_number in self.get_column_numbers(sudoku, column)
                    for column in columns_to_verify
                ]
            )

            if exist_on_first_line and exist_on_second_line and exists_on_empty_column:
                chosen_number = existing_number
                break
        return chosen_number

    def apply_sudoku_strategies(
        self, sudoku: list[list], empty_positions: dict
    ) -> list[list]:
        """Solve sudoku
        - Create new sudoku
        - Find empty positions
        - Iterates to find best positions to replace (with just 1 number remaining)
        Args:
            sudoku (list[list]): Original sudoku

        Raises:
            MalformedSudoku: When sudoku is unsolvable

        Returns:
            list[list]: Solved sudoku when there's no empty value in sudoku anymore
        """

        print(f"Posições vazias: {len(empty_positions)}")
        try:
            while True:
                for index, ((i, j), _) in enumerate(empty_positions.items()):
                    possible_numbers = set(
                        self.NUMBERS - self.find_existing_numbers(sudoku, i, j)
                    )
                    empty_positions[(i, j)] = possible_numbers

                    if len(possible_numbers) == 1:
                        sudoku[i][j] = possible_numbers.pop()
                        empty_positions.pop((i, j))
                        break
                    quadrant = self.find_quadrant(i, j)

                    # Pega todas as posições fora a que eu desejo
                    other_positions = [
                        (aux_i, aux_j)
                        for aux_i in quadrant[0]
                        for aux_j in quadrant[1]
                        if (aux_i, aux_j) != (i, j) and sudoku[aux_i][aux_j] != 0
                    ]

                    if chosen_number := self.line_exclusion_inference(
                        sudoku=sudoku,
                        quadrant=quadrant,
                        i=i,
                        other_positions=other_positions,
                        possible_numbers=possible_numbers,
                    ):
                        sudoku[i][j] = chosen_number
                        empty_positions.pop((i, j))
                        break

                    elif chosen_number := self.column_exclusion_inference(
                        sudoku=sudoku,
                        quadrant=quadrant,
                        j=j,
                        other_positions=other_positions,
                        possible_numbers=possible_numbers,
                    ):
                        sudoku[i][j] = chosen_number
                        empty_positions.pop((i, j))
                        break

                    elif chosen_number := self.line_and_column_exclusion_inference(
                        sudoku=sudoku,
                        i=i,
                        j=j,
                        quadrant=quadrant,
                        possible_numbers=possible_numbers,
                    ):
                        sudoku[i][j] = chosen_number
                        empty_positions.pop((i, j))
                        break
                else:
                    raise MalformedSudoku
                if not empty_positions:
                    break

            return True, empty_positions
        except MalformedSudoku:
            print("Não é um sudoku fácil!")
            return False, empty_positions

    @staticmethod
    def get_empty_value(sudoku):
        """Gets first empty value found

        Args:
            sudoku (list[list]): sudoku

        Returns:
            Optional[int]: Empty value if exists
        """
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] == 0:
                    return i, j
        return None

    def is_number_valid(self, sudoku, number, empty_value):
        """Checks if number can be placed on that position

        Args:
            sudoku (_type_): Sudoku
            number (_type_): Number
            empty_value (_type_): Empty value position

        Returns:
            _type_: _description_
        """

        i, j = empty_value

        for aux_j in range(9):
            if sudoku[i][aux_j] == number:
                return False
        for aux_i in range(9):
            if sudoku[aux_i][j] == number:
                return False
        quadrant = self.find_quadrant(i, j)

        for i in quadrant[0]:
            for j in quadrant[1]:
                if sudoku[i][j] == number:
                    return False

        return True

    def apply_backtracking_strategy(self, sudoku, empty_positions: dict):
        """Applies backtracking strategy with recursion

        Args:
            sudoku (_type_): sudoku
            empty_positions (dict): Empty positions info

        Returns:
            _type_: _description_
        """

        empty_value = self.get_empty_value(sudoku)
        if not empty_value:
            return True
        i, j = empty_value

        for number in empty_positions[(i, j)]:
            if self.is_number_valid(sudoku, number, empty_value):
                sudoku[i][j] = number
                if self.apply_backtracking_strategy(sudoku, empty_positions):
                    return True
                sudoku[i][j] = 0
        return False

    def solve(self):
        """Executes strategies"""

        start = time.perf_counter()

        modified_sudoku = copy.deepcopy(self.original_sudoku)

        is_solved, empty_positions = self.apply_sudoku_strategies(
            sudoku=modified_sudoku,
            empty_positions=self.get_empty_positions(self.original_sudoku),
        )

        self.print_sudoku(
            first_sudoku=self.original_sudoku,
            current_sudoku=modified_sudoku,
        )

        if not is_solved:
            modified_sudoku_v2 = copy.deepcopy(modified_sudoku)
            is_solved = self.apply_backtracking_strategy(
                modified_sudoku_v2, empty_positions
            )

            self.print_sudoku(
                first_sudoku=modified_sudoku,
                current_sudoku=modified_sudoku_v2,
            )
        self.execution_time = round((time.perf_counter() - start) * 1000, 2)
        print(f"Tempo total de execução: {self.execution_time} ms")

