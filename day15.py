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


class Node:
    def __init__(self, parent=None, y=None, x=None):
        self.parent = parent
        self.y = y
        self.x = x
        if x == 0 and y == 0:
            self.risk = 0
        else:
            self.risk = float('inf')


def find_optimal_risk_path_dijkstra(grid):
    # Implemented from: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Algorithm
    max_y_idx = len(grid) - 1
    max_x_idx = len(grid[0]) - 1

    # 1) Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.
    # 2) Assign to every node a tentative distance value: set it to zero for our initial node and to infinity for all
    # other nodes. Set the initial node as current.
    unvisited = []
    for j in range(max_y_idx + 1):
        for i in range(max_x_idx + 1):
            unvisited.append(Node(None, j, i))
    current_node = unvisited[0]
    end_node = unvisited[-1]

    # 5) If the destination node has been marked visited, then stop. The algorithm has finished.
    while end_node in unvisited:

        # 3) For the current node, consider all of its unvisited neighbors and calculate their tentative distances
        # through the current node. Compare the newly calculated tentative distance to the current assigned value and
        # assign the smaller one.
        # // Generate children
        children = []
        adjacents_movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for movement in adjacents_movements:
            child_y = current_node.y + movement[0]
            child_x = current_node.x + movement[1]
            if child_y < 0 or child_y > max_y_idx or child_x < 0 or child_x > max_x_idx:
                continue  # Ignore if off grid
            for node in unvisited:
                if node.y == child_y and node.x == child_x:
                    children.append(node)

        # // Loop through children to calculate their risk
        for child in children:
            if child not in unvisited:
                continue  # Ignore child if visited
            child.risk = min(current_node.risk + grid[child.y][child.x], child.risk)

        # 4) When we are done considering all of the unvisited neighbors of the current node, mark the current node
        # as visited and remove it from the unvisited set. A visited node will never be checked again.
        for i, o in enumerate(unvisited):
            if o == current_node:
                del unvisited[i]
                break

        # 6) Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the
        # new current node, and go back to step 3.
        lowest_risk = float('inf')
        for i, o in enumerate(unvisited):
            current_risk = unvisited[i].risk
            if current_risk < lowest_risk:
                lowest_risk = current_risk
                current_node = o

        # Debug
        # if len(unvisited) % 10 == 0:
        #    print(str(len(unvisited)))

    return end_node.risk


def part_2_create_full_cavern(tile):
    factor = 5
    tile_y = len(tile)
    tile_x = len(tile[0])
    full_y = tile_y * factor
    full_x = tile_x * factor
    full = []

    # Create full cavern
    for j in range(full_y):
        full.append([0] * full_x)

    # Populate cavern
    for row_idx, row in enumerate(full):
        for col_idx, value in enumerate(full):
            add_y = row_idx // tile_y
            old_y = row_idx % tile_y
            add_x = col_idx // tile_x
            old_x = col_idx % tile_x
            new_value = tile[old_y][old_x] + add_y + add_x
            if new_value > 9:
                new_value = (new_value + 1) % 10
            full[row_idx][col_idx] = new_value

    return full


###########################################

cavern = ingest_grid_of_ints('inputs/15-0.1')
lowest_risk_of_optimal_path = find_optimal_risk_path_dijkstra(cavern)
print("Part 1 Test Input (40): " + str(lowest_risk_of_optimal_path))

###########################################

cavern = ingest_grid_of_ints('inputs/15-1')
lowest_risk_of_optimal_path = find_optimal_risk_path_dijkstra(cavern)
print("Part 1 Real Input (363): " + str(lowest_risk_of_optimal_path))

###########################################

cavern_tile = ingest_grid_of_ints('inputs/15-0.1')
cavern = part_2_create_full_cavern(cavern_tile)
lowest_risk_of_optimal_path = find_optimal_risk_path_dijkstra(cavern)
print("Part 2 Test Input (315): " + str(lowest_risk_of_optimal_path))

###########################################

cavern_tile = ingest_grid_of_ints('inputs/15-1')
cavern = part_2_create_full_cavern(cavern_tile)
lowest_risk_of_optimal_path = find_optimal_risk_path_dijkstra(cavern)
print("Part 2 Real Input (2835): " + str(lowest_risk_of_optimal_path))

###########################################
