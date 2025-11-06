# Define the canvas size
GRID_WIDTH = 30
GRID_HEIGHT = 30
EMPTY_PIXEL = ' '
# LINE_PIXEL = '*'

# Define the start and end points
from_x = 20
from_y = 20
to_x = 29
to_y = 10

# --- 1. Initialize the Grid (Matrix of Pixels) ---
# Create a list of lists representing the matrix

def draw_line_bresenham(from_x, from_y, to_x, to_y) -> list[list]:
    grid = [[EMPTY_PIXEL] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    
    # Create a line on the grid between (from_x, from_y) and (to_x, to_y) using Bresenham's algorithm.
    # This implementation handles all octants.
    
    # Ensure coordinates are within bounds for the simple example
    # In a real application, you'd add robust clipping/boundary checks.
    distance_x = abs(to_x - from_x)
    distance_y = abs(to_y - from_y)
    
    # Determine direction of step
    step_x = 1 if from_x < to_x else -1
    step_y = 1 if from_y < to_y else -1

    # Initial decision parameter (simplified for this general case)
    err = distance_x - distance_y
    
    current_x, current_y = from_x, from_y

    # Main loop iterates until the end point is reached
    # The loop condition ensures the drawing stops at (x1, y1)
    while True:
        # Draw the pixel at the current coordinates (y is row, x is column)
        # Note: In a list-of-lists matrix, the first index is the row (y-coordinate)
        # and the second index is the column (x-coordinate).
        if 0 <= current_y < len(grid) and 0 <= current_x < len(grid[0]):
            print(f"Draw x:{current_x} y:{current_y}")
            grid[current_y][current_x] = '*'

        # Exit condition: if we've reached the end point
        if current_x == to_x and current_y == to_y:
            break

        # Calculate the next step
        e2 = 2 * err
        
        if e2 > -distance_y:  # Move in x-direction
            err -= distance_y
            current_x += step_x
        
        if e2 < distance_x:  # Move in y-direction
            err += distance_x
            current_y += step_y

    return grid
            
# --- 2. Draw the Line ---
print(f"Drawing line from ({from_x}, {from_y}) to ({to_x}, {to_y})...")
grid = draw_line_bresenham(from_x, from_y, to_x, to_y)

# --- 3. Print the Resulting Matrix (The 'Canvas') ---
print("\n--- Canvas Output ---")
for row in grid:
    print("".join(row))
print("---------------------")

# Verify the endpoints are drawn
print(f"Start point ({from_x}, {from_y}) pixel: '{grid[from_y][from_x]}'")
print(f"End point ({to_x}, {to_y}) pixel: '{grid[to_y][to_x]}'")