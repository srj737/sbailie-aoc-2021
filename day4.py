def ingestBingoSubprocess(filename):
    with open(filename) as file:
        ingest = file.readlines()
        ingest = [line.strip() for line in ingest]
    calls = [int(i) for i in (ingest.pop(0)).split(',')]
    boards, currentBoard = [], []
    ingest.pop(0)  # Remove first empty line
    while len(ingest) > 0:
        currentLine = [int(i) for i in ingest.pop(0).split()]
        if currentLine == []:
            boards.append(currentBoard.copy())
            currentBoard = []
        else:
            currentBoard.append(currentLine)
    boards.append(currentBoard.copy())
    return {'calls': calls, 'boards': boards}


def playBingo(bingoInput, boardsToWin = 1):
    boards = bingoInput['boards']
    calls = bingoInput['calls']
    called = []
    winningScore = 0
    boardsWon = [0] * len(boards)
    while len(calls) > 0 and boardsWon.count(1) < boardsToWin:
        call = calls.pop(0)
        called.append(call)
        for index, board in enumerate(boards):
            winningScore = checkBingoBoard(board, called)
            if winningScore != 0:
                boardsWon[index] = 1
                if boardsWon.count(1) == boardsToWin:
                    break
    return winningScore


def checkBingoBoard(board, called):
    won = False

    # Check horizonal
    for row in board:
        if all(elem in called for elem in row):
            won = True
            break

    # Check vertical (transpose then check horizonal)
    if not won:
        board = list(map(list, zip(*board)))
        # Check horizonal
        for row in board:
            if all(elem in called for elem in row):
                won = True
                break

    # If won, count the score
    if won:
        lastCall = called[-1]
        unmatchedSum = 0
        for row in board:
            for value in row:
                if value not in called:
                    unmatchedSum += value
        return lastCall * unmatchedSum

    return 0


###########################################

bingoInput = ingestBingoSubprocess('inputs/4-0.1')
bingoResult = playBingo(bingoInput)
print("Part 1 Test Input (4512): " + str(bingoResult))

###########################################

bingoInput = ingestBingoSubprocess('inputs/4-1')
bingoResult = playBingo(bingoInput)
print("Part 1 Real Input (27027): " + str(bingoResult))

# ###########################################

bingoInput = ingestBingoSubprocess('inputs/4-0.1')
bingoResult = playBingo(bingoInput, len(bingoInput['boards']))
print("Part 2 Test Input (1924): " + str(bingoResult))

###########################################

bingoInput = ingestBingoSubprocess('inputs/4-1')
bingoResult = playBingo(bingoInput, len(bingoInput['boards']))
print("Part 2 Real Input (36975): " + str(bingoResult))

###########################################