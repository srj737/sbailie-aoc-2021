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


def process_polymer_naively(poly, steps):
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

        # print("Finished Step: " + str(step))
        # print(polymer)

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


def insert_key_to_count_dictionary(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value


def process_polymer_efficiently(poly, steps):
    polymer = {}
    for index in range(len(poly['template']) - 1):
        pair = poly['template'][index] + poly['template'][index + 1]
        insert_key_to_count_dictionary(polymer, pair, 1)

    for step in range(steps):
        pairs_to_increase = {}
        for pair in polymer:
            count = polymer[pair]
            if count < 1:
                continue  # If no occurrences, don't bother
            else:
                if pair in poly['rules']:
                    new_char = poly['rules'][pair]
                    polymer[pair] -= count  # Decrease pair count of one that will be split
                    insert_key_to_count_dictionary(pairs_to_increase, pair[0] + new_char,
                                                   count)  # Increase new pair preceding
                    insert_key_to_count_dictionary(pairs_to_increase, new_char + pair[1],
                                                   count)  # Increase new pair proceeding
        # The actual save need to be outside loop due to: "RuntimeError: dictionary changed size during iteration"
        for pair, value in pairs_to_increase.items():
            insert_key_to_count_dictionary(polymer, pair, value)

        # print("Finished Step: " + str(step))
        # print(polymer)

    # Calculate answer
    char_frequencies = {}
    for pair in polymer:
        count = polymer[pair]
        for char in pair:
            insert_key_to_count_dictionary(char_frequencies, char, count)
    for key, value in char_frequencies.items():
        # First and last characters are were each only counted once.
        if key in [poly['template'][0], poly['template'][-1]]:
            value += 1
        # Now all characters are double counted so divide by 2.
        char_frequencies[key] = int(value / 2)

    most_common = max(char_frequencies, key=char_frequencies.get)
    least_common = min(char_frequencies, key=char_frequencies.get)
    most_common_count = char_frequencies[most_common]
    least_common_count = char_frequencies[least_common]

    return most_common_count - least_common_count


###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-0.1')
most_common_count_minus_least_common_count = process_polymer_naively(polymerization, 10)
print("Part 1 Test Input (10 steps - 1588): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-1')
most_common_count_minus_least_common_count = process_polymer_naively(polymerization, 10)
print("Part 1 Real Input (10 steps - 3906): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-0.1')
most_common_count_minus_least_common_count = process_polymer_efficiently(polymerization, 40)
print("Part 2 Test Input (40 steps - 2188189693529): " + str(most_common_count_minus_least_common_count))

###########################################

polymerization = ingest_polymer_template_and_insertion_rules('inputs/14-1')
most_common_count_minus_least_common_count = process_polymer_efficiently(polymerization, 40)
print("Part 2 Real Input (40 steps - 4441317262452): " + str(most_common_count_minus_least_common_count))

###########################################
