WIDTH = 12
HEIGHT = 14
EMPTY = "_"
BLOCK = "@"

T_BLOCK = [[False, False, False],[True, True, True],[False,True,False]]
S_BLOCK_F = [[False, False, True],[False, True, True],[False,True,False]]
S_BLOCK_B = [[False,True,False],[False, True, True],[False,False,True]]
I_BLOCK = [[j == 0] * 4 for j in range(4)]
SQUARE_BLOCK = [[True, True], [True, True]]
from random import *

BLOCKS = [T_BLOCK,S_BLOCK_F,S_BLOCK_B,SQUARE_BLOCK, I_BLOCK]

def get_random_block():
    return([row[::] for row in BLOCKS[randint(0,len(BLOCKS)-1)]])

board = [[EMPTY for i in range(HEIGHT)] for i in range(WIDTH)]
for i in range(WIDTH):
    board[i][HEIGHT-1] = BLOCK


def print_board():
    temp_board = [row[::] for row in board]
    block_width = len(current_block)
    for i in range(block_width**2):
        if (blockX+ i%block_width<WIDTH) and current_block[i%block_width][int(i//block_width)]:
            temp_board[int(blockX+i%block_width)][int(blockY - 1 + i//block_width)] = BLOCK
    print("\n".join(["".join([temp_board[x][y] for x in range(WIDTH)]) for y in range(HEIGHT)]))

def game_over():
    return any(board[x][0] == BLOCK for x in range(WIDTH))
def drop():
    global current_block, blockX, blockY, block_width
    current_block = get_random_block()
    blockX = WIDTH //2 - 1
    blockY = 1
    block_width = len(current_block)
    stuck = any(any(board[int(blockX+i)][int(blockY+j)]==BLOCK and current_block[i][j] for i in range(block_width)) for j in range(block_width))
    if stuck:
        print_board()
        print("GAME OVER!")
        quit(0)

def block_intersects_with_map():
    return any(any(((blockX+offX)<WIDTH) and board[int(blockX+offX)][int(blockY+offY)]==BLOCK and current_block[int(offX)][int(offY)] for offX in range(block_width)) for offY in range(block_width))
def solidify_block():
    for i in range(block_width**2):
        if current_block[int(i%block_width)][int(i//block_width)]:
            board[int(blockX+i%block_width)][int(blockY + i//block_width)] = BLOCK
def right():
    return (blockX+1, blockY, current_block)

def left():
    return (blockX-1, blockY, current_block)
def rotate():
    poss_block = [row[::] for row in current_block]
    if block_width<=2:
        return poss_block
    if block_width == 3:
        copy = [row[::] for row in poss_block]
        poss_block = [[copy[0][2],copy[1][2],copy[2][2]],[copy[0][1],copy[1][1],copy[2][1]],[copy[0][0],copy[1][0],copy[2][0]]]
    if block_width == 4:
        copy = [row[::] for row in poss_block]
        for x in range(block_width):
            for y in range(block_width):
                new_x = block_width - x -1
                new_y = block_width - y - 1
                poss_block[x][y] = current_block[new_y][new_x]
    return (blockX, blockY, poss_block)
def rotate2():
    poss_block = [row[::] for row in current_block]

    for x in range(block_width//2):
        for y in range(block_width//2):
            poss_block[block_width - x-1][y] = current_block[x][y]
            poss_block[block_width - x-1][block_width - y-1] = current_block[block_width - y-1][x]
            poss_block[x][block_width - y-1] = current_block[block_width - y-1][block_width -x-1]
            poss_block[x][y] = current_block[block_width - y-1][x]

    return (blockX, blockY, poss_block)

def rotate3():
    poss_block = [row[::] for row in current_block]
    mat = poss_block
    N = block_width
    for x in range(block_width//2):
        for y in range(x, N - x - 1):

            temp = poss_block[x][y];
            mat[x][y] = mat[y][N-1-x];
            mat[y][N-1-x] = mat[N-1-x][N-1-y];
            mat[N-1-x][N-1-y] = mat[N-1-y][x];
            mat[N-1-y][x] = temp;
    return blockX, blockY, mat
def do_nothing():
    """
    They say it's impossible, but I do it all the time
    :return:
    """
    return (blockX, blockY+1, current_block)
def bad_x(x):
    return x<0 or x>=WIDTH
def bad_y(y):
    return y<0 or y>=HEIGHT
def is_valid_location(tup):

    for i in range(int(block_width)):
        for j in range(int(block_width)):
            if tup[2][i][j] and (bad_x(tup[0]+i) or bad_y(tup[1]+j) or board[int(tup[0]+i)][int(tup[1]+j)]==BLOCK):
                return False


    return True

current_block = None
blockX = None
blockY = None
block_width = None
drop()



while True:
    for i in range(3, HEIGHT-1):
        if all(board[x][i]== BLOCK for x in range(WIDTH)):
            for j in range(i):
                height = i - j
                for x in range(WIDTH):
                    board[x][height] = board[x][height - 1]
    print_board()
    move = input("Make a move... 0 means move left... 1 means move right... 2 ... means rotate 3... do nothing")

    move = move if move in list(str(i) for i in range(4)) else 3
    temp_tup = ([left, right, rotate3, do_nothing][int(move)])()
    if is_valid_location(temp_tup):
        blockX = temp_tup[0]
        blockY = temp_tup[1]
        current_block = temp_tup[2]
    elif move ==3:
        solidify_block()
        drop()
        if game_over():
            break

print_board()
print("GAME OVER!")
quit(0)