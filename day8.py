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
#
# Seven Segment Figits
# 0: abcefg
# 1: cf
# 2: acdeg
# 3: acdfg
# 4: bcdf
# 5: abdfg
# 6: abdefg
# 7: acf
# 8: abcdefg
# 9: abcdfg

dictionary = {
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
        output = line.split('|')[1].strip().split(' ')
        buffer = {'signals': signals, 'output': output}
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
