import math
import regex as re


def ingest_list_of_snailfish_numbers(filename):
    with open(filename) as file:
        lines = [i.strip() for i in file.readlines()]
    return lines


def summation(nums):
    z = nums.pop(0)
    for w in nums:
        z = addition(z, w)
    return z


def addition(x, y):
    z = '[' + x + ',' + y + ']'
    z = reduce(z)
    return z


def reduce(z):
    # First explode if needed, then reduce again
    z_new = explode_if_needed(z)
    if z_new != z:
        z_new = reduce(z_new)
        return z_new
    # Secondly split if needed, then reduce again
    z_new = split_if_needed(z)
    if z_new != z:
        z_new = reduce(z_new)
        return z_new
    # Otherwise it's all completely reduced
    return z


def explode_if_needed(z):
    # If any pair is nested inside four pairs, the leftmost such pair explodes.
    matches = re.finditer(r"(?<=(?:\[.*){4,})\[[0-9]+,[0-9]+\](?=(?:.*\]){4,})", z)
    for match in matches:
        pre_pair = z[:match.start()]
        post_pair = z[match.end():]

        # Exclude if previous open parenthesis or later closed parenthesis have been cancelled out.
        non_cancelled_openers = pre_pair.count('[') - pre_pair.count(']')
        non_cancelled_closers = post_pair.count(']') - post_pair.count('[')
        if non_cancelled_openers < 4 or non_cancelled_closers < 4:
            continue

        # Add the left number to the left
        left = int(re.findall(r"[0-9]+", match.group())[0])
        left_target = re.search(r"(\d+)(?!.*\d)", pre_pair)
        if left_target:
            pre_target = pre_pair[:left_target.start()]
            post_target = pre_pair[left_target.end():]
            total = str(left + int(left_target.group()))
            pre_pair = pre_target + total + post_target

        # Add the right number to the right
        right = int(re.findall(r"[0-9]+", match.group())[-1])
        right_target = re.search(r"(?<!\d.*)(\d+)", post_pair)
        if right_target:
            pre_target = post_pair[:right_target.start()]
            post_target = post_pair[right_target.end():]
            total = str(right + int(right_target.group()))
            post_pair = pre_target + total + post_target

        # Return new z, and don't check other matches
        return pre_pair + '0' + post_pair

    # Otherwise, no need to explode anything
    return z


def split_if_needed(z):
    # If any regular number is 10 or greater, the leftmost such regular number splits.
    match = re.search(r"(?<=[^\d]*)\d{2,}", z)
    if match:
        value = int(match.group())
        pre_value = z[:match.start()]
        new_pair = '[' + str(math.floor(float(value) / 2)) + ',' + str(math.ceil(float(value) / 2)) + ']'
        post_value = z[match.end():]
        return pre_value + new_pair + post_value
    return z


def magnitude(z):
    match = re.search(r"\[[0-9]+,[0-9]+\]", z)
    while match:
        left = int(re.findall(r"[0-9]+", match.group())[0])
        right = int(re.findall(r"[0-9]+", match.group())[-1])
        pre_pair = z[:match.start()]
        mag = str((3 * left) + (2 * right))
        post_pair = z[match.end():]
        z = pre_pair + mag + post_pair
        match = re.search(r"\[[0-9]+,[0-9]+\]", z)
    return int(z)


def find_largest_magnitude(nums):
    largest_mag = 0
    for x in nums:
        for y in nums:
            if x == y:
                continue
            mag = magnitude(addition(x, y))
            if mag > largest_mag:
                largest_mag = mag
    return largest_mag


###########################################

print("Part 1 - Explosion - Mini Test 1: " + str(explode_if_needed('[[[[[9,8],1],2],3],4]') == '[[[[0,9],2],3],4]'))
print("Part 1 - Explosion - Mini Test 2: " + str(explode_if_needed('[7,[6,[5,[4,[3,2]]]]]') == '[7,[6,[5,[7,0]]]]'))
print("Part 1 - Explosion - Mini Test 3: " + str(explode_if_needed('[[6,[5,[4,[3,2]]]],1]') == '[[6,[5,[7,0]]],3]'))
print("Part 1 - Explosion - Mini Test 4: " + str(
    explode_if_needed('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))
print("Part 1 - Explosion - Mini Test 5: " + str(
    explode_if_needed('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]') == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'))

###########################################

print("Part 1 - Split - Mini Test 1: " + str(split_if_needed('[10]') == '[[5,5]]'))
print("Part 1 - Split - Mini Test 2: " + str(split_if_needed('[1,[2,[11]]]') == '[1,[2,[[5,6]]]]'))
print("Part 1 - Split - Mini Test 3: " + str(split_if_needed('[12]') == '[[6,6]]'))

###########################################

print("Part 1 - Addition - Mini Test 1: " + str(
    addition('[[[[4,3],4],4],[7,[[8,4],9]]]', '[1,1]') == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'))

###########################################

print("Part 1 - Summation - Mini Test 1: " + str(
    summation(['[1,1]', '[2,2]', '[3,3]', '[4,4]']) == '[[[[1,1],[2,2]],[3,3]],[4,4]]'))
print("Part 1 - Summation - Mini Test 2: " + str(
    summation(['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]']) == '[[[[3,0],[5,3]],[4,4]],[5,5]]'))
print("Part 1 - Summation - Mini Test 3: " + str(
    summation(['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]']) == '[[[[5,0],[7,4]],[5,5]],[6,6]]'))
numbers = ingest_list_of_snailfish_numbers('inputs/18-0.1')
print("Part 1 - Summation - Test Input 1: " + str(
    summation(numbers) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'))
numbers = ingest_list_of_snailfish_numbers('inputs/18-0.2')
print("Part 1 - Summation - Test Input 2: " + str(
    summation(numbers) == '[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]'))

###########################################

print("Part 1 - Magnitude - Mini Test 1: " + str(magnitude('[9,1]') == 29))
print("Part 1 - Magnitude - Mini Test 2: " + str(magnitude('[1,9]') == 21))
print("Part 1 - Magnitude - Mini Test 3: " + str(magnitude('[[9,1],[1,9]]') == 129))
print("Part 1 - Magnitude - Mini Test 4: " + str(magnitude('[[1,2],[[3,4],5]]') == 143))
print("Part 1 - Magnitude - Mini Test 5: " + str(magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384))
print("Part 1 - Magnitude - Mini Test 6: " + str(magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445))
print("Part 1 - Magnitude - Mini Test 7: " + str(magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791))
print("Part 1 - Magnitude - Mini Test 8: " + str(magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137))
print("Part 1 - Magnitude - Mini Test 9: " + str(
    magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488))
numbers = ingest_list_of_snailfish_numbers('inputs/18-0.2')
print("Part 1 - Magnitude - Test Input 2: " + str(magnitude(summation(numbers)) == 4140))

###########################################

print("Part 1 Real 1: " + str(magnitude('[9,1]') == 29))
print("Part 1 - Magnitude - Mini Test 2: " + str(magnitude('[1,9]') == 21))
print("Part 1 - Magnitude - Mini Test 3: " + str(magnitude('[[9,1],[1,9]]') == 129))
print("Part 1 - Magnitude - Mini Test 4: " + str(magnitude('[[1,2],[[3,4],5]]') == 143))
print("Part 1 - Magnitude - Mini Test 5: " + str(magnitude('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]') == 1384))
print("Part 1 - Magnitude - Mini Test 6: " + str(magnitude('[[[[1,1],[2,2]],[3,3]],[4,4]]') == 445))
print("Part 1 - Magnitude - Mini Test 7: " + str(magnitude('[[[[3,0],[5,3]],[4,4]],[5,5]]') == 791))
print("Part 1 - Magnitude - Mini Test 8: " + str(magnitude('[[[[5,0],[7,4]],[5,5]],[6,6]]') == 1137))
print("Part 1 - Magnitude - Mini Test 9: " + str(
    magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') == 3488))
numbers = ingest_list_of_snailfish_numbers('inputs/18-0.2')
print("Part 1 - Magnitude - Test Input 2: " + str(magnitude(summation(numbers)) == 4140))

###########################################

numbers = ingest_list_of_snailfish_numbers('inputs/18-1')
print("Part 1 - Magnitude - Real Input: " + str(magnitude(summation(numbers)) == 4173))

###########################################

numbers = ingest_list_of_snailfish_numbers('inputs/18-0.2')
print("Part 2 - Largest Magnitude - Test Input: " + str(find_largest_magnitude(numbers) == 3993))

###########################################

numbers = ingest_list_of_snailfish_numbers('inputs/18-1')
print("Part 2 - Largest Magnitude - Real Input: " + str(find_largest_magnitude(numbers) == 4706))

###########################################
