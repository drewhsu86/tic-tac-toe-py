# time is imported to allow program to wait (time.sleep(seconds)) before computer moves
# sys is imported for sys.exit()
import time
import sys

# tictactoe practice app
# Part 1: Design
#    This is practice for making python arrays, functions and loops
#    To be played in the command line
#
#     1) Notes:
#         Python version 2.7 uses raw_input, 3.6 uses input
#         Don't know how to slice an array like in Javascript without importing
#         Don't want to use iteration, so when evaluating cpu moves
#         The AI will alter the board, grade the board, then change it back to 0
#         0 is empty, 1 is human, 2 is cpu
#
#     2) Game data storage
#       a) game board: can be stored as array, or array of array
#       b) since the gameboard is only (and always) 3x3, we will write
#          an array with a length of 9 (and write functions to operate on it)
#       c) inputs need to make sense to the user so we will do
#           a, b, c on the horizontal axis and
#           1, 2, 3 on the vertical axis
#           Inputs will ask for a horizontal and vertical move and error check
#           Then will check for move legality by converting to a single array index
#           Then will fork between executing move or ask for another move
#
#      3) Game methods/functions
#         Assumes user always goes first
#         Computer reads board as an array and outputs a move as one index
#         There will be one "cpuMove" function and one "executeMove" function
#
#         cpuMove()
#             return type: integer (index of 9 length array) of best move
#         gradeMove(move)
#             returns a value of how good the move is based on heuristic
#             parameter move is 0 thru 8
#
#         askForMove()
#             return type: none
#             side effect: ask for player input using print and raw_input or input
#             can have "enter q to quit"
#         printBoard()
#             return type: none
#             side effect: print the board as a 3x3 instead of a 9 length array
#
#       4) Heuristics grading
#         3 in a row for "2" = 1000
#         "almost 3" for "2" = 10
#         3 in a row for "1" = -1000
#         "almost 3" for "1" = -10
#         There are only 8 ways to win (3 side, 3 up/down, and 2 diagonals)
#         so these checks can be done quickly
#         e.g. read diagonal = read positions 0, 4, 8 and see if it has all 2's
#         or only 2x 2's and 1x 0
#  ------------------------------------------------------------------------------


# initialize our board
board = [0] * 9
cheatmode = 0
lookAhead = 2
t1 = [0, 1, 2]
t2 = [3, 4, 5]
t3 = [6, 7, 8]
t4 = [0, 3, 6]
t5 = [1, 4, 7]
t6 = [2, 5, 8]
t7 = [0, 4, 8]
t8 = [2, 4, 6]
triplets = [t1, t2, t3, t4, t5, t6, t7, t8]


def numToXO(n):
    # converts 0, 1 or 2 to X, O or a space string
    if n == 0:
        return ' '
    elif n == 1:
        return 'X'
    elif n == 2:
        return 'O'
    else:
        return 'er'


def coordToIndex(x, y):
    # assumes the inputs have already been vetted so no error checking
    X = Y = 0
    if x == 'a':
        X = 0
    elif x == 'b':
        X = 1
    elif x == 'c':
        X = 2

    if y == '1':
        Y = 0
    elif y == '2':
        Y = 1
    elif y == '3':
        Y = 2

    return X + Y*3


def printBoard():
    # use for loop to print the board
    for x in range(3):
        # range of 3 means zero to three

        print('| ' + numToXO(board[0+x*3]) + ' | ' +
              numToXO(board[1 + x*3]) + ' | ' + numToXO(board[2 + x*3]) + ' | ' + str(x+1))
        print('-------------')
    print('  a   b   c  ')


def askForMove():
    # prints board then asks for and parses input
    print('')
    print('Player\'s turn to go!')
    print('')
    printBoard()
    print('')
    # ask for left (abc) and then up (123) coordinates
    left = up = 0
    while True:
        while True:
            left = input('Input Left Coordinate (a, b or c): ').lower()
            if left != 'a' and left != 'b' and left != 'c' and left != 'q':
                print('Input not recognized. Please try again.')
            elif left == 'q':
                sys.exit()
            else:
                break
        while True:
            up = input('Input Up Coordinate (1, 2 or 3): ').lower()
            if up != '1' and up != '2' and up != '3' and up != 'q':
                if up == 'cheat':
                    cheatmode = 1
                print('Input not recognized. Please try again.')
            elif up == 'q':
                sys.exit()
            else:
                break
        if board[coordToIndex(left, up)] == 0:
            print('')
            print('Move made: ' + left + ', ' + up)
            print('')
            board[coordToIndex(left, up)] = 1
            break
        else:
            print('')
            print('This space is not empty.')
            print('')

    printBoard()


def cpuMove():
    # for all possible moves, grade the move and pick the highest graded one
    # save an array of moves where it stores submatrices [move, score]

    print('')
    print('CPU is thinking!!! [[o_o]')
    print('')
    time.sleep(1)

    movelist = []
    for move in range(9):
        # check if move is legal, then add it to array moveList after grading
        if board[move] == 0:
            grade = gradeMove(move, lookAhead, 2)
            print('Calculating: ' + str(move) + ': ' + str(grade) + ' ... ')
            movelist.append([move, grade])
    # after the for loop, movelist should be filled up
    # if movelist is empty that means there's no free spaces
    if len(movelist) == 0:
        print('Looks like a tie, human. Hit ENTER to restart.')
        restart()
    # find the max grade in movelist and do that move
    maxGrade = movelist[0]
    # print(movelist)
    for movegrade in movelist:
        if movegrade[1] > maxGrade[1]:
            maxGrade = movegrade
    # maxgrade should be an array holding the [move, grade]
    AImove = maxGrade[0]
    board[AImove] = 2


def gradeMove(move, level, player):
    # change board at the beginning, but then change it back at the end
    board[move] = player
    # printBoard()
    # level used to determine how many moves to look ahead
    if level == 0:
        return 0
    # we check 8 ways to win and only want to look at 2 types
    # win: 3x 2   =     1000
    # threaten win: 2x 2, 1x 0 (if last one is 1, can't play winning move)
    # = 10
    # lose: 3x 1   =   -1000
    # threaten lose: 2x 1, 1x 0
    # = -10

    score = 0

    # if this current move is a diagonal it gets +/- 1
    # diagonals are on spaces 0, 2, 6, 8
    if move == 0 or move == 2 or move == 6 or move == 8:
        score = score + player*2 - 3

    for triplet in triplets:
        numE = numX = numO = 0
        for p in triplet:
            piece = board[p]
            if piece == 0:
                numE = numE + 1
            elif piece == 1:
                numX = numX + 1
            elif piece == 2:
                numO = numO + 1
        # count score for this triplet
        # if it meets a condition, add it to score
        if numX == 3:
            score = score - 1000
        elif numO == 3:
            score = score + 1000
        elif numE == 1:
            if numX == 2:
                score = score - 10
            elif numO == 2:
                score = score + 10
    # end of for loop through each triplet

    nextPlayer = 2
    if player == 2:
        nextPlayer = 1

    maxDamage = 0
    for nextmove in range(9):
        if board[nextmove] == 0:
            # print('examining move ' + str(nextmove) + ' at level ' + str(level))
            nextscore = gradeMove(nextmove, level - 1, nextPlayer)
            board[nextmove] = 0
            if nextscore < maxDamage:
                # print(nextscore)
                maxDamage = nextscore
    score = score + maxDamage

    # remember to change board back at the end
    board[move] = 0
    return score


def spaceLeft():
    for p in board:
        if p == 0:
            return True
    return False


def restart():
    for space in range(9):
        board[space] = 0
    gameLoop()


def checkWin():
    # since only 8 ways, we can hardcode in 8 length=3 matrices nested in a matrix
    # t for triplet
    for triplet in triplets:
        numE = numX = numO = 0
        for p in triplet:
            piece = board[p]
            if piece == 0:
                numE = numE + 1
            elif piece == 1:
                numX = numX + 1
            elif piece == 2:
                numO = numO + 1
        # count score for this triplet
        # if it meets a condition, add it to score
        # print(str(numX) + ', ' + str(numO))
        if numX == 3:
            return 1
        elif numO == 3:
            return 2
    return 0
    # end of for loop through each triplet

# main game loop start
# hopefully with the quit option inside askForMove(), we won't freeze our computer


def gameLoop():
    while True:
        askForMove()

        if checkWin() == 1:
            print('')
            print('******************************')
            printBoard()
            print(' You wonnered!!! [[\'o\']')
            print('******************************')
            restart()

        cpuMove()

        if checkWin() == 2:
            print('')
            print('******************************')
            printBoard()
            print(' You loosed [[._.] ')
            print('******************************')
            restart()


# start game loop here:
while True:
    difficulty = input('\n Enter difficulty 1-3:  ')
    print('')
    if difficulty == '1':
        lookAhead = 1
        print('Stupid CPU mode')
        break
    elif difficulty == '2':
        lookAhead = 3
        print('Normie CPU mode')
        break
    elif difficulty == '3':
        lookAhead = 5
        print('Robot Overlord CPU mode')
        break
    else:
        print('Are you sure you understand directions?')
print('---------------------')

gameLoop()
