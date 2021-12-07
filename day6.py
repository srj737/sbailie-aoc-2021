def ingestListOfIntOnOneLine(filename):
    with open(filename) as file:
        line = file.readlines()[0]
    fishes = [int(i) for i in line.split(',')]
    school = [0] * 9
    for fish in fishes:
        school[fish] += 1
    return school


def simulateFish(school, days):
    # school is a list:
    # [ 0val, 1val, 2val, 3val, 4val, 5val, 6val, 7val, 8val]
    # [ 1val, 2val, 3val, 4val, 5val, 6val, 7val + 0val, 8val, 0val]
    for day in range(days):
        zero_value_fish = school.pop(0)
        school[6] += zero_value_fish
        school.append(zero_value_fish)
    return sum(school)


###########################################

fish_school = ingestListOfIntOnOneLine('inputs/6-0.1')
fish_count = simulateFish(fish_school, 18)
print("Part 1 Test Input (18 Days: 26): " + str(fish_count))

fish_school = ingestListOfIntOnOneLine('inputs/6-0.1')
fish_count = simulateFish(fish_school, 80)
print("Part 1 Test Input (80 Days: 5934): " + str(fish_count))

###########################################

fish_school = ingestListOfIntOnOneLine('inputs/6-1')
fish_count = simulateFish(fish_school, 80)
print("Part 1 Real Input (80 Days: 372984): " + str(fish_count))

###########################################

fish_school = ingestListOfIntOnOneLine('inputs/6-0.1')
fish_count = simulateFish(fish_school, 256)
print("Part 2 Test Input (256 Days: 26984457539): " + str(fish_count))

###########################################

fish_school = ingestListOfIntOnOneLine('inputs/6-1')
fish_count = simulateFish(fish_school, 256)
print("Part 2 Real Input (256 Days: 1681503251694): " + str(fish_count))

###########################################