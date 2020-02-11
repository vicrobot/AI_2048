from random import choice, random
import numpy as np
cimport numpy as np
cimport numpy as cnp
import time
cimport cython

#cnp.ndarray[cnp.int64_t, ndim=2]
@cython.boundscheck(False)
def left(np.ndarray grid):
    #assumption: grid is 4 x 4 numpy matrix 
    cdef np.ndarray l = grid.copy()
    cdef int j, i, p, merged;
    cdef long t;
    cdef list res;
    for j in range(4):
        res = [];
        merged = 0
        for i in range(4):
            t = l[j][-i-1]
            if t == 0: continue
            if res and t == res[-1] and merged == 0:
                res[-1]+=t
                merged = 1
            else:
                if res: merged = 0
                res+=[t]
        for p in range(4-len(res)): res = [0]+res
        l[j] = res[::-1]
        #l[j][0], l[j][1], l[j][2], l[j][3] = res[3], res[2], res[1], res[0]
    return l

@cython.boundscheck(False)
def right(np.ndarray grid):
    cdef np.ndarray l = grid.copy()
    cdef int j, i, p, merged;
    cdef long t;
    cdef list res;
    for j in range(4):
        res = []
        merged = 0
        for i in range(4):
            t = l[j][i]
            if t == 0: continue
            if res and t == res[-1] and merged == 0:
                res[-1]+=t
                merged = 1
            else:
                if res: merged = 0
                res+=[t]
        for p in range(4-len(res)): res = [0]+res
        l[j] = res
    return l

@cython.boundscheck(False)
def down(np.ndarray grid):
    cdef np.ndarray l = grid.copy()
    cdef int j, i, p, merged;
    cdef long t;
    cdef list res;
    for j in range(4):
        res = []
        merged = 0
        for i in range(4):
            t = l[i][j]
            if t == 0: continue
            if res and t == res[-1] and merged == 0:
                res[-1]+=t
                merged = 1
            else:
                if res: merged = 0
                res+=[t]
        for p in range(4-len(res)): res=[0]+res
        l[:, j] = res
    return l

@cython.boundscheck(False)
def up(np.ndarray grid):
    cdef np.ndarray l = grid.copy()
    cdef int j, i, p, merged;
    cdef long t;
    cdef list res;
    for j in range(4):
        res = []
        merged = 0
        for i in range(4):
            t = l[-i-1][j]
            if t == 0: continue
            if res and t == res[-1] and merged == 0:
                res[-1]+=t
                merged = 1
            else:
                if res: merged = 0
                res+=[t]
        for p in range(4-len(res)): res=[0]+res
        l[:, j] = res[::-1]
    return l

@cython.boundscheck(False)
@cython.wraparound(False)
def c(np.ndarray grid, int move):
    if move == 2: return left(grid)
    if move == 0: return up(grid)
    if move == 1: return down(grid)
    if move == 3: return right(grid)
    
@cython.boundscheck(False)
@cython.wraparound(False)
def isvalid(np.ndarray l):#l is grid
    if 0 in l: return True
    cdef int i, j;
    for i in range(3):
        for j in range(4):
            if l[i][j] == l[i+1][j]: return True
        if l[i][0] == l[i][1] or l[i][1] == l[i][2] or l[i][2] == l[i][3]: return True
    i = 3
    if l[i][0] == l[i][1] or l[i][1] == l[i][2] or l[i][2] == l[i][3]: return True
    return False

cdef np.ndarray ind = np.arange(16).reshape(4,4)

@cython.boundscheck(False)
@cython.wraparound(False)
def next_play(np.ndarray grid, int move):
    #assumption: grid is 4 x 4 matrix
    if move not in range(4): return grid #invalid move.
    cdef np.ndarray moved_grid = c(grid, move)           # c moves grid by specific move "move".
    cdef int moved = (moved_grid == grid).all()^1
    if moved == 0: return grid # return as it was
    cdef np.ndarray p = ind[moved_grid==0]
    if len(p) == 0: return moved_grid  #no spawn needed
    cdef int idx = choice(p) #randomly picked empty place's index
    moved_grid[idx//4][idx%4] = 2 if random() < .9 else 4
    return moved_grid

@cython.boundscheck(False)
def rand_moves(np.ndarray data,int first_move,int times): #data is playing grid, numpy matrix 4 x 4
    assert times >0, 'Wrong value of times'
    cdef int score = 0;
    k = range(4)
    cdef int p,m;
    cdef np.ndarray data1;
    for p in range(times):
        data1 = data.copy()
        data1 = next_play(data1, first_move) #next_play moves grid & generate tile randomly on an empty place if moved
        m = data.max()
        while isvalid(data1):                #isvalid checks validity of grid, ie playable or not.
            data1 = next_play(data1, choice(k)) #choice is random.choice func.
            m *= 1 if 2*m not in data else 2
            score+= m#data1.max()
    return score/times


def getAvailableMoves(np.ndarray data):
    data_list= [(c(data,i),i) for i in range(4)]
    ret = []
    cdef int move;
    for data1,move in data_list:
        if (data1==data).all():continue
        else:
            ret.append(move)
    return ret

def getMove(data, int times = 10):
    cdef float sc = float('-inf')
    mv = None
    cdef int move;
    cdef int score;
    for move in getAvailableMoves(data):
        score = 0
        score += rand_moves(data.copy(),move,times)
        if score > sc:
            sc= score
            mv = move
        elif score == sc:
            mv = choice([mv, move]) #randomly choose one of them
    return mv #if none, case handing occurs at caller side.

#if __name__ == '__main__':
def do():
    cdef np.ndarray data = np.asarray([[2,2,0,2],
                       [4,4,0,2],
                       [32,32,32,8],
                       [0,0,0,2]]) #a sample grid


    t1 = time.time()
    from sys import argv
    print(getMove(data, 100))#int(argv[1])))
    t_time = time.time() - t1
    print(t_time, 's')
    return t_time


