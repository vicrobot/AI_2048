#distutils: language = c++
from libcpp.vector cimport vector

cdef extern from "vect.h":
    cppclass myvec:
        myvec() except +
        vector[vector[int]] up(vector[vector[int]] vect)
        vector[vector[int]] down(vector[vector[int]] vect)
        vector[vector[int]] left(vector[vector[int]] vect)
        vector[vector[int]] right(vector[vector[int]] vect)
        vector[int] l(vector[int])
        vector[int] r(vector[int])
        vector[vector[int]] c(vector[vector[int]] vect, int move)
        int isvalid(vector[vector[int]] vect)
        int random(int, int)
        vector[vector[int]] fillnum_m(vector[vector[int]] vect)
        int maxim(vector[vector[int]] vect)
        int hasMoved(vector[vector[int]] v1, vector[vector[int]] v2)
        vector[vector[int]] next_play(vector[vector[int]] vect, int)
        double rand_moves(vector[vector[int]] vect, int first_move, int times)
        

cdef myvec vect = myvec()

from random import choice, random
import numpy as np
cimport numpy as np
cimport numpy as cnp
import time
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def c(np.ndarray grid, int move):
    if move not in range(4): return
    return np.asarray(vect.c(grid, move))
    
@cython.boundscheck(False)
@cython.wraparound(False)
def isvalid(np.ndarray l):#l is grid
    return bool(vect.isvalid(l))

cdef np.ndarray ind = np.arange(16).reshape(4,4)

@cython.boundscheck(False)
@cython.wraparound(False)
def next_play(np.ndarray grid, int move):
    return np.asarray(vect.next_play(grid, move))

@cython.boundscheck(False)
def fillnums(np.ndarray grid):
    return np.asarray(vect.fillnum_m(grid))

@cython.boundscheck(False)
def rand_moves(np.ndarray data,int first_move,int times): #data is playing grid, numpy matrix 4 x 4
    assert times > 0
    return np.asarray(vect.rand_moves(data,first_move, times))

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
    cdef double score;
    for move in getAvailableMoves(data):
        score = 0
        score += vect.rand_moves(data,move,times)
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


