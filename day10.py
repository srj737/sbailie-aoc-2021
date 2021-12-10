def ingest_list_of_strings(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]
    return lines


open_ref = ['(', '[', '{', '<']
closed_ref = [')', ']', '}', '>']
closed_to_open_map = {')': '(', ']': '[', '}': '{', '>': '<'}
error_point_map = {')': 3, ']': 57, '}': 1197, '>': 25137}


def analyse_subsystem_chunks(chunks):
    valid_count, corrupt_count, incomplete_count, total_syntax_error_score = 0, 0, 0, 0
    for line in chunks:
        status = 'incomplete'  # Presume valid
        buffer = []
        for index, char in enumerate(line):
            if char in open_ref:
                buffer.append(char)
            elif char in closed_ref:
                if buffer[-1] == closed_to_open_map[char]:
                    buffer.pop()
                else:
                    status = 'corrupt'
                    total_syntax_error_score += error_point_map[char]
                    break
            if index == len(line) - 1 and len(buffer) == 0:
                status = 'valid'

        if status == 'valid':
            valid_count += 1
        elif status == 'corrupt':
            corrupt_count += 1
        elif status == 'incomplete':
            incomplete_count += 1

    return {'total': len(chunks), 'valid': valid_count, 'corrupt': corrupt_count, 'incomplete': incomplete_count,
            'error score': total_syntax_error_score}


###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.01')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1 Mini Input (All 5 Valid Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.02')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1 Mini Input (All 4 Corrupt Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.03')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1 Mini Input (All 3 Incomplete Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.1')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1 Input (Error Score: 26397): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-1')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1 Real (Error Score: 392139): " + str(chunk_analysis))

###########################################
