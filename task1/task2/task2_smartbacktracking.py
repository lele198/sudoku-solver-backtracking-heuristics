
import copy
import time

# This code implements a Sudoku solver using backtracking with heuristics (Minimum Remaining Values and Least Constraining Value).
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

# Read the Sudoku board from a file. The file should have 9 lines of 9 digits (0 for empty cells), with optional spaces.
def read_board(filename):
    """Read Sudoku board from a file."""
    board = []
    with open(filename, 'r') as f:
        lines = f.readlines()[1:]  # Skip the first line (metadata)
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            line = line.replace(" ", "")  # Remove spaces

            if len(line) != 9 or not line.isdigit():
                raise ValueError("Each line must contain exactly 9 characters.")
            board.append([int(char) for char in line])
    if len(board) !=9:
        raise ValueError("The board must contain exactly 9 lines.")
    return board

# Check if it's valid to place a number in a given cell according to Sudoku rules.
def is_valid(board, row, col, num):
    """Check if it's valid to place num in the given row and column."""
    # Check the row
    for j in range(9):
        if board[row][j] == num:
            return False
    # Check the column
    for i in range(9):
        if board[i][col] == num:
            return False
    # Check the 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            if board[i][j] == num:
                return False
    return True


# Get the neighboring variables (cells in the same row, column, and box) for a given variable.
def get_neighbors(variable):
    """Get the neighboring variables (cells in the same row, column, and box) for a given variable."""
    row, col = variable
    neighbors = set()
    # Add neighbors from the same row
    for j in range(9):
        if j != col:
            neighbors.add((row, j))
    # Add neighbors from the same column
    for i in range(9):
        if i != row:
            neighbors.add((i, col))
    # Add neighbors from the same 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3  
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            if (i, j) != variable:
                neighbors.add((i, j))
    return neighbors


# Initialize the domain for each cell in the Sudoku board. For empty cells, the domain consists of valid numbers (1-9) that can be placed in that cell. For filled cells, the domain is empty.
def initialize_domain(board):
    """Initialize the domain for each cell in the Sudoku board."""
    domain = {}
    # For each cell, if it's empty (0), calculate the valid numbers that can be placed in that cell and add them to the domain. If it's already filled, set the domain to an empty set.
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:


                domain[(i,j)] = set()
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        domain[(i,j)].add(num)
            else:
                domain[(i,j)] = set()  # No options for already filled cells
    return domain

 # Select an unassigned variable using the Minimum Remaining Values (MRV) heuristic. This heuristic selects the variable with the fewest legal values in its domain, which can help reduce the search space and increase efficiency. 
def select_unassigned_variable(domain):
    """Select an unassigned variable using the Minimum Remaining Values (MRV) heuristic."""
    min_remaining_values = float('inf')
    selected_variable = None
    # Iterate through the domain to find the variable with the fewest legal values (smallest domain size) that is still unassigned (has a non-empty domain).
    for variable, values in domain.items():
        if len(values) > 0 and len(values) < min_remaining_values:
            min_remaining_values = len(values)
            selected_variable = variable
    return selected_variable

# Order the domain values for a variable using the Least Constraining Value (LCV) heuristic. This heuristic prefers values that leave the most options open for neighboring variables, which can help avoid dead ends in the search process.
def order_domain_values(variable, domain):
    """Order the domain values for a variable using the Least Constraining Value (LCV) heuristic."""
    value_counts = {}
    #  For each value in the variable's domain, count how many neighboring variables would be affected (i.e., how many neighbors have that value in their domain). The value that affects the fewest neighbors is considered the least constraining.
    for value in domain[variable]:
        count = 0
        for neighbor in get_neighbors(variable):
            if value in domain[neighbor]:
                count += 1
        value_counts[value] = count
    return sorted(domain[variable], key=lambda x: value_counts[x])


# The main backtracking function that uses the MRV and LCV heuristics to solve the Sudoku board. It recursively assigns values to variables and backtracks if a solution is not found.
def smart_backtracking(board, domain):
    """Solve the Sudoku board using backtracking with heuristics."""
    varible = select_unassigned_variable(domain)
    if not varible:
        return True  # Puzzle solved
    
    row, col = varible
    # For each value in the ordered domain of the selected variable, check if it's valid to place that value in the corresponding cell. If it is valid, place the value and update the domain for neighboring variables. Then, recursively call the backtracking function with the updated board and domain. If a solution is found, return True. If not, reset the cell (backtrack) and continue with the next value.
    for value in order_domain_values(varible, domain):
        if is_valid(board, row, col, value):
            board[row][col] = value  # Place the number
            new_domain = copy.deepcopy(domain)
            new_domain[varible] = set()  # Clear the domain for the assigned variable

            # Update the domain for neighboring variables by removing the assigned value from their domains. This is a form of forward checking that helps to reduce the search space and can lead to faster solutions.
            for neighbor in get_neighbors(varible):
                    new_domain[neighbor].discard(value)  # Remove the assigned value from neighbors' domains

            if all(len(new_domain[v]) > 0 for v in new_domain if board[v[0]][v[1]] == 0):
                if smart_backtracking(board, new_domain):
                    return True  # Continue with this placement
                
            board[row][col] = 0  # Reset (backtrack)
    return False  # Trigger backtracking


if __name__ == "__main__":
    # Read the Sudoku board from a file
    board = read_board("sudoku_input.txt")

    print("Original Sudoku Board:")
    print_board(board)

    start_time = time.time()
    domains = initialize_domain(board)
    if smart_backtracking(board, domains):
        end_time = time.time()
        print("\nSolved Sudoku Board:")
        print_board(board)
        print(f"Solved in {end_time - start_time:.4f} seconds.")
    else:
        print("No solution exists for the given Sudoku board.")

