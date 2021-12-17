def ingest_target_area(filename):
    with open(filename) as file:
        lines = file.readlines()
    x_points = tuple(
        sorted([int(i) for i in lines[0].strip().split(' ')[-2:][0].split(',')[0].split('=')[1].split('..')]))
    y_points = tuple(
        sorted([int(i) for i in lines[0].strip().split(' ')[-2:][1].split(',')[0].split('=')[1].split('..')]))
    return y_points, x_points


def find_tragectory_with_highest_peak(target, max_y_vel=50, min_y_vel=-20, max_x_vel=50, min_x_vel=0):
    optimum_peak = optimum_y_vel = optimum_x_vel = hit_count = 0
    for y_velocity in range(min_y_vel, max_y_vel):
        for x_velocity in range(min_x_vel, max_x_vel):
            target_hit, trajectory_peak = launch_probe((0, 0), target, (y_velocity, x_velocity))
            if target_hit:
                optimum_peak = trajectory_peak
                optimum_y_vel = y_velocity
                optimum_x_vel = x_velocity
                hit_count += 1
                # print(str(x_velocity) + ',' + str(y_velocity))
    return optimum_y_vel, optimum_x_vel, optimum_peak, hit_count


# Due to drag, the probe's x velocity changes by 1 toward the value 0; that is, it decreases by 1 if it is greater
# than 0, increases by 1 if it is less than 0, or does not change if it is already 0. Due to gravity, the probe's y
# velocity decreases by 1.
x_acc = lambda vel: -1 if (vel > 0) else (+1 if (vel < 0) else 0)
y_acc = - 1


def launch_probe(start, target, velocity):
    target_hit = False
    y_pos, x_pos = start
    y_vel, x_vel = velocity
    peak = y_pos
    time_step = 0
    while is_not_after_target((y_pos, x_pos), target):
        y_pos += y_vel
        x_pos += x_vel
        y_vel += y_acc
        x_vel += x_acc(x_vel)
        time_step += 1
        if y_pos > peak:
            peak = y_pos
        if hit_target((y_pos, x_pos), target):
            target_hit = True
    return target_hit, peak


def is_not_after_target(position, target_area):
    lowest_y = min(target_area[0])
    farthest_x = max(target_area[1])
    if position[0] < lowest_y or position[1] > farthest_x:
        return False
    return True


def hit_target(position, target_area):
    lower_y = min(target_area[0])
    higher_y = max(target_area[0])
    closer_x = min(target_area[1])
    farther_x = max(target_area[1])
    if lower_y <= position[0] <= higher_y and closer_x <= position[1] <= farther_x:
        return True
    return False


###########################################

target = ingest_target_area('inputs/17-0.1')
y_vel, x_vel, peak, valid_vel = find_tragectory_with_highest_peak(target)
print("Part 1 Test Input (Peak: 45): " + str(peak))
print("Part 2 Test Input (Valid Velocity Pairs: 112): " + str(valid_vel))

###########################################

target = ingest_target_area('inputs/17-1')
y_vel, x_vel, peak, valid_vel = find_tragectory_with_highest_peak(target, 150, -150, 300)
print("Part 1 Real Input (Peak: 5050): " + str(peak))
print("Part 2 Real Input (Valid Velocity Pairs: 2223): " + str(valid_vel))

###########################################
