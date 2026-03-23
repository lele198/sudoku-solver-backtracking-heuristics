
def print_board(board):
    """Print 9x9 Sudoku board."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Print horizontal separator every 3 rows
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # Print vertical separator every 3 columns
            print(board[i][j], end=" ")
        print()  # Newline after each row

def find_empty(board):
    """Find an empty cell in the Sudoku board. Returns (row, col) or None if no empty cell."""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # Return the position of the empty cell
    return None  # No empty cells found

def is_valid(board, num, pos):
    """Check if placing num at pos is valid according to Sudoku rules."""
    row, col = pos

    # Check the row
    for j in range(9):
        if board[row][j] == num and j != col:
            return False

    # Check the column
    for i in range(9):
        if board[i][col] == num and i != row:
            return False

    # Check the 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True  # The move is valid

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking. Returns True if solved, False otherwise."""
    empty_cell = find_empty(board)
    if not empty_cell:
        return True  # No empty cells, puzzle solved

    row, col = empty_cell
    for num in range(1, 10):  # Try numbers 1-9
        if is_valid(board, num, (row, col)):
            board[row][col] = num  # Place the number

            if solve_sudoku(board):
                return True  # Continue to solve the rest of the board

            board[row][col] = 0  # Reset the cell (backtrack)

    return False  # Trigger backtracking

if __name__ == "__main__":
    # Example Sudoku board (0 represents empty cells)
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0 ,6],
        [9 ,6 ,1 ,5 ,3 ,4 ,2 ,8 ,7],
        [3 ,7 ,2 ,9 ,1 ,8 ,5 ,4 ,6],
        [1 ,5 ,4 ,2 ,6 ,7 ,3 ,9 ,8]
    ]

    print("Original Sudoku Board:")
    print_board(board)

    if solve_sudoku(board):
        print("\nSolved Sudoku Board:")
        print_board(board)
    else:
        print("\nNo solution exists for the given Sudoku board.")