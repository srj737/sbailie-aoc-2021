def ingestListOfLines(filename):
    result = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
    for line in lines:
        # x1,y1 -> x2,y2
        part_a, part_b = line.split(' -> ')
        x1, y1 = part_a.split(',')
        x2, y2 = part_b.split(',')
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # m=(y2-y1)/(x2-x1)
        if x2 - x1 == 0:
            m = float("nan")
        else:
            m = (y2 - y1) / (x2 - x1)
        result.append({'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'm': m})
    return result


def countOverlappingLines(lines, diagonalPresent=False):
    max_x, max_y = 0, 0
    for line in lines:
        max_x = max(max_x, line['x1'], line['x2'])
        max_y = max(max_y, line['y1'], line['y2'])
    grid = []
    for y in range(max_y + 1):
        grid.append([0] * (max_x + 1))
    for line in lines:
        curr_x, curr_y = line['x1'], line['y1']

        # Horizontal
        if line['m'] == 0:
            if line['x1'] < line['x2']:
                while curr_x <= line['x2']:
                    grid[curr_y][curr_x] += 1
                    curr_x += +1
            else:
                while curr_x >= line['x2']:
                    grid[curr_y][curr_x] += 1
                    curr_x += -1

        # Vertical
        if line['m'] != line['m']:  # Unique way to test for NaN
            if line['y1'] < line['y2']:
                while curr_y <= line['y2']:
                    grid[curr_y][curr_x] += 1
                    curr_y += +1
            else:
                while curr_y >= line['y2']:
                    grid[curr_y][curr_x] += 1
                    curr_y += -1

        if diagonalPresent:
            # Diagonal Up Right
            if line['m'] == 1:  # Unique way to test for NaN
                if line['y1'] < line['y2']:
                    while curr_y <= line['y2']:
                        grid[curr_y][curr_x] += 1
                        curr_x += +1
                        curr_y += +1
                else:
                    while curr_y >= line['y2']:
                        grid[curr_y][curr_x] += 1
                        curr_x += -1
                        curr_y += -1
            # Diagonal Down Right
            if line['m'] == -1:
                if line['x1'] < line['x2']:
                    while curr_x <= line['x2']:
                        grid[curr_y][curr_x] += 1
                        curr_x += +1
                        curr_y += -1
                else:
                    while curr_x >= line['x2']:
                        grid[curr_y][curr_x] += 1
                        curr_x += -1
                        curr_y += +1

    count = 0
    for row in grid:
        for value in row:
            if value > 1:
                count += 1

    return count


###########################################

ventLines = ingestListOfLines('inputs/5-0.1')
count = countOverlappingLines(ventLines)
print("Part 1 Test Input (5): " + str(count))

###########################################

ventLines = ingestListOfLines('inputs/5-1')
count = countOverlappingLines(ventLines)
print("Part 1 Real Input (6397): " + str(count))

###########################################

ventLines = ingestListOfLines('inputs/5-0.1')
count = countOverlappingLines(ventLines, True)
print("Part 2 Test Input (12): " + str(count))

###########################################

ventLines = ingestListOfLines('inputs/5-1')
count = countOverlappingLines(ventLines, True)
print("Part 2 Real Input (22335): " + str(count))

###########################################
