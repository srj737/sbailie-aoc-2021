def ingest_list_of_strings(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file.readlines()]
    return lines


open_ref = ['(', '[', '{', '<']
closed_ref = [')', ']', '}', '>']
closed_to_open_map = {')': '(', ']': '[', '}': '{', '>': '<'}
error_point_map = {')': 3, ']': 57, '}': 1197, '>': 25137}
autocomplete_point_map = {'(': 1, '[': 2, '{': 3, '<': 4}


def analyse_subsystem_chunks(chunks):
    valid_count, corrupt_count, incomplete_count, total_error_score, autocomplete_score = 0, 0, 0, 0, float('nan')
    autocomplete_scores = []
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
                    total_error_score += error_point_map[char]
                    break
            if index == len(line) - 1 and len(buffer) == 0:
                status = 'valid'

        if status == 'valid':
            valid_count += 1
        elif status == 'corrupt':
            corrupt_count += 1
        elif status == 'incomplete':
            incomplete_count += 1
            # Part 2 - Generate autocomplete score
            temp_score = 0
            buffer.reverse()
            for char in buffer:
                temp_score *= 5
                temp_score += autocomplete_point_map[char]
            autocomplete_scores.append(temp_score)

    if len(autocomplete_scores) > 0:
        autocomplete_scores = sorted(autocomplete_scores)
        autocomplete_score = autocomplete_scores[round((len(autocomplete_scores) - 1) / 2)]

    return {'total': len(chunks), 'valid': valid_count, 'corrupt': corrupt_count, 'incomplete': incomplete_count,
            'error score': total_error_score, 'autocomplete score': autocomplete_score}


###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.01')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1&2 Mini Input (All 5 Valid Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.02')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1&2 Mini Input (All 4 Corrupt Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.03')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1&2 Mini Input (All 3 Incomplete Chunks): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-0.1')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1&2 Input (Error Score: 26397, Autocomplete Score: 288957): " + str(chunk_analysis))

###########################################

navigation_subsystem = ingest_list_of_strings('inputs/10-1')
chunk_analysis = analyse_subsystem_chunks(navigation_subsystem)
print("Part 1&2 Real (Error Score: 392139, Autocomplete Score: 4001832844): " + str(chunk_analysis))

###########################################
