def ingest_grid_of_ints(filename):
    with open(filename) as file:
        lines = file.readlines()
    output = []
    for line in lines:
        line = line.strip()
        buffer = []
        for char in line:
            buffer.append(int(char))
        output.append(buffer)
    return output


# Reusable function
def check_if_low_point(y, x, grid, want_lower_point_returned=False):
    height = grid[y][x]
    adjacent_increments = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    adjacent_heights = []
    for index, movement in enumerate(adjacent_increments):
        try:
            test_y = y + movement[0]
            test_x = x + movement[1]
            if test_y < 0 or test_x < 0:
                continue  # Argh! Forgot that negative index is valid!
            adjacent_heights.append(grid[test_y][test_x])
            if grid[test_y][test_x] < height:
                strictly_lower_point = (test_y, test_x)
        except IndexError:
            continue  # Out of Bounds -> At edge, so move on.
    if all(i > height for i in adjacent_heights):
        # Found lowest point
        return True
    elif want_lower_point_returned:
        return strictly_lower_point
    else:
        return False


# Part 1
def find_risk_level_of_low_points(grid):
    total_risk = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            height = grid[y][x]
            if check_if_low_point(y, x, grid):
                total_risk += (1 + height)
    return total_risk


# Part 2
def find_product_of_largest_basins(grid):
    # Create grid to keep track of low points and how many drain into them
    low_point_grid = []
    for y in range(len(grid)):
        buffer = [0] * len(grid[0])
        low_point_grid.append(buffer)

    # Iterate and drain each point
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            height = grid[y][x]
            if height != 9:
                at_low_point = check_if_low_point(y, x, grid)
                curr_x, curr_y = x, y
                while at_low_point is not True:
                    at_low_point = check_if_low_point(curr_y, curr_x, grid, True)
                    if at_low_point is True:
                        break
                    curr_y, curr_x = at_low_point
                # Found related basin point (Known to find one and only one)
                low_point_grid[curr_y][curr_x] += 1

    # Multiply three largest basins together
    extracted_low_points = []
    for y in range(len(low_point_grid)):
        for x in range(len(low_point_grid[0])):
            value = low_point_grid[y][x]
            if value > 0:
                extracted_low_points.append(value)
    extracted_low_points = sorted(extracted_low_points, reverse=True)
    return extracted_low_points[0] * extracted_low_points[1] * extracted_low_points[2]


###########################################

cave_floor = ingest_grid_of_ints('inputs/9-0.1')
risk_level = find_risk_level_of_low_points(cave_floor)
print("Part 1 Test Input (15): " + str(risk_level))

###########################################

cave_floor = ingest_grid_of_ints('inputs/9-1')
risk_level = find_risk_level_of_low_points(cave_floor)
print("Part 1 Real Input (562): " + str(risk_level))

###########################################

cave_floor = ingest_grid_of_ints('inputs/9-0.1')
largest_three_basins_product = find_product_of_largest_basins(cave_floor)
print("Part 2 Test Input (1134): " + str(largest_three_basins_product))

###########################################

cave_floor = ingest_grid_of_ints('inputs/9-1')
largest_three_basins_product = find_product_of_largest_basins(cave_floor)
print("Part 2 Main Input (1076922): " + str(largest_three_basins_product))

###########################################
