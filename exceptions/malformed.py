from typing import Optional


class MalformedSudoku(Exception):
    message = "Sudoku mal formado, não é possível resolver!"

    def __init__(self, message: Optional[str] = None):
        super().__init__(self.message)
