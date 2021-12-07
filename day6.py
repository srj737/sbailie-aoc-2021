def ingestListOfIntOnOneLine(filename):
    result = []
    with open(filename) as file:
        lines = file.readlines()
    numbers = [int(i) for i in lines[0].split(',')]
    return numbers


def simulateFish(school, days):
    for day in range(days):
        fish_to_add = 0
        for index, fish in enumerate(school):
            if fish == 0:
                fish = 6
                school[index] = 6
                fish_to_add += 1
            else:
                fish += -1
                school[index] += -1
        for new_fish in range(fish_to_add):
            school.append(8)
        if day % 25 == 0:
            print("Loading: " + str(day) + '/' + str(days) + ' days... (Size: ' + str(len(school)) + ')')
    return len(school)


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
print("Part 2 Real Input (256 Days: X): " + str(fish_count))

###########################################