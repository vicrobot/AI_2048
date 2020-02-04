import random
import numpy as np
import sys

gen = lambda: random.choice([2]*9+[4]*1)
scoregrid = np.asarray([     [4**15,4**14,4**13,4**12],
                             [4**8,4**9,4**10,4**11],
                             [4**7,4**6,4**5,4**4],
                             [4**0,4**1,4**2,4**3]])
def left(l1):
    #assumption: l1 is 4 x 4 matrix
    l = l1.copy()
    for j in range(4):
        res = []
        merged = False
        for i in l[j]:
            if i==0:continue
            if res and i == res[-1] and not merged:
                res[-1] += i
                merged = True #this merged will be broken up only when next i!= res[-1] occurs.
            else:
                if res and res[-1]!= 0: merged = False  # here will come only when i!= res[-1]
                res.append(i)
        for i in range(4 - len(res)): res.append(0)
        l[j] = res
    return l
#v.T[:,::-1]  #clockwise
#v[:,::-1].T  #anticlockwise
#v[:,::-1]    #mirrored

def c(l1, move):
    #assumption: l1 is 4 x 4 matrix
    if move == 2: return left(l1)
    if move == 0: return left(l1[:,::-1].T).T[:,::-1] #anti, left, clock
    if move == 1: return left(l1.T[:,::-1])[:,::-1].T #clock, left, anti
    if move == 3: return left(l1[:,::-1])[:,::-1]# mirrored, left, mirrored


def fillnums(l1, flat = 1):
    if 0 not in l1: return l1
    if flat != 1:
        return fillnums(l1.flatten()).reshape(l1.shape)
    l1[random.choice(np.arange(16)[l1==0])] = gen()
    return l1

def isvalid(l1):
    #assume l1 is 4 x 4 and there's no none in it.
    if 0 in l1: return True
    l = []
    for move in range(4):
        b = (l1 == c(l1,move)).all()
        if not b: return True
        l.append(b)
    if all(l): return False

def getChildren(data,playerT):
    if playerT:
        l = []
        for move in range(4):
            #if (c(data.copy(), move) == data).all(): continue
            l.append(c(data.copy(), move))
    else:
        if 0 not in data: return [(data, 1)]
        indices = (np.arange(16).reshape(4,4)[data == 0]).flatten()
        l = []
        for idx in indices:
            data1 = data.copy()
            data1[idx//4][idx - 4*(idx//4)] = 2
            l.append((data1,0.9))
            data1 = data.copy()
            data1[idx//4][idx - 4*(idx//4)] = 4
            l.append((data1,0.1))
    return l
def score_G(data):
    #heuristics
    grid = scoregrid
    score = (grid * data).sum()
    a1 = -score/8 if (data == 0).sum() < 3 else score/16 #free tile reward
    a2 = score if data[0][0]>=data[1][0]>=data[2][0] else 0  #monotonicity1 reward
    a3 = score if data[0][0]>=data[0][1]>=data[0][2]>=data[0][3] else 0  #monotonicity2 reward
    
    return score + a1+ a2+ a3
def next_play(l1, move):
    #assumption: l1 is 4 x 4 matrix
    first = c(l1, move)
    k = (first == l1).all()
    if 0 in first:
        if k: return l1
        else: return fillnums(first, flat = 0)
    if not k: return (fillnums(first, flat = 0)) if valid else l1
    else: return first if valid else l1

def minimaxab(data, alpha, beta,depth, maximizing):
    if depth <= 0 or not isvalid(data): return score_G(data.copy())
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data.copy(), True): #will run 4 times at max
            sc = max(sc, minimaxab(child,alpha,beta, depth-1,False))
            if sc >= beta: return sc  #actually it is same as if alpha >= beta, 
                                        #maximizing player need not to care now
            alpha = max(alpha, sc)
        return sc
    if not maximizing:
        sc = float('inf')
        for child,w in getChildren(data.copy(), False):
            sc = min(sc, minimaxab(child,alpha,beta, depth-1,True))
            if sc < alpha: return sc # minimizer need not to care
            beta = min(beta, sc)
        return sc

def getMove(data, plays_c=2):
    sc, mv = float('-inf'), 5
    for  move in range(4):
        moved = c(data.copy(), move)
        if ( moved == data).all(): continue
        score = 0
        #score += Minimaxab.calculate(moved.copy().flatten().tolist(),plays_c, -np.inf, np.inf, False)
        score += minimaxab(moved.copy(), -np.inf, np.inf, plays_c, False)    #---->Not Working as expected
        if move == 0 or move == 2: score+= 10000
        t_sc = score#sum(scores)/len(scores)#score
        if t_sc > sc:
            sc= t_sc
            mv = move
        elif t_sc == sc:
            mv = random.choice([mv, move])
    return mv

    


