import functools
import itertools


def play_dirac_dice_game(positions=[0, 0], target_score=1000, board_size=10):
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


@functools.lru_cache(maxsize=None)
def play_dirac_dice_game_part2(pos_1, pos_2, score_1=0, score_2=0, target_score=21, board_size=10):
    wins_1 = wins_2 = 0
    for roll_1, roll_2, roll_3 in itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3)):
        move = roll_1 + roll_2 + roll_3
        next_pos = ((pos_1 - 1 + move) % board_size) + 1
        new_score_1 = score_1 + next_pos
        new_pos_1 = next_pos
        if new_score_1 >= target_score:
            # Just rolled won
            wins_1 += 1
        else:
            # Not winner, so next player goes
            sub_wins_2, sub_wins_1 = play_dirac_dice_game_part2(pos_2, new_pos_1, score_2, new_score_1)
            wins_1 += sub_wins_1
            wins_2 += sub_wins_2
    return wins_1, wins_2


###########################################

scores, rolls = play_dirac_dice_game([4, 8])
print("Part 1 - Test Input (739785): " + str(min(scores) * rolls))

###########################################

scores, rolls = play_dirac_dice_game([7, 3])
print("Part 1 - Real Input (551901): " + str(min(scores) * rolls))

###########################################

player_wins = play_dirac_dice_game_part2(4, 8)
print("Part 2 - Test Input (444356092776315): " + str(max(player_wins)))

###########################################

player_wins = play_dirac_dice_game_part2(7, 3)
print("Part 2 - Real Input (272847859601291): " + str(max(player_wins)))

###########################################