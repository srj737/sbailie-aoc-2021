import functools


def ingest_reboot_steps(filename):
    with open(filename) as file:
        lines = file.readlines()
    output = []
    for line in lines:
        state = 0
        if line.split(" ")[0] == "on":
            state = 1
        coords = line.strip().split(" ")[1]
        split_coords = coords.split(",")
        min_x, max_x = [int(i) for i in split_coords[0].strip("x=").split("..")]
        min_y, max_y = [int(i) for i in split_coords[1].strip("y=").split("..")]
        min_z, max_z = [int(i) for i in split_coords[2].strip("z=").split("..")]
        output.append([state, min_x, max_x, min_y, max_y, min_z, max_z])
    return output


def count_on_cubes(steps, initial_range_flag=False):
    on_cubes = set()
    for step_index, step in enumerate(steps):
        print("Starting reboot step #" + str(step_index) + " of " + str(len(steps)) + " steps.")
        # To speed up, first check if it is totally out of range, and then don't even iterate through each coord
        if initial_range_flag and out_of_initial_range_check(step):
            continue
        # Iterate through each coord
        for x in range(step[1], step[2] + 1):
            for y in range(step[3], step[4] + 1):
                for z in range(step[5], step[6] + 1):
                    coord = (x, y, z)
                    if initial_range_flag and out_of_initial_range_check(coord):
                        continue
                    if step[0] == 1:
                        on_cubes.add(coord)
                    elif step[0] == 0 and coord in on_cubes:
                        on_cubes.remove(coord)
    return len(on_cubes)


#@functools.lru_cache(maxsize=None)
def out_of_initial_range_check(input):
    range_min_x = range_min_y = range_min_z = -50
    range_max_x = range_max_y = range_max_z = 50
    # (1) If a list has been passed in, that means it is a full step consisting of ranges
    if isinstance(input, list):
        if input[1] < range_min_x and input[2] < range_min_x:
            return True  # All x are below min x
        elif input[1] > range_max_x and input[2] > range_max_x:
            return True  # All x are above max x
        if input[3] < range_min_y and input[4] < range_min_y:
            return True  # All y are below min y
        elif input[3] > range_max_y and input[4] > range_max_y:
            return True  # All y are above max y
        if input[5] < range_min_z and input[6] < range_min_z:
            return True  # All z are below min z
        elif input[5] > range_max_z and input[6] > range_max_z:
            return True  # All z are above max z
    # (2) Otherwise if a set has been passed in, that means it is a single coordinate to check
    elif isinstance(input, set):
        if input[0] < range_min_x or input[0] > range_max_x:
            return True  # The x coord is below the min x or above the max x
        elif input[1] < range_min_y or input[1] > range_max_y:
            return True  # The y coord is below the min y or above the max y
        elif input[2] < range_min_z or input[2] > range_max_z:
            return True  # The z coord is below the min z or above the max z
    return False  # Otherwise, the default after the checks is that it is in the range and valid


###########################################

reboot_steps = ingest_reboot_steps('inputs/22-0.1')
on_cube_count = count_on_cubes(reboot_steps, True)
print("Part 1 Mini Test Input (39): " + str(on_cube_count))

###########################################

reboot_steps = ingest_reboot_steps('inputs/22-0.2')
on_cube_count = count_on_cubes(reboot_steps, True)
print("Part 1 Test Input (590784): " + str(on_cube_count))

###########################################

reboot_steps = ingest_reboot_steps('inputs/22-1')
on_cube_count = count_on_cubes(reboot_steps, True)
print("Part 1 Real Input (611176): " + str(on_cube_count))

###########################################

reboot_steps = ingest_reboot_steps('inputs/22-1.1')
on_cube_count = count_on_cubes(reboot_steps, True)
print("Part 2 Test Input (Only initialization procedure region: 474140): " + str(on_cube_count))

###########################################

reboot_steps = ingest_reboot_steps('inputs/22-1.1')
on_cube_count = count_on_cubes(reboot_steps)
print("Part 2 Test Input (2758514936282235): " + str(on_cube_count))

###########################################

reboot_steps = ingest_reboot_steps('inputs/22-1')
on_cube_count = count_on_cubes(reboot_steps)
print("Part 2 Real Input (??): " + str(on_cube_count))

###########################################
