
def play_dirac_dice_game(positions=[0, 0], target_score=1000, board_size=10, die=[100, False]):
    scores = [0, 0]
    roll = 0
    player = 0
    roll_3 = 0
    while max(scores) < target_score:
        roll_1 = roll_deterministic_die(roll_3)
        roll_2 = roll_deterministic_die(roll_1)
        roll_3 = roll_deterministic_die(roll_2)
        move = roll_1 + roll_2 + roll_3
        # print(str(roll_1) + ", " + str(roll_2) + ", " + str(roll_3))
        next_pos = ((positions[player] - 1 + move) % board_size) + 1
        scores[player] += next_pos
        positions[player] = next_pos
        # print(scores)
        player = (player + 1) % len(positions)
        # print(player)
        roll += 3
    return scores, roll


def roll_deterministic_die(last, sides=100):
    current = last + 1
    if current > sides:
        current = 1
    return current


###########################################

scores, rolls = play_dirac_dice_game([4, 8])
print("Part 1 - Test Input (739785): " + str(min(scores) * rolls))

###########################################

scores, rolls1 = play_dirac_dice_game([7, 3])
print("Part 1 - Real Input (551901): " + str(min(scores) * rolls1))

###########################################
