def ingest_coordinates_and_folding_instructions(filename):
    with open(filename) as file:
        lines = file.readlines()
    dots, folds = [], []
    for line in lines:
        if ',' in line:
            dots.append(tuple(int(i) for i in line.strip().split(',')))
        elif 'fold' in line:
            equation = line.strip().split(' ')[2]
            folds.append((equation.split('=')[0], int(equation.split('=')[1])))
    return {'dots': dots, 'folds': folds}


def print_paper_grid(grid):
    for row in grid:
        print("".join(str(x) for x in row))
    return


def x_fold(grid, value):
    for row in grid:
        for col_index, char in enumerate(row):
            if col_index > value and char == '█':
                mirrored_col_index = (2 * value) - col_index
                row[mirrored_col_index] = char
        del row[value:]
    return


def y_fold(grid, value):
    for row_index, row in enumerate(grid):
        if row_index > value:
            mirrored_row_index = (2 * value) - row_index
            for col_index, char in enumerate(row):
                if char == '█':
                    grid[mirrored_row_index][col_index] = char
    del grid[value:]
    return


def execute_fold(grid, fold):
    if fold[0] == 'x':
        x_fold(grid, fold[1])
    elif fold[0] == 'y':
        y_fold(grid, fold[1])
    return


def count_dots(grid):
    count = 0
    for row in grid:
        for char in row:
            if char == '█':
                count += 1
    return count


def fold_paper(paper):
    # Calculate needed size of grid
    max_x, max_y = 0, 0
    for dot in paper['dots']:
        if dot[0] > max_x:
            max_x = dot[0]
        if dot[1] > max_y:
            max_y = dot[1]

    # Create grid in memory
    grid = []
    for y in range(max_y + 1):
        grid.append([' '] * (max_x + 1))

    # Add current dots to grid
    for dot in paper['dots']:
        grid[dot[1]][dot[0]] = '█'

    # Execute folds
    for index, fold in enumerate(paper['folds']):
        execute_fold(grid, fold)
        if index == 0:  # Part 1: Print number of dots after fold
            print("Number of dots after first fold: " + str(count_dots(grid)))

    # Final printed grid
    print_paper_grid(grid)

    return


###########################################

transparent_paper = ingest_coordinates_and_folding_instructions('inputs/13-0.1')
print("Part 1&2 Test Input (17 first dots):")
fold_paper(transparent_paper)

###########################################

transparent_paper = ingest_coordinates_and_folding_instructions('inputs/13-1')
print("Part 1&2 Real Input (X first dots):")
fold_paper(transparent_paper)

###########################################
