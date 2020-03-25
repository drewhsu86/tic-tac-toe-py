# time is imported to allow program to wait (time.sleep(seconds)) before computer moves
import time

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
#             return type: integer (index of 9 length array)
#         executeMove(move, player)
#             return type: none
#             side effect: changes board using move and player
#               i) waits 5 sec
#               ii) calls cpuMove and gets an integer
#               iii) execute move (assumes move is legal based on cpuMove)
#               iv) askForMove is called again (should have an overall game loop)
#             player can just be 1 and 2 (1 is always human, 2 is cpu)
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
board = [0]*9


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
        print ('-------------')
    print('  a   b   c  ')


def askForMove():
    # prints board then asks for and parses input
    print ('')
    print ('Player\'s turn to go!')
    print('')
    printBoard()
    # ask for left (abc) and then up (123) coordinates
    left = up = 0
    while True:
        left = input('Input Left Coordinate (a, b or c): ').lower()
        if left != 'a' and left != 'b' and left != 'c':
            print ('Input not recognized. Please try again.')
        else:
            break
    while True:
        up = input('Input Up Coordinate (1, 2 or 3): ').lower()
        if up != '1' and up != '2' and up != '3':
            print ('Input not recognized. Please try again.')
        else:
            break
    print ('')
    print ('Move made: ' + left + ', ' + up)
    print ('')
    board[coordToIndex(left, up)] = 1
    printBoard()


# main game loop start
# hopefully with the quit option inside askForMove(), we won't freeze our computer

def gameLoop():
    askForMove()


# start game loop here:
gameLoop()
