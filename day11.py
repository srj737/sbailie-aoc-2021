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


def check_if_more_to_flash(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if isinstance(grid[y][x], int) and grid[y][x] > 9:
                return True
    return False


def check_if_all_current_flashing(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != 'FLASHED':
                return False
    return True


adjacent_increments = [
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, 0),
    (-1, 1),
    (-1, -1),
    (0, -1),
    (0, 1)
]


def flash_to_neighbours(grid, y, x):
    for index, movement in enumerate(adjacent_increments):
        test_y = y + movement[0]
        test_x = x + movement[1]
        if test_y < 0 or test_x < 0 or test_y > len(grid) - 1 or test_x > len(grid[0]) - 1:
            continue
        if isinstance(grid[test_y][test_x], int):
            grid[test_y][test_x] += 1
    return


def count_flashes_after_steps(grid, steps):
    flashes = 0
    first_simultaneous_flash_step = 0
    for step in range(steps):

        # Increase energy by 1 for all octopuses
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                grid[y][x] += 1

        # All octopuses with energy > 9 flash. (iterates until all flashes cascade)
        pending_flashes_flag = check_if_more_to_flash(grid)
        while pending_flashes_flag is True:
            for y in range(len(grid)):
                for x in range(len(grid[0])):
                    if isinstance(grid[y][x], int) and grid[y][x] > 9:
                        grid[y][x] = 'FLASHED'
                        flashes += 1
                        flash_to_neighbours(grid, y, x)
            pending_flashes_flag = check_if_more_to_flash(grid)

        # Check and record the first time all simultaneously flashed
        if first_simultaneous_flash_step == 0:
            if check_if_all_current_flashing(grid):
                first_simultaneous_flash_step = step + 1

        # All flashed reset to zero
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if grid[y][x] == 'FLASHED':
                    grid[y][x] = 0

    return flashes, first_simultaneous_flash_step


###########################################

octopuses = ingest_grid_of_ints('inputs/11-0.01')
flash_count = count_flashes_after_steps(octopuses, 2)[0]
print("Part 1 Mini Test Input (9): " + str(flash_count))

###########################################

octopuses = ingest_grid_of_ints('inputs/11-0.1')
flash_count = count_flashes_after_steps(octopuses, 100)[0]
print("Part 1 Test Input (1656): " + str(flash_count))

###########################################

octopuses = ingest_grid_of_ints('inputs/11-1')
flash_count = count_flashes_after_steps(octopuses, 100)[0]
print("Part 1 Real Input (1637): " + str(flash_count))

###########################################

octopuses = ingest_grid_of_ints('inputs/11-0.1')
first_simultaneous_flash = count_flashes_after_steps(octopuses, 200)[1]
print("Part 2 Test Input (195): " + str(first_simultaneous_flash))

###########################################

octopuses = ingest_grid_of_ints('inputs/11-1')
first_simultaneous_flash = count_flashes_after_steps(octopuses, 250)[1]
print("Part 2 Test Input (242): " + str(first_simultaneous_flash))

###########################################