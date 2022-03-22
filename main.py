from symbol import except_clause
from numpy import False_
import pygame
from pygame.locals import KEYDOWN, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEWHEEL, QUIT
from random import randint, sample
from copy import deepcopy

idx_numbers = list(range(0, 9))
sample_numbers = list(range(1, 10))
cell_width = 100
grid_size = 9
w, h = cell_width * grid_size, cell_width * grid_size
grid_data = []
grid_sample_numbers = []


def init_grid():
    global grid_size, grid_data
    grid_data = []
    for i in range(grid_size):
        row_data = []
        for j in range(grid_size):
            row_data.append(0)
        grid_data.append(row_data)


def getRow(grid, i):
    return grid[i]


def getCol(grid, i):
    col = []
    for row in grid:
        col.append(row[i])
    return col

def setRow(grid,new_row, pos):
    grid[pos] = deepcopy(new_row)
    
def setCol(grid, new_col, pos):
    for i in range(9):
        grid[i][pos] = new_col[i]
            
    


def getSubGrid(grid, x, y):
    begin_i = x * 3
    end_i = begin_i + 3
    begin_j = y * 3
    end_j = begin_j + 3
    sub_grid = []
    for i in range(begin_i, end_i):
        sub_row = []
        for j in range(begin_j, end_j):
            sub_row.append(grid[i][j])
        sub_grid.append(sub_row)
    return sub_grid


def setSubGrid(grid, new_sublist, x, y):
    begin_i = x * 3
    end_i = begin_i + 3
    begin_j = y * 3
    end_j = begin_j + 3
    for i in range(begin_i, end_i):
        sub_row = []
        for j in range(begin_j, end_j):
            grid[i][j] = deepcopy(new_sublist[i * 3 + j])


def flatten2D(grid):
    res = []
    for row in grid:
        res.extend(row)
    return res
        
                

init_grid()

backtracks = 0

import random
def solveSudoku(grid, i=0, j=0):
    global backtracks
    i, j = findNextCellToFill(grid)
    if i == -1:
        return True
    random_list = random.sample(range(1,10),9)
    for e in random_list:
        if isValid(grid, i, j, e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            backtracks += 1
        grid[i][j] = 0
    return False


def findNextCellToFill(grid):
    for x in range(0, 9):
        for y in range(0, 9):
            if grid[x][y] == 0:
                return x, y
    return -1, -1


def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3 * (i//3), 3 * (j//3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if grid[x][y] == e:
                        return False
            return True
    return False


def printSudoku(grid):
    numrow = 0
    for row in grid:
        if numrow % 3 == 0 and numrow != 0:
            print(' ')
        print(row[0:3], ' ', row[3:6], ' ', row[6:9])
        numrow += 1
    print()


def deleteSoduke(grid, user_places, fixed_data):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            rnum = randint(0, 20)
            if rnum >19:
                grid[i][j] = 0
                user_places.append((i,j))
            else:
                fixed_data.append((i,j))

def isSolved(grid):
    # row
    for i in range(9):
        row = getRow(grid,i)
        duplicates = [number for number in row if row.count(number) > 1]
        unique_duplicates = list(set(duplicates))
        if len(unique_duplicates) > 0:
            return False
    print("rows passed!")
    # col
    for j in range(9):
        cols = getCol(grid, j)
        print(j, cols)
        duplicates = [number for number in cols if cols.count(number) > 1]
        unique_duplicates = list(set(duplicates))
        if len(unique_duplicates) > 0:
            return False  
    print("cols passed!")
    #sub_grid
    for y in range(3):
        for x in range(3):
            sub_grid = getSubGrid(grid, x, y)
            flat_grid = flatten2D(sub_grid)
            duplicates = [number for number in flat_grid if flat_grid.count(number) > 1]
            unique_duplicates = list(set(duplicates))
            if len(unique_duplicates) > 0:
                return False 
    print("subgrids passed!") 
    return True
       
        
def isSameGrid(grid1, grid2):
    for i in range(9):
        for j in range(9):
            if grid1[i][j] != grid2[i][j]:
                return False
    return True

def isAllFilled(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return False
    print("all filled!")
    return True
            
def swapsubBlock(grid, h1, h2, horiontal=True):
    temp = []
    if horiontal:
        for i in range(3):
            temp = deepcopy(grid[h1*3+i])
            grid[h1*3+i] = deepcopy(grid[h2*3+i])
            grid[h2*3+i] = deepcopy(temp)
    else:
        temp = [0] * 9
        for j in range(3):
            for i in range(9):
                temp[j] = grid[i][h1*3+j]
                grid[i][h1*3+j] = grid[i][h2*3+j]
                grid[i][h2*3+j] = temp[j]

def swapRow(grid, r1, r2):
    row1 = getRow(grid, r1)
    row2 = getRow(grid, r2)
    grid[r1] = deepcopy(row2)
    grid[r2] = deepcopy(row1)
    

def swapCol(grid, r1, r2):
    col1 = getCol(grid, r1)
    col2 = getCol(grid, r2)
    setCol(grid, col2, r1)
    setCol(grid, col1, r2)

    
pygame.init()
clock = pygame.time.Clock()
SURFACE = pygame.display.set_mode((w, h))
board_img = pygame.image.load("./images/board.png")
board_img = pygame.transform.scale(board_img, (w, h))

back_img = pygame.image.load("./images/back.png")
back_img = pygame.transform.scale(back_img, (cell_width, cell_width))

num_imgs = []
for i in range(0, grid_size + 1):
    img = pygame.image.load(f"./images/{str(i)}.png")
    num_imgs.append(pygame.transform.scale(img, (cell_width, cell_width)))

num_fixed_imgs = []
for i in range(0, grid_size + 1):
    print(f"./images/{str(i)}f.png")
    if i==0:
        img = pygame.image.load(f"./images/{str(i)}.png")
    else:
        img = pygame.image.load(f"./images/{str(i)}f.png")
    num_fixed_imgs.append(pygame.transform.scale(img, (cell_width, cell_width)))
    

running = True
pressed = False
clicked = False
number = 0
pos_x, pos_y = 0, 0

init_grid()
print("init")
printSudoku(grid_data)
rlist = sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
# print(rlist)
k = 0
num_block_row = randint(0,2)
num_block_col = randint(0,2)
setSubGrid(grid_data, rlist, num_block_row, num_block_col)

print(grid_data)
solveSudoku(grid_data)
print("solved")
printSudoku(grid_data)

num_shuffles = randint(20, 100)
print("swapping sub bolcks")
for _ in range(num_shuffles):
    V1, V2 = sample([0, 1, 2], 2)
    swapsubBlock(grid_data, V1, V2, horiontal=randint(0, 1))
    printSudoku(grid_data)

print("swapping rows in subblocks")
for i in range(num_shuffles):
    block_row_num = randint(0,2)
    V1, V2 = sample([0, 1, 2], 2)
    V1 = V1 + block_row_num * 3
    V2 = V2 + block_row_num * 3
    swapRow(grid_data, V1, V2)
    printSudoku(grid_data)

print("swapping cols in subblocks")
for i in range(num_shuffles):
    block_row_num = randint(0,2)
    V1, V2 = sample([0, 1, 2], 2)
    V1 = V1 + block_row_num * 3
    V2 = V2 + block_row_num * 3
    swapCol(grid_data, V1, V2)
    printSudoku(grid_data)
    input()   

printSudoku(grid_data)
user_places = []
fixed_places =[]
deleteSoduke(grid_data, user_places, fixed_places)
solved_data = deepcopy(grid_data)
solveSudoku(solved_data)


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                init_grid()
            if event.key == pygame.K_s:
                solveSudoku(grid_data)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
            clicked = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if pressed:
                pos_x, pos_y = pygame.mouse.get_pos()
                pressed = False
                clicked = False
                if pos_x > 10 and pos_x < w - 10 and pos_y > 10 and pos_y < h - 10:
                    j_q = int(pos_x / cell_width)
                    i_q = int(pos_y / cell_width)
                    print(solved_data[i_q][j_q])
                    (i_q, j_q) in user_places
                    if (i_q, j_q) in user_places:
                        grid_data[i_q][j_q] = number
                        number += 1
                        if number > 9:
                            number = 1
                        clicked = True
                

    if clicked:
        if isAllFilled(grid_data):
            if isSolved(grid_data):
                print("solved !")
                running = False
    SURFACE.fill((255, 255, 255))
    
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) in fixed_places:
                SURFACE.blit(num_fixed_imgs[grid_data[i][j]],(j * cell_width, i * cell_width))
            else:
                SURFACE.blit(num_imgs[grid_data[i][j]],(j * cell_width, i * cell_width))
    for i in range(9):
        for j in range(9):
            rect = (i * cell_width, j*cell_width, cell_width, cell_width)
            pygame.draw.rect(SURFACE, (0,0,0), rect, 2)


    for i in range(3):
        for j in range(3):
            rect = (i * cell_width*3, j*cell_width*3, cell_width*3, cell_width*3)
            pygame.draw.rect(SURFACE, (0,0,0), rect, 5)
            
    
    
    pygame.display.update()
    clock.tick(60)


pygame.quit()
