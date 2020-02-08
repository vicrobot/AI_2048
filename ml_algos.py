from functions import isvalid, score_G, getChildren, next_play

def minimax(data,depth, maximizing):
    if depth <= 0 or not isvalid(data): return score_G(data)
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data.copy(), True): #will run 4 times at max
            sc = max(sc, minimax(child, depth-1,True))
        return sc
    if not maximizing:
        sc = float('inf')
        for child, w in getChildren(data.copy(), False):
            sc = min(sc, minimax(child, depth-1,False))*w
        return sc

def minimaxab(data, alpha, beta,depth, maximizing):
    #funcs used: isvalid, score_G, getChildren
    """
    Opens all possibilities till given depth, returns score of evil computer trying to minimize score.
    Thus choose that move which gets highest score from this, expressing most secure move.
    It tries to minimize risk. Not maximizing score.
    """
    if depth <= 0 or not isvalid(data): return score_G(data)
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data, True): #will run 4 times at max
            sc = max(sc, minimaxab(child,alpha,beta, depth-1,False))
            if sc >= beta: return sc  #actually it is same as if alpha >= beta, 
                                        #maximizing player need not to care now #mamavsbhanja
            alpha = max(alpha, sc)
        return sc
    if not maximizing:
        sc = float('inf')
        for child,w in getChildren(data, False):
            sc = min(sc, minimaxab(child,alpha,beta, depth-1,True))
            if sc < alpha: return sc # minimizer need not to care
            beta = min(beta, sc)
        return sc

def expectimax(data,depth, maximizing):
    if depth <= 0 or not isvalid(data): return score_G(data)
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data, True): #will run 4 times at max
            sc = max(sc, expectimax(child,depth-1,False))
        return sc
    if not maximizing: #chance node 
        sc = 0
        t = getChildren(data, False)
        for child,w in t:
            sc += w*expectimax(child,depth-1,True)
        return sc/len(t)

def monte_carlo(data,move,plays_c=10):
    assert plays_c >0, 'Wrong value of plays_c'
    score = 0
    k = range(4)
    for j in range(plays_c):
        data1 = data.copy()
        data1 = next_play(data1, move)
        while isvalid(data1):
            data1 = next_play(data1, choice(k))
            score+= data1.max()
    return score/plays_c

