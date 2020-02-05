from functions import isvalid, score_G, getChildren

def minimax(data,depth, maximizing):
    if depth <= 0 or not isvalid(data): return score_G(
                                                    np.where(data.copy() == None, 0, data.copy()).flatten())
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

def minimaxab( data, alpha, beta,depth, maximizing):
    """
    Opens all possibilities till given depth, returns score of evil computer trying to minimize score.
    Thus choose that move which gets highest score from this, expressing most secure move.
    It tries to minimize risk. Not maximizing score.
    """
    if depth <= 0 or not isvalid(data): return score_G(
                                                    np.where(data == None, 0, data.copy()))
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
        for child, w in getChildren(data.copy(), False):
            sc = min(sc, minimaxab(child,alpha,beta, depth-1,True))
            if sc < alpha: return sc # minimizer need not to care
            beta = min(beta, sc)
        return sc

