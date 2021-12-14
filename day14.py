def ingest_polymer_template_and_insertion_rules(filename):
    with open(filename) as file:
        lines = file.readlines()
    template = lines[0].strip()
    rules = {}
    for line in lines:
        if ' -> ' in line:
            rules[line.strip().split(' -> ')[0]] = line.strip().split(' -> ')[1]
    return {'template': template, 'rules': rules}


def insert_char(string, char, index):
    return string[:index] + char + string[index:]


def process_polymer(poly, steps):
    polymer = poly['template']

    for step in range(steps):

        # Calculate what's to be inserted
        insert_buffer = []
        for index, char in enumerate(polymer):
            try:
                current_pair = polymer[index] + polymer[index + 1]
                if current_pair in poly['rules']:
                    insert_buffer.append((index + 1, poly['rules'][current_pair]))
            except IndexError:
                continue

        # Insert characters into string
        for i in reversed(insert_buffer):
            polymer = insert_char(polymer, i[1], i[0])

        print("Finished Step: " + str(step))
        #print(polymer)

    # Calculate answer
    char_frequencies = {}
    for char in polymer:
        if char in char_frequencies:
            char_frequencies[char] += 1
        else:
            char_frequencies[char] = 1
    most_common = max(char_frequencies, key=char_frequencies.get)
    least_common = min(char_frequencies, key=char_frequencies.get)
    most_common_count = char_frequencies[most_common]
    least_common_count = char_frequencies[least_common]

    return most_common_count - least_common_count


###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-0.1')
most_common_count_minus_least_common_count = process_polymer(polymerization, 10)
print("Part 1 Test Input (10 steps - 1588): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-1')
most_common_count_minus_least_common_count = process_polymer(polymerization, 10)
print("Part 1 Real Input (10 steps - 3906): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-0.1')
most_common_count_minus_least_common_count = process_polymer(polymerization, 40)
print("Part 2 Test Input (40 steps - 2188189693529): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-1')
most_common_count_minus_least_common_count = process_polymer(polymerization, 40)
print("Part 2 Real Input (40 steps - X): " + str(most_common_count_minus_least_common_count))

###########################################