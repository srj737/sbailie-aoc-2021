def ingestListOfWordAndInt(filename):
    with open(filename) as file:
        lines = file.readlines()
        lines = [[line.strip().split()[0], int(line.strip().split()[1])] for line in lines]
        #print(lines)
    return lines


def processCommands(commands):
    x, y = 0, 0
    for command in commands:
        direction = command[0]
        value = command[1]
        if direction == 'forward':
            x += value
        elif direction == 'down':
            y += value
        elif direction == 'up':
            y += -value
    return x * y


def processCommandsWithAim(commands):
    x, y, aim = 0, 0, 0
    for command in commands:
        direction = command[0]
        value = command[1]
        if direction == 'forward':
            x += value
            y += aim * value
        elif direction == 'down':
            aim += value
        elif direction == 'up':
            aim += -value
    return x * y


###########################################

commands = ingestListOfWordAndInt('inputs/2-0.1')
value = processCommands(commands)
print("Part 1 Test Input (150): " + str(value))


###########################################

commands = ingestListOfWordAndInt('inputs/2-1')
value = processCommands(commands)
print("Part 1 Real Input (1962940): " + str(value))


###########################################

commands = ingestListOfWordAndInt('inputs/2-0.1')
value = processCommandsWithAim(commands)
print("Part 2 Test Input (900): " + str(value))


###########################################

commands = ingestListOfWordAndInt('inputs/2-1')
value = processCommandsWithAim(commands)
print("Part 2 Real Input (1813664422): " + str(value))


###########################################