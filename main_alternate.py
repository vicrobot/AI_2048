import random
import numpy as np
from grid import isvalid
import key, strings
import time
import config
import pdb



# architecturing the 2048 game.

# in the indian style, say.

# digvadhu - nabh, dhara, vaam, agra (in the writing way).

# Three entities. One is board. One is visible player. One is the nature. (jag, aham, para)

# Player talks with the board, and so does the nature.


####
"""
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

This above is a snap from code review stack exchange; my post.
For each available moves, it runs 100 times the full board till non-valid. Takes about 3.25 sec. per move. Gives 80% win rate.
Since a board ends up at like 200 random moves, and since there are 4 available moves typically, and since 100 moves are run, so 80k karma is done per 3.2 sec at least. Current algo seems way powerful, doing 1lac per sec. Almost 4x powerful. 
But, but, but... This is without assuming overheads like score eval, alpha beta minimax etc calcs.
"""
###

def empty_trail_root(a,b,c,d):
    # supposing left to right growth happens.
    # supposing array has nonzeros, zeros sort from root to leaves.
    if d:
        return 4 # out of bound, indicating it doesn't make sense
    elif c:
        return 3
    elif b:
        return 2
    elif a:
        return 1
    else:
        return 0

newline = '\n'           

#########+==================

class Board:
    #Time taken for 1000000 moves: 16.4565s
    def __init__(self):
        # config_fetch
        self.grid_size = config.grid_size
        self.twos_chances = config.twos_chances
        
        #basic setup
        self.time_start = time.time()
        self.total_elements = self.grid_size**2
        self.grid = np.zeros((self.grid_size, self.grid_size),dtype=np.int64) # space use
        
        #initializing grid with 2 values
        init_point_1, init_point_2 = random.sample(range(self.total_elements),2)
        self.grid[init_point_1//self.grid_size][init_point_1%self.grid_size] = 2 if random.random() < self.twos_chances else 4
        self.grid[init_point_2//self.grid_size][init_point_2%self.grid_size] = 2 if random.random() < self.twos_chances else 4
    
        
    def vect_sum_left(self, a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        changed=0
        if a == 0:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d, changed # didn't change
                    else:
                        # case: d is non-zero
                        changed = 1
                        return d,0,0,0, changed # changed
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    changed = 1
                    a,b,c,d = c,d,0,0 # a is 0, c isn't, changed.
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    changed = 1
                    a,b,c,d = b,d,0,0 # changed
                else:
                    # b and c matter, d doesn't
                    changed = 1 #as b nonzero switched a
                    a,b,c,d = b,c,d,0
        else:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d,changed,  #didn't change
                    else:
                        # case: d is non-zero
                        changed = 1
                        a,b,c,d= a,d,0,0 #changed as b 0 was replaced with d non-zero
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    changed= 1
                    a,b,c,d = a,c,d,0 #changed
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    changed = 1 if d else 0
                    a,b,c,d = a,b,d,0
                else:
                    # b and c matter, d doesn't
                    #a,b,c,d = a,b,c,d
                    pass #didn't changed
        
        if b-a == 0:
            if d-c == 0: 
                return b+a,c+d,0,0 , changed if not b and not d else 1
            return b+a,c,d,0 , changed if not b else 1
        elif c-b == 0:
            return a, b+c, d, 0 , changed if not c else 1
        elif d-c == 0:
            return a,b,c+d,0 , changed if not d else 1
        else:
            return a,b,c,d , changed
            
            
    def vect_sum_right(self, a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        changed = 0  
        if d == 0:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d , changed #not changed
                    else:
                        # case: a is non-zero
                        changed = 1
                        return 0,0,0,a , changed
                else:
                    # case: b is non-zero, a doesn't matter
                    changed = 1
                    a,b,c,d = 0,0,a,b
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    changed = 1
                    a,b,c,d = 0,0,a,c
                else:
                    # case: c and b are non-zero
                    changed = 1
                    a,b,c,d = 0,a,b,c
        else:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d , changed
                    else:
                        # case: a is non-zero
                        changed = 1
                        a,b,c,d= 0,0,a,d
                else:
                    # case: b is non-zero, a doesn't matter
                    changed = 1 #since b nonzero took place of c zero
                    a,b,c,d = 0,a,b,d
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    changed = 1 if a else 0
                    a,b,c,d = 0,a,c,d
                else:
                    # case: c and b are non-zero
                    #a,b,c,d = a,b,c,d
                    pass #unchanged
        
        if d-c == 0:
            if a-b == 0:
                return 0,0,a+b,c+d , changed if not d and not a else 1
            return 0,a,b,c+d , changed if not d else 1
        elif c-b == 0:
            return 0,a,c+b,d  , changed if not c else 1
        elif b-a==0:
            return 0,a+b,c,d , changed if not b else 1
        else:
            return a,b,c,d , changed

   
    def vect_sum_left_simpler(self, a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        #changed=0
        if a == 0:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d #, changed # didn't change
                    else:
                        # case: d is non-zero
                        #changed = 1
                        return d,0,0,0 #, changed # changed
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    #changed = 1
                    a,b,c,d = c,d,0,0 # a is 0, c isn't, changed.
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    #changed = 1
                    a,b,c,d = b,d,0,0 # changed
                else:
                    # b and c matter, d doesn't
                    #changed = 1 #as b nonzero switched a
                    a,b,c,d = b,c,d,0
        else:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d #didn't change
                    else:
                        # case: d is non-zero
                        #changed = 1
                        a,b,c,d= a,d,0,0 #changed as b 0 was replaced with d non-zero
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    #changed= 1
                    a,b,c,d = a,c,d,0 #changed
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    #changed = 1 if d else 0
                    a,b,c,d = a,b,d,0
                else:
                    # b and c matter, d doesn't
                    #a,b,c,d = a,b,c,d
                    pass #didn't changed
        
        if b-a == 0:
            if d-c == 0: return b+a,c+d,0,0 #, changed if not b and not d else 1
            return b+a,c,d,0 #, changed if not b else 1
        elif c-b == 0:
            return a, b+c, d, 0 #, changed if not c else 1
        elif d-c == 0:
            return a,b,c+d,0 #, changed if not d else 1
        else:
            return a,b,c,d #, changed
            
            
    def vect_sum_right_simpler(self, a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        #changed = 0  
        if d == 0:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d #, changed #not changed
                    else:
                        # case: a is non-zero
                        #changed = 1
                        return 0,0,0,a #, changed
                else:
                    # case: b is non-zero, a doesn't matter
                    #changed = 1
                    a,b,c,d = 0,0,a,b
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    #changed = 1
                    a,b,c,d = 0,0,a,c
                else:
                    # case: c and b are non-zero
                    #changed = 1
                    a,b,c,d = 0,a,b,c
        else:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d #, changed
                    else:
                        # case: a is non-zero
                        #changed = 1
                        a,b,c,d= 0,0,a,d
                else:
                    # case: b is non-zero, a doesn't matter
                    #changed = 1 #since b nonzero took place of c zero
                    a,b,c,d = 0,a,b,d
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    #changed = 1 if a else 0
                    a,b,c,d = 0,a,c,d
                else:
                    # case: c and b are non-zero
                    #a,b,c,d = a,b,c,d
                    pass #unchanged
        
        if d-c == 0:
            if a-b == 0:
                return 0,0,a+b,c+d #, changed if not d and not a else 1
            return 0,a,b,c+d #, changed if not d else 1
        elif c-b == 0:
            return 0,a,c+b,d  #, changed if not c else 1
        elif b-a==0:
            return 0,a+b,c,d #, changed if not b else 1
        else:
            return a,b,c,d #, changed



    def mahimafalam(self, disha, inplace=True, grid_external=None, return_copy=False): #vidit, apekshit
        # nabh, dhara, vaam, agra # 0,1,2,3
        # currently only supporting the 4 edge size
        
        if grid_external is not None:
            grid = grid_external
        else:
            grid = self.grid

        if not inplace:
            grid = grid.copy() #preventing overwrite
        empty_idxs = []
        global_changed = 0
        if disha == 0:
            # nabh
            #grid = grid.T # for up/down, make T then left/right then T
            for col_num in range(4):
                #grid[row_num]=self.vect_sum_left(*grid[row_num])
                if not global_changed:
                    #*grid[:,col_num],changed=self.vect_sum_left(*grid[:,col_num])
                    #global_changed = global_changed or changed
                    a,b,c,d,changed=self.vect_sum_left(*grid[:,col_num])
                    #print(f'a,b,c,d are {a,b,c,d} and the input value before up shift were {grid[:,col_num]}')
                    grid[:,col_num]=a,b,c,d
                    global_changed = global_changed or changed
                    if d:
                        pass
                    elif c:
                        # d is 0
                        # math for columns work like:
                        # it will be like row cases, cuz its data loss as the element index in row cases is col num
                        # thus, say idx 9, so 9//4 is row num which is elem idx = 2, and 9%4 is col num ie 1
                        # thus col_num + elem_idx*4 will give flatten idx map
                        empty_idxs.append(col_num + 12)
                    elif b:
                        # d and c are 0
                        empty_idxs.append(col_num + 12)
                        empty_idxs.append(col_num + 8)
                    elif a:
                        # d=c=b = 0
                        empty_idxs.append(col_num + 12)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+4)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+12)
                    
                else:
                    a,b,c,d=self.vect_sum_left_simpler(*grid[:,col_num])
                    grid[:,col_num] = a,b,c,d
                    if d:
                        pass
                    elif c:
                        # d is 0
                        # math for columns work like:
                        # it will be like row cases, cuz its data loss as the element index in row cases is col num
                        # thus, say idx 9, so 9//4 is row num which is elem idx = 2, and 9%4 is col num ie 1
                        # thus col_num + elem_idx*4 will give flatten idx map
                        empty_idxs.append(col_num + 12)
                    elif b:
                        # d and c are 0
                        empty_idxs.append(col_num + 12)
                        empty_idxs.append(col_num + 8)
                    elif a:
                        # d=c=b = 0
                        empty_idxs.append(col_num + 12)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+4)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+12)
                    
            #grid = grid.T
        elif disha == 1:
            # dhara
            #grid = grid.T
            for col_num in range(4):
                #grid[row_num]=self.vect_sum_right(*grid[row_num])
                if not global_changed:
                    a,b,c,d,changed=self.vect_sum_right(*grid[:,col_num])
                    grid[:,col_num]=a,b,c,d
                    global_changed = global_changed or changed
                    if a:
                        pass
                    elif b:
                        # a is 0
                        # math for columns work like:
                        # it will be like row cases, cuz its data loss as the element index in row cases is col num
                        # thus, say idx 9, so 9//4 is row num which is elem idx = 2, and 9%4 is col num ie 1
                        # thus col_num + elem_idx*4 will give flatten idx map
                        empty_idxs.append(col_num) # col_num + 4*0 = col_num
                    elif c:
                        # a and b are 0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num + 4)
                    elif d:
                        # a=b=c = 0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+12)
                else:
                    a,b,c,d=self.vect_sum_right_simpler(*grid[:,col_num])
                    grid[:,col_num] = a,b,c,d
                    if a:
                        pass
                    elif b:
                        # a is 0
                        # math for columns work like:
                        # it will be like row cases, cuz its data loss as the element index in row cases is col num
                        # thus, say idx 9, so 9//4 is row num which is elem idx = 2, and 9%4 is col num ie 1
                        # thus col_num + elem_idx*4 will give flatten idx map
                        empty_idxs.append(col_num) # col_num + 4*0 = col_num
                    elif c:
                        # a and b are 0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num + 4)
                    elif d:
                        # a=b=c = 0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(col_num)
                        empty_idxs.append(col_num+4)
                        empty_idxs.append(col_num+8)
                        empty_idxs.append(col_num+12)
                    
            #grid = grid.T
        elif disha == 2:
            # vaam
            for row_num in range(4):
                x_4 = row_num*4
                #grid[row_num]=self.vect_sum_left(*grid[row_num])
                if not global_changed:
                    #*grid[row_num],changed=self.vect_sum_left(*grid[row_num])
                    #global_changed = global_changed or changed
                    a,b,c,d,changed=self.vect_sum_left(*grid[row_num])
                    global_changed = global_changed or changed
                    
                    if d:
                        pass
                    elif c:
                        # d is 0, others not. We're in hunt of empty places(not change detection),
                        # they surely occur in trails after shifting
                        # 0 to 15 numbers are x//4, x%4 as x,y example: 3: 3//4=0th row, 3%4=3 idx ie 4th elem
                        # example 2: 9//4 = 2, 9%4 = 1, therefore (2+1=3)rd row, 2nd elem
                        # to map backwards: (row_num)*4 + (elem idx )
                        # example, row_num=0, for d, the number is 0*4 + 3 = 3
                        empty_idxs.append(x_4 + 3)
                    elif b:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                    elif a:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                    else:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 0)
                    grid[row_num]=a,b,c,d
                    global_changed = global_changed or changed
                else:
                    a,b,c,d=self.vect_sum_left_simpler(*grid[row_num])
                    if d:
                        pass
                    elif c:
                        # d is 0, others not. We're in hunt of empty places(not change detection),
                        # they surely occur in trails after shifting
                        # 0 to 15 numbers are x//4, x%4 as x,y example: 3: 3//4=0th row, 3%4=3 idx ie 4th elem
                        # example 2: 9//4 = 2, 9%4 = 1, therefore (2+1=3)rd row, 2nd elem
                        # to map backwards: (row_num)*4 + (elem idx )
                        # example, row_num=0, for d, the number is 0*4 + 3 = 3
                        empty_idxs.append(x_4 + 3)
                    elif b:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                    elif a:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                    else:
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 0)
                    grid[row_num]=a,b,c,d
                    
        elif disha == 3:
            # agra
            for row_num in range(4):
                x_4 = row_num * 4
                #grid[row_num]=self.vect_sum_right(*grid[row_num])
                if not global_changed:
                    a,b,c,d,changed=self.vect_sum_right(*grid[row_num])
                    if a:
                        pass
                    elif b:
                        # a is 0
                        empty_idxs.append(x_4 + 0)
                    elif c:
                        # a and b are 0
                        empty_idxs.append(x_4 + 0)
                        empty_idxs.append(x_4 + 1)
                    elif d:
                        # a=b=c = 0
                        empty_idxs.append(x_4 + 0)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 2)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 0)
                    grid[row_num]=a,b,c,d
                    global_changed = global_changed or changed
                else:
                    a,b,c,d=self.vect_sum_right_simpler(*grid[row_num])
                    if a:
                        pass
                    elif b:
                        # a is 0
                        empty_idxs.append(x_4 + 0)
                    elif c:
                        # a and b are 0
                        empty_idxs.append(x_4 + 0)
                        empty_idxs.append(x_4 + 1)
                    elif d:
                        # a=b=c = 0
                        empty_idxs.append(x_4 + 0)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 2)
                    else:
                        # a=b=c=d=0
                        empty_idxs.append(x_4 + 3)
                        empty_idxs.append(x_4 + 2)
                        empty_idxs.append(x_4 + 1)
                        empty_idxs.append(x_4 + 0)
                    grid[row_num]=a,b,c,d
        else:
            print('wrong move') #can log also, or can ignore, or can raise exception if this is not user sided
        
        if return_copy or not inplace: return grid.copy(),global_changed,empty_idxs
        return global_changed,empty_idxs
    
    def animafalam(self,inplace=True,grid_external=None,return_copy=False,empty_idxs=None): #agyaat
        # 2 if rand() < 0.9 else 4 in random position.
        if grid_external is not None:
            grid = grid_external
        else:
            grid = self.grid

        if not inplace:
            grid = grid.copy() #preventing overwrite
        
        if empty_idxs is None:
            x,y = random.choice(np.argwhere(grid==0))
        else:
            try:
                idx = random.choice(empty_idxs)
            except:
                breakpoint()
            x,y = idx//4, idx%4
        random_val = 2 if random.random() < self.twos_chances else 4
        grid[x][y] = random_val
        
        if return_copy or not inplace: return grid.copy()
        
    def karmafalam(self, disha,inplace=True,grid_external=None):
    
        # use mahimafalam, then animafalam.
        # TODO: Maybe we can create a pre-filter, to decide if a grid can move a move or will stay same.
        #grid_unworked = self.grid.copy() if grid_external is None else grid_external
        #breakpoint()
        grid_mahimafalit,changed,empty_idxs = self.mahimafalam(disha,inplace=inplace,grid_external=grid_external,return_copy=True)
        #if np.array_equal(grid_unworked, grid_mahimafalit):
        if not changed:
            #no karma, no fal
            return grid_mahimafalit,changed
        else:
            self.animafalam(inplace=inplace,grid_external=grid_mahimafalit,empty_idxs=empty_idxs)
            if grid_external is None:
                self.grid = grid_mahimafalit # if inplace=True, then it's modified inplace so its grid_karmafalit
            return grid_mahimafalit,changed
    
    def karma(self, disha,inplace=True,grid_external=None):
        # if no grid given, obj's grid is worked upon.
        # inplace prevents the subject grid being overwritten
        return self.karmafalam(disha,inplace=inplace,grid_external=grid_external)
    
    
    def prettyprint(self, move, grid, count = 0):
        grid = np.where(grid == 0, '.', grid)
        first_row = True
        move_array = ["UP   ", "DOWN ", "LEFT ", "RIGHT"]
        print('\r' ' '*5)
        for row_vector in grid:
            if first_row:
                print(eval(config.initial_grid_string),eval(config.timestamp_string),'\n')
                first_row = 0
            else: print(eval(config.post_initial_grid_string),'\n')
        for i in range(2*len(grid) + 1):
            print("\033[F",end='', flush=True)

"""
class Test:
    def __init__(self,*args,**kwargs):pass
    
    def foo(vect):
        return vect ** 2
    
    sq = np.vectorize(foo)
    
    def var(self,grid):
        print(self.sq(grid))
    
Test().var(np.asarray([[1,2],[3,4]]))
exit()
"""

# the above board now holds a grid, can talk with player and his karmafal assigned by nature on the board.

def argv_parser():
    from sys import argv
    args = argv[1:]
    len_args = len(args)
    if not args:
        print(config.help_string)
        mode,AI_level = 1,0
    elif len_args == 1:
        if int(args[0]) != 1:
            print(config.default_ai_level_string)
            mode, AI_level = 0, 4
        else:
            mode, AI_level = 1, 0
    elif len_args >= 2 and int(args[0]) not in [1,0]:# or int(argv[2]) not in range(1,10):
        mode, AI_level = 1,0
        print(config.wrong_mode_args_string)
    else:
        try:
            mode, AI_level = int(args[0]), int(args[1])
        except IndexError:
            mode, AI_level = 1, 30
            print(config.wrong_mode_args_string)
    return mode, AI_level



def score(grid):
    maxv = grid.max()

def get_move(grid):
    #time.sleep(random.choice([0.3,0.4,0.5,0.6]))
    
    return random.choice(range(4))


if __name__ == '__main__':
    
    # mode 0: AI Autoplay, mode 1: human manual play
    mode, AI_level = argv_parser()
    if mode == 1:
        print('Manual Gameplay is On')
        print(config.instructions_string)
        
        #creating board instance
        board_instance = Board()
        #printing the initial grid()
        board_instance.prettyprint(0,board_instance.grid)
        move_map = dict(zip(range(4),['Up','Down','Left','Right']))
        keyobj = key.Key()
        steps_count = 0
        while isvalid(board_instance.grid):
            # initializing the key press listener
            keyobj.listen()
            move = keyobj.Keys.index(keyobj.key)
            
            if move == 4: break #esc key pressed. Breaking the loop.
            elif move > 4: continue # unexpected key, ignoring.
            if steps_count == 0:
                board_instance.time_start=time.time()
            board_instance.karma(move)
            with open('boardlog.txt','a+') as boardlog:
                boardlog.write(move_map[move])
                boardlog.write(newline)
                boardlog.write(board_instance.grid.__str__())
                boardlog.write(newline*4)
                
            board_instance.prettyprint(move,board_instance.grid)
            steps_count += 1
        print('\n'*10)
        score = board_instance.grid.max() # TODO: temporary right now. WIll need board evaluation.
        final_T = time.time() - board_instance.time_start
        print(f"Steps: {steps_count:>4}, Score: {score:>2},",'Time: {:>6.6}s,'.format(final_T),end = '')
        print(f" Average Steps/s: {steps_count/final_T:5.4}")
        if score >= 2048:
            print(strings.win_string)
    else:
        print(f'AI Gameplay is On, level: {AI_level}')
        #creating board instance
        board_instance = Board()
        #printing the initial grid()
        board_instance.prettyprint(0,board_instance.grid)
        
        steps_count = 0
        while isvalid(board_instance.grid):
        
            move = get_move(board_instance.grid)
            
            if steps_count == 0:
                board_instance.time_start=time.time()
            board_instance.karma(move)
            board_instance.prettyprint(move,board_instance.grid)
            steps_count += 1
        print('\n'*10)
        score = board_instance.grid.max() # TODO: temporary right now. WIll need board evaluation.
        final_T = time.time() - board_instance.time_start
        print(f"Steps: {steps_count:>4}, Score: {score:>2},",'Time: {:>6.6}s,'.format(final_T),end = '')
        print(f" Average Steps/s: {steps_count/final_T:5.4}")
        if score >= 2048:
            print(strings.apocalypse_string)






#####

"""
Bugs

"""

#####
























