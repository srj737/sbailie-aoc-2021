def ingest_one_line_of_ints(filename):
    with open(filename) as file:
        line = file.readlines()[0]
    numbers = [int(i) for i in line.split(',')]
    return numbers


def find_fuel_of_best_position(crabs, fuel_consumption='linear'):
    lowest_fuel = max(crabs) * max(crabs) * len(crabs)

    def find_fuel(i):
        total = 0
        for crab in crabs:

            if fuel_consumption == 'linear':
                # Part 1 - Linear Fuel Consumption (1=1, 2=2, 3=3, ...)
                increment = (abs(crab - i))
            else:
                # Part 2 - Triangular Fuel Consumption (1=1, 2=3, 3=6, ...)
                increment = int((abs(crab - i) * abs(crab - i) + abs(crab - i)) / 2)
            total += increment
            if total > lowest_fuel:
                return total
        return total

    for position in range(max(crabs) + 1):
        test = find_fuel(position)
        if test < lowest_fuel:
            lowest_fuel = test
    return lowest_fuel


###########################################

crabs_submarines = ingest_one_line_of_ints('inputs/7-0.1')
fuel = find_fuel_of_best_position(crabs_submarines)
print("Part 1 Test Input (26): " + str(fuel))

###########################################

crabs_submarines = ingest_one_line_of_ints('inputs/7-1')
fuel = find_fuel_of_best_position(crabs_submarines)
print("Part 1 Real Input (356179): " + str(fuel))

###########################################

crabs_submarines = ingest_one_line_of_ints('inputs/7-0.1')
fuel = find_fuel_of_best_position(crabs_submarines, 'triangular')
print("Part 2 Test Input (168): " + str(fuel))

###########################################

crabs_submarines = ingest_one_line_of_ints('inputs/7-1')
fuel = find_fuel_of_best_position(crabs_submarines, 'triangular')
print("Part 2 Real Input (99788435): " + str(fuel))

###########################################
