

import copy
import time

# Sudoku Solver with Backtracking and Heuristics (MRV and LCV)
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

# Read Sudoku board from a file
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

# Check if placing a number in a specific cell is valid according to Sudoku rules
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



#  Get neighboring variables (cells in the same row, column, and box) for a given variable
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



# Initialize the domain for each cell in the Sudoku board
def initialize_domain(board):
    """Initialize the domain for each cell in the Sudoku board."""
    domain = {}
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
 
 # Select an unassigned variable using the Minimum Remaining Values (MRV) heuristic
def select_unassigned_variable(domain):
    """Select an unassigned variable using the Minimum Remaining Values (MRV) heuristic."""
    min_remaining_values = float('inf')
    selected_variable = None
    for variable, values in domain.items():
        if len(values) > 0 and len(values) < min_remaining_values:
            min_remaining_values = len(values)
            selected_variable = variable
    return selected_variable

#   Order the domain values for a variable using the Least Constraining Value (LCV) heuristic
def order_domain_values(variable, domain):
    """Order the domain values for a variable using the Least Constraining Value (LCV) heuristic."""
    value_counts = {}
    for value in domain[variable]:
        count = 0
        for neighbor in get_neighbors(variable):
            if value in domain[neighbor]:
                count += 1
        value_counts[value] = count
    return sorted(domain[variable], key=lambda x: value_counts[x])


# Backtracking search with heuristics (MRV and LCV)
def smart_backtracking(board, domain, counter):
    """Solve the Sudoku board using backtracking with heuristics."""
    varible = select_unassigned_variable(domain)
    if not varible:
        return True  # Puzzle solved
    counter[0] += 1  # Increment step counter
    row, col = varible

    # Try each value in the ordered domain for the selected variable
    for value in order_domain_values(varible, domain):
        if is_valid(board, row, col, value):
            board[row][col] = value  # Place the number
            new_domain = copy.deepcopy(domain)
            new_domain[varible] = set()  # Clear the domain for the assigned variable

            # Update the domains of neighboring variables
            for neighbor in get_neighbors(varible):
                if value in new_domain[neighbor]:
                    new_domain[neighbor].remove(value)  # Remove the assigned value from neighbors' domains

            # Check if any neighboring variable has an empty domain after the assignment
            if all(len(new_domain[v]) > 0 for v in new_domain if board[v[0]][v[1]] == 0):
                if smart_backtracking(board, new_domain, counter):
                    return True  # Continue with this placement
               
            board[row][col] = 0  # Reset (backtrack)
    return False  # Trigger backtracking




if __name__ == "__main__":
   files = ["sudoku_input_easy.txt", "sudoku_input_medium.txt", "sudoku_input_hard.txt"]

   print(f"{'Board':<25} {'Time Taken (seconds)':<15} {'Smart Time':<12} {'Smart Steps'}")
   print("-" * 55  )

# Run the Sudoku solver for each input file and measure the time taken and steps
   for file in files:
        board = read_board(file)

        counter = [0]       

        smart_board = copy.deepcopy(board)
        domain = initialize_domain(smart_board)

        start_time = time.time()
        domain = initialize_domain(board)
        smart_backtracking(board, domain, counter)
        end_time = time.time()
        print(f"{file:<25} {end_time - start_time:<15.4f} {counter[0]} steps")