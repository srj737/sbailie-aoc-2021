#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg
#
seven_segment_dictionary = {
    '0': 'abcefg',  # 6 digits
    '1': 'cf',  # 2 digits
    '2': 'acdeg',  # 5 digits
    '3': 'acdfg',  # 5 digits
    '4': 'bcdf',  # 4 digits
    '5': 'abdfg',  # 5 digits
    '6': 'abdefg',  # 6 digits
    '7': 'acf',  # 3 digits
    '8': 'abcdefg',  # 7 digits
    '9': 'abcdfg'  # 6 digits
}


def ingest_list_of_lines(filename):
    with open(filename) as file:
        lines = file.readlines()
    return lines


def process_seven_segment_notes(notes):
    processed = []
    for line in notes:
        signals = line.split('|')[0].strip().split(' ')
        alphabetised_signals = ["".join(sorted(i)) for i in signals]
        output = line.split('|')[1].strip().split(' ')
        alphabetised_output = ["".join(sorted(i)) for i in output]
        buffer = {'signals': alphabetised_signals, 'output': alphabetised_output}
        processed.append(buffer)
    return processed


# Part 1
def count_1s_4s_7s_8s_in_outputs(notes):
    # Function to count number of 1's, 4's, 7' & 8's in the output. These are the numbers with unique numbers of
    # segments. The 'tally' list will represent the count of: [<1's>, <4's>, <7's>, <8's>]
    tally = [0] * 4
    for note in notes:
        for value in note['output']:
            if len(value) == 2:
                # 2 Segments Lit Up = '1'
                tally[0] += 1
            elif len(value) == 4:
                # 4 Segments Lit Up = '4'
                tally[1] += 1
            elif len(value) == 3:
                # 3 Segments Lit Up = '7'
                tally[2] += 1
            elif len(value) == 7:
                # 7 Segments Lip Up = '8'
                tally[3] += 1
    return sum(tally)


def count_overlapping_characters(a, b):
    count = 0
    for char in a:
        if char in b:
            count += 1
    return count


# Part 2
def solve_and_sum_outputs(notes):
    total = 0

    for note in notes:
        note['solved'] = [0] * 10

        # Solve for 1's and 4's
        for value in note['signals']:
            if len(value) == 2:
                # 2 Segments Lit Up = '1'
                note['solved'][1] = value
            elif len(value) == 4:
                # 4 Segments Lit Up = '4'
                note['solved'][4] = value
            elif len(value) == 3:
                # 3 Segments Lit Up = '7'
                note['solved'][7] = value
            elif len(value) == 7:
                # 7 Segments Lip Up = '8'
                note['solved'][8] = value

        def solve_based_on_overlap(test_value):
            overlap_with_1 = count_overlapping_characters(test_value, note['solved'][1])
            overlap_with_4 = count_overlapping_characters(test_value, note['solved'][4])
            if len(test_value) in [2, 4, 3, 7]:
                # Already solved
                return 'pre-solved'
            elif len(test_value) == 6:
                if overlap_with_1 == 1:
                    return 6
                elif overlap_with_1 == 2:
                    if overlap_with_4 == 3:
                        return 0
                    elif overlap_with_4 == 4:
                        return 9
            elif len(test_value) == 5:
                if overlap_with_4 == 4:
                    return 9
                elif overlap_with_4 == 2:
                    return 2
                elif overlap_with_4 == 3:
                    if overlap_with_1 == 2:
                        return 3
                    elif overlap_with_1 == 1:
                        return 5

        # Solve all digits
        for value in note['signals']:
            if len(value) != (2 or 4):
                # If not 2 or 4 Segments Lit Up (As '1' and '4' already solved)
                # Otherwise can be solved:
                solved_index = solve_based_on_overlap(value)
                if solved_index != 'pre-solved':
                    note['solved'][solved_index] = value

        # Decode output
        output_string = ''
        for value in note['output']:
            output_string += str(note['solved'].index(value))
        total += int(output_string)

    return total


###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-0.1'))
unique_digits = count_1s_4s_7s_8s_in_outputs(seven_segment_notes)
print("Part 1 Mini Test Input (0): " + str(unique_digits))

###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-0.2'))
unique_digits = count_1s_4s_7s_8s_in_outputs(seven_segment_notes)
print("Part 1 Test Input (26): " + str(unique_digits))

###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-1'))
unique_digits = count_1s_4s_7s_8s_in_outputs(seven_segment_notes)
print("Part 1 Real Input (440): " + str(unique_digits))

###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-0.1'))
output_sum = solve_and_sum_outputs(seven_segment_notes)
print("Part 2 Mini Test Input (5353): " + str(output_sum))

###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-0.2'))
output_sum = solve_and_sum_outputs(seven_segment_notes)
print("Part 2 Test Input (61229): " + str(output_sum))

###########################################

seven_segment_notes = process_seven_segment_notes(ingest_list_of_lines('inputs/8-1'))
output_sum = solve_and_sum_outputs(seven_segment_notes)
print("Part 2 Real Input (1046281): " + str(output_sum))

###########################################
