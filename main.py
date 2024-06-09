from sudoku_solver import SudokuSolver
from statistics import mean
sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

sudoku1 = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0],
]

sudoku2 = [
    [0, 0, 0, 5, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 8, 0],
    [6, 4, 9, 8, 3, 0, 0, 5, 7],
    [0, 6, 2, 0, 0, 0, 3, 0, 0],
    [1, 0, 0, 7, 0, 3, 4, 2, 0],
    [3, 0, 0, 9, 2, 0, 0, 6, 0],
    [0, 9, 6, 1, 0, 0, 0, 3, 0],
    [2, 0, 0, 0, 9, 6, 7, 0, 0],
    [7, 5, 3, 2, 0, 0, 1, 9, 6],
]

# Sudoku difícil!!
sudoku3 = [
    [0, 0, 0, 9, 0, 0, 0, 5, 8],
    [9, 0, 5, 0, 8, 7, 0, 0, 0],
    [0, 8, 0, 0, 0, 4, 9, 0, 7],
    [0, 0, 8, 0, 0, 0, 0, 7, 4],
    [0, 0, 2, 4, 0, 0, 8, 0, 5],
    [7, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 5, 0, 0, 9, 0, 0, 4, 3],
    [8, 0, 0, 3, 0, 0, 0, 9, 6],
    [3, 0, 0, 0, 2, 0, 0, 0, 0],
]


total_times = []

for sudoku in [sudoku, sudoku1, sudoku2, sudoku3] * 100:
    sudoku_solver = SudokuSolver(original_sudoku=sudoku)

    sudoku_solver.solve()
    total_times.append(sudoku_solver.execution_time)

print(mean(total_times))
