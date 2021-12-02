with open('inputs/1-0.1') as file:
    lines = file.readlines()
    lines = [int(line.rstrip()) for line in lines]
    #print(lines)

count = 0
prev = lines[0]
for val in lines:
    if val > prev:
        count += 1
    prev = val

print("Part 1 Test Input (7): " + str(count))

###################################

with open('inputs/1-1') as file:
    lines = file.readlines()
    lines = [int(line.rstrip()) for line in lines]
    #print(lines)

count = 0
prev = lines[0]
for val in lines:
    if val > prev:
        count += 1
    prev = val


print("Part 1 Real Input (1228): " + str(count))

###################################

with open('inputs/1-0.1') as file:
    lines = file.readlines()
    lines = [int(line.rstrip()) for line in lines]
    #print(lines)

count = 0
prev = lines[0] + lines[1] + lines[2]
for i in range(1, len(lines) - 2):
    val = lines[i] + lines[i+1] + lines[i+2]
    if val > prev:
        count += 1
    prev = val

print("Part 2 Test Input (5): " + str(count))

###################################

with open('inputs/1-1') as file:
    lines = file.readlines()
    lines = [int(line.rstrip()) for line in lines]
    #print(lines)

count = 0
prev = lines[0] + lines[1] + lines[2]
for i in range(1, len(lines) - 2):
    val = lines[i] + lines[i+1] + lines[i+2]
    if val > prev:
        count += 1
    prev = val

print("Part 2 Real Input (1257): " + str(count))