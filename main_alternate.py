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



class Board:
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
    
    
    def vect_sum_left(self,a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        if a == 0:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d
                    else:
                        # case: d is non-zero
                        return d,0,0,0
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    a,b,c,d = c,d,0,0
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    a,b,c,d = b,d,0,0
                else:
                    # b and c matter, d doesn't
                    a,b,c,d = b,c,d,0
        else:
            if b == 0:
                if c == 0:
                    if d == 0:
                        return a,b,c,d
                    else:
                        # case: d is non-zero
                        a,b,c,d= a,d,0,0
                else:
                    # case: c is non-zero, doesn't matter d is or not
                    a,b,c,d = a,c,d,0
            else:
                # case: b is non-zero
                if c == 0:
                    # case: b is non-zero and c is zero, d doesn't matter as below is to be returned
                    a,b,c,d = a,b,d,0
                else:
                    # b and c matter, d doesn't
                    #a,b,c,d = a,b,c,d
                    pass
        
        if b-a == 0:
            if d-c == 0: return b+a,c+d,0,0
            return b+a,c,d,0
        elif c-b == 0:
            return a, b+c, d, 0
        elif d-c == 0:
            return a,b,c+d,0
        else:
            return a,b,c,d

    def vect_sum_right(self, a,b,c,d):
        # 2048 alike left slide
        # currently for 4 grid edge
        if d == 0:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d
                    else:
                        # case: a is non-zero
                        return 0,0,0,a
                else:
                    # case: b is non-zero, a doesn't matter
                    a,b,c,d = 0,0,a,b
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    a,b,c,d = 0,0,a,c
                else:
                    # case: c and b are non-zero
                    a,b,c,d = 0,a,b,c
        else:
            if c == 0:
                if b == 0:
                    if a == 0:
                        return a,b,c,d
                    else:
                        # case: a is non-zero
                        a,b,c,d= 0,0,a,d
                else:
                    # case: b is non-zero, a doesn't matter
                    a,b,c,d = 0,a,b,d
            else:
                if b == 0:
                    # case: c is non-zero, b is zero
                    a,b,c,d = 0,a,c,d
                else:
                    # case: c and b are non-zero
                    #a,b,c,d = a,b,c,d
                    pass
        
        if d-c == 0:
            if a-b == 0:
                return 0,0,a+b,c+d
            return 0,a,b,c+d
        elif c-b == 0:
            return 0,a,c+b,d
        elif b-a==0:
            return 0,a+b,c,d
        else:
            return a,b,c,d

    
    def mahimafalam(self, disha, inplace=True, grid_external=None, return_copy=False): #vidit, apekshit
        # nabh, dhara, vaam, agra # 0,1,2,3
        # currently only supporting the 4 edge size
        
        if grid_external is not None:
            grid = grid_external
        else:
            grid = self.grid

        if not inplace:
            grid = grid.copy() #preventing overwrite
        
        # TODO: one heavy operation right now is transposing 2 times per up or down.
        if disha == 0:
            #breakpoint()
            grid = grid.T # for up/down, make T then left/right then T
            for row_num in range(4):
                grid[row_num]=self.vect_sum_left(*grid[row_num])
            grid = grid.T
        elif disha == 1:
            grid = grid.T
            for row_num in range(4):
                grid[row_num]=self.vect_sum_right(*grid[row_num])
            grid = grid.T
        elif disha == 2:
            for row_num in range(4):
                grid[row_num]=self.vect_sum_left(*grid[row_num])
            
        elif disha == 3:
            for row_num in range(4):
                grid[row_num]=self.vect_sum_right(*grid[row_num])
        else:
            print('wrong move') #can log also, or can ignore, or can raise exception if this is not user sided
        
        if return_copy or not inplace: return grid.copy()
    
    def animafalam(self,inplace=True,grid_external=None,return_copy=False): #agyaat
        # 2 if rand() < 0.9 else 4 in random position.
        if grid_external is not None:
            grid = grid_external
        else:
            grid = self.grid

        if not inplace:
            grid = grid.copy() #preventing overwrite
        
        x,y = random.choice(np.argwhere(grid==0))
        random_val = 2 if random.random() < self.twos_chances else 4
        grid[x][y] = random_val
        
        if return_copy or not inplace: return grid.copy()
        
    def karmafalam(self, disha,inplace=True,grid_external=None):
    
        # use mahimafalam, then animafalam.
        # TODO: Maybe we can create a pre-filter, to decide if a grid can move a move or will stay same.
        
        grid_unworked = self.grid.copy() if grid_external is None else grid_external
        grid_mahimafalit = self.mahimafalam(disha,inplace=inplace,grid_external=grid_external,return_copy=True)
        if np.array_equal(grid_unworked, grid_mahimafalit):
            #no karma, no fal
            return grid_unworked
        else:
            grid_karmafalit = self.animafalam(inplace=inplace,grid_external=grid_mahimafalit)
            return grid_karmafalit
    
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


# the above board now holds a grid, can talk with player and his karmafal assigned by nature on the board.

def argv_parser():
    from sys import argv
    argv = argv[1:]
    len_argv = len(argv)
    if not argv:
        print(config.help_string)
        mode,AI_level = 1,0
    elif len_argv == 1:
        if int(argv[1]) != 1:
            print(config.default_ai_level_string)
            mode, AI_level = 0, 4
        else:
            mode, AI_level = 1, 0
    elif len_argv >= 2 and int(argv[1]) not in [1,0]:# or int(argv[2]) not in range(1,10):
        mode, AI_level = 1,0
        print(config.wrong_mode_args_string)
    else:
        mode, AI_level = int(argv[1]), int(argv[2])
    return mode, AI_level


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
            board_instance.prettyprint(move,board_instance.grid)
            steps_count += 1
        print('\n'*10)
        score = board_instance.grid.max() # TODO: temporary right now. WIll need board evaluation.
        final_T = time.time() - board_instance.time_s
        print(f"Steps: {steps_count:>4}, Score: {score:>2},",'Time: {:>6.6}s,'.format(final_T),end = '')
        print(f" Average Steps/s: {steps_count/final_T:5.4}")
        if score >= 2048:
            print(strings.win_string)
    else:
        print(f'AI Gameplay is On, level: {AI_level}')






#####

"""
Bugs.

Well that tells how mathematically incomplete logic i've written.
Here some of the bugs I see:

1. Up up and up, the grid do animafal even if no karma was done
2. For some reason, up wasn't working. Yes, the first column had first elem as 8, then 0 then 2 then ... and it stayed like that. I got it now.


"""

#####
























