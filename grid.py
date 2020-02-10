from random import choice, random
import numpy as np
import time
import pickle

#assuming d1 is a dictionary that has all types of cell, and its shifts to left
#similarly d2, but its values are shifts to right.
with open('ds.pickle', 'rb') as var:
    ds =  pickle.load(var) #list of dicts
d1 = ds[0]  #dictionary containing left shift of all possible tuples of size 4, having elems from 0 to 2048, 2's powers
d2 = ds[1] #dictionary containing right shift of all possible tuples of size 4, having elems from 0 to 2048, 2's powers

def l(grid):
    l1=grid.copy()
    for i in range(4):
        l1[i] = d1[tuple(l1[i])]
    return l1

def r(grid):
    l1 = grid.copy()
    for i in range(4):
        l1[i] = d2[tuple(l1[i])]
    return l1

def u(grid):
    l1 = grid.copy()
    for i in range(4):
        l1[:,i] = d1[tuple(l1[:,i])]
    return l1

def d(grid):
    l1 = grid.copy()
    for i in range(4):
        l1[:,i] = d2[tuple(l1[:,i])]
    return l1

def c(grid, move):
    if move == 2: return l(grid)
    if move == 0: return u(grid)
    if move == 1: return d(grid)
    if move == 3: return r(grid)

def isvalid(grid):
    if 0 in grid: return True
    l = grid
    for i in range(3):
        for j in range(4):
            if l[i][j] == l[i+1][j]: return True
        if l[i][0] == l[i][1] or l[i][1] == l[i][2] or l[i][2] == l[i][3]: return True
    i = 3
    if l[i][0] == l[i][1] or l[i][1] == l[i][2] or l[i][2] == l[i][3]: return True
    return False

ind = np.arange(16).reshape(4,4)
def next_play(grid, move):
    #assumption: grid is 4 x 4 matrix
    if move not in range(4): return grid #invalid move.
    moved_grid = c(grid, move)           # c moves grid by specific move "move".
    moved = not (moved_grid == grid).all()
    if not moved: return grid # return as it was
    p = ind[moved_grid==0]
    if len(p) == 0: return moved_grid  #no spawn needed
    idx = choice(p) #randomly picked empty place's index
    moved_grid[idx//4][idx%4] = 2 if random() < .9 else 4
    return moved_grid

def rand_moves(data,first_move,times): #data is playing grid, numpy matrix 4 x 4
    assert times >0, 'Wrong value of times'
    score = 0
    k = range(4)
    for _ in range(times):
        data1 = data.copy()
        data1 = next_play(data1, first_move) #next_play moves grid & generate tile randomly on an empty place if moved
        while isvalid(data1):                #isvalid checks validity of grid, ie playable or not.
            data1 = next_play(data1, choice(k)) #choice is random.choice func.
            score+= data1.max()
    return score/times

def getAvailableMoves(data):
    data_list= [(c(data,i),i) for i in range(4)]
    ret = []
    for data1,i in data_list:
        if (data1==data).all():continue
        else:
            ret.append(i)
    return ret

def getMove(data, times = 10):
    sc, mv = float('-inf'), None
    for move in getAvailableMoves(data):
        score = 0
        score += rand_moves(data.copy(),move,times)
        if score > sc:
            sc= score
            mv = move
        elif score == sc:
            mv = choice([mv, move]) #randomly choose one of them
    return mv #if none, case handing occurs at caller side.

if __name__ == '__main__':
    data = np.asarray([[2,2,0,2],
                       [4,4,0,2],
                       [32,32,32,8],
                       [0,0,0,2]]) #a sample grid


    print(data)

    t1 = time.time()
    from sys import argv
    print(getMove(data, int(argv[1])))
    print(time.time() - t1, 's')





































