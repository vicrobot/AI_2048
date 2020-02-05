import random
import numpy as np

gen = lambda: random.choice([2]*9+[4]*1)
scoregrid = np.asarray([     [4**15,4**14,4**13,4**12],
                             [4**8,4**9,4**10,4**11],
                             [4**7,4**6,4**5,4**4],
                             [4**0,4**1,4**2,4**3]])
def left(l1):
    #assumption: l1 is 4 x 4 numpy matrix
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
    #assumption: l1 is 4 x 4 numpy matrix
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
    #assume l1 is 4 x 4
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
    """
    Upgrades needed:
    1. Smootheness measure.
    2. It is hard coded for top-left. Needs to be automatically decide for any corner.
    """
    grid = scoregrid
    score = (grid * data).sum()
    """
    Not going in score's dimension is recommended.
    
    With below heuristic and 4th level AI: 2048: 50%+
    
    div = 100
    #a1 = -score/div if (data == 0).sum() < 3 else score/10 #free tiles
    a1 = score/(div*(16-(data == 0).sum()))
    a2 = score/div if data[0][0]>=data[1][0]>=data[2][0] else 0  #monoton1
    a3 = score/div if data[0][0]>=data[0][1]>=data[0][2]>=data[0][3] else -score/50 #monoton2
    a4 = score/div if data[0][3] >= data[1][3] else -score/20
    a5 = score/div if data.max() == data[0][0] else -score
    a6 = score/div if data[0][1] >= data[1][1] and data[0][2] >= data[1][2] else -score/2
    a7 = score/div if data[1][3] >= data[1][2] else -score/20
    -----------------------------------------------------------------------
    
    """
    div = 300
    #a1 = -score/div if (data == 0).sum() < 3 else score/10 #free tiles
    a1 = score/(div*(16-(data == 0).sum()))
    a2 = score/div if data[0][0]>=data[1][0]>=data[2][0] else 0  #left vert.1 monotone
    a3 = score/div if data[0][0]>=data[0][1]>=data[0][2]>=data[0][3] else -score/50 #top horz. monotone.
    a4 = score/div if data[0][3] >= data[1][3] and data[1][3] >= data[1][2] else -score/50 #1to2 rightop corner monotone
    a5 = score/div if data.max() == data[0][0] else -2*score #max at top left.
    a6 = score/div if data[0][1] >= data[1][1] >= data[2][1] else -score/2 #vert 2 mono
    a7 = score/div if data[0][2] >= data[1][2] >= data[2][2] else -score/20  #vert 3 mono
    a8 = score/div if data[2][2] <= data[1][2] else -score/20
    
    return score + a1+ a2+ a3 + a4 + a5 + a6 + a7 + a8

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
                                        #maximizing player need not to care now #mamavsbhanja
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
        score += minimaxab(moved.copy(), -np.inf, np.inf, plays_c, False)
        if move == 0 or move == 2: score+= 10000 #motivation on up or left.
        t_sc = score
        if t_sc > sc:
            sc= t_sc
            mv = move
        elif t_sc == sc:
            if mv in [0,2]: continue
            mv = random.choice([mv, move])
    return mv

    


