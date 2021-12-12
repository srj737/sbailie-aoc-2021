def ingest_list_of_connections(filename):
    with open(filename) as file:
        lines = file.readlines()
    output_dictionary = {}
    for line in lines:
        a, b = line.strip().split('-')
        # Save a to b path in dictionary
        if a in output_dictionary:
            if b not in output_dictionary[a]:
                output_dictionary[a].append(b)
        else:
            output_dictionary[a] = [b]
        # Save b to a path in dictionary
        if b in output_dictionary:
            if a not in output_dictionary[b]:
                output_dictionary[b].append(a)
        else:
            output_dictionary[b] = [a]
    return output_dictionary


def is_valid_next_step(next_cave, path, part_2):
    new_path = path.copy()
    new_path.append(next_cave)
    small_cave_tally = {}
    small_caves_visited_twice = []
    for cave in new_path:
        if cave.islower():
            if cave in small_cave_tally:
                small_cave_tally[cave] += 1
            else:
                small_cave_tally[cave] = 1
    for cave in small_cave_tally:
        if cave in ['start', 'end']:
            if small_cave_tally[cave] > 1:
                return False  # Start and end can only be visited once in both Part 1 or Part 2
        if small_cave_tally[cave] > 2:
            return False  # 3 or more times is invalid regardless of Part 1 or Part 2
        elif small_cave_tally[cave] > 1:
            if not part_2:
                return False
            else:
                small_caves_visited_twice.append(cave)
                if len(small_caves_visited_twice) > 1:
                    return False
    return True


def count_distinct_paths(connections, additional_rules=False):
    distinct_path_count = 0
    paths = [['start']]  # start with just the start
    while len(paths) > 0:
        current_path = paths.pop()
        if current_path[0] == 'start' and current_path[-1] == 'end':
            distinct_path_count += 1
            continue
        latest_cave = current_path[-1]
        for next_step in connections[latest_cave]:
            if is_valid_next_step(next_step, current_path, additional_rules):
                buffer = current_path.copy()
                buffer.append(next_step)
                paths.append(buffer)
    return distinct_path_count


###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.01')
distinct_paths = count_distinct_paths(cave_connections)
print("Part 1 Mini Test 1 Input (10): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.02')
distinct_paths = count_distinct_paths(cave_connections)
print("Part 1 Mini Test 2 Input (19): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.1')
distinct_paths = count_distinct_paths(cave_connections)
print("Part 1 Test Input (226): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-1')
distinct_paths = count_distinct_paths(cave_connections)
print("Part 1 Real Input (3450): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.01')
distinct_paths = count_distinct_paths(cave_connections, True)
print("Part 2 Mini Test 1 Input (36): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.02')
distinct_paths = count_distinct_paths(cave_connections, True)
print("Part 2 Mini Test 2 Input (103): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-0.1')
distinct_paths = count_distinct_paths(cave_connections, True)
print("Part 2 Test Input (3509): " + str(distinct_paths))

###########################################

cave_connections = ingest_list_of_connections('inputs/12-1')
distinct_paths = count_distinct_paths(cave_connections, True)
print("Part 2 Real Input (96528): " + str(distinct_paths))

###########################################
