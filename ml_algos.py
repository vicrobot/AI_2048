from functions import isvalid, score_G, getChildren

def minimax(data,depth, maximizing):
    """
    firstly we'll get all child of grid, by maximizing, ie playing by 4 moves,
    then will get all child on each child by playing all swaps, you can for now take it as 2.
    and so on till given depth, then we will evaluate scores, then will return move with highest score at final.
    How is it working?:-
    
    I evaluated minimax for 4 grids, the child of main grid.
    minimax will give scores for 4 grids and grid with max score will make its corresp. move to win.
    In minimax, each grid when enters, do this:
                grid
    childs by 4 moves
    each having child of 2 placed one all nones one by one
    so on till given depth
    Now minimax algo is applied and evaluated the score.
    """
    if depth <= 0 or not isvalid(data): return score_G(
                                                    np.where(data.copy() == None, 0, data.copy()).flatten())
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data.copy(), True): #will run 4 times at max
            sc = max(sc, minimax(data.copy(), depth-1,True))
        return sc
    if not maximizing:
        sc = float('inf')
        for child, w in getChildren(data.copy(), False):
            sc = min(sc, minimax(data.copy(), depth-1,False))*w
        return sc

def minimaxab( data, alpha, beta,depth, maximizing):
    """
    firstly we'll get all child of grid, by maximizing, ie playing by 4 moves,
    then will get all child on each child by playing all swaps, you can for now take it as 2.
    and so on till given depth, then we will evaluate scores, then will return move with highest score at final.
    How is it working?:-
    
    I evaluated minimax for 4 grids, the child of main grid.
    minimax will give scores for 4 grids and grid with max score will make its corresp. move to win.
    In minimax, each grid when enters, do this:
                grid
    childs by 4 moves
    each having child of 2 placed one all nones one by one
    so on till given depth
    Now minimax algo is applied and evaluated the score.
    When we run it for non maximizing, we take grid having maximum score since minimizing player failed for that
    grid to minimize, or say minimizing player could do lowest loss on it.
    """
    if depth <= 0 or not isvalid(data): return score_G(
                                                    np.where(data == None, 0, data.copy()))
    if maximizing:
        sc = float('-inf')
        for child in getChildren(data.copy(), True): #will run 4 times at max
            sc = max(sc, minimaxab(data.copy(),alpha,beta, depth-1,False))
            if sc >= beta: return sc  #actually it is same as if alpha >= beta, 
                                        #maximizing player need not to care now
            alpha = max(alpha, sc)
        return sc
    if not maximizing:
        sc = float('inf')
        for child, w in getChildren(data.copy(), False):
            sc = min(sc, minimaxab(data.copy(),alpha,beta, depth-1,True))
            if sc < alpha: return sc # minimizer need not to care
            beta = min(beta, sc)
        return sc

