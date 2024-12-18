from unittest.mock import patch
from unittest import TestCase
import unittest
import numpy as np
import time
import random

from main_alternate import Board,getChildren

newline='\n'


class MainAlternateTestCases(TestCase):
    
    #@patch()
    def test_karmafalam(self,*args):
        return
        board_instance = Board()
        core_grid = np.asarray([[2,2,0,0],[4,4,0,0],[4,2,4,2],[0,0,0,0]])
        
        def scene_runner(scene_number,move_code,core_grid,inplace=False):
            move_map = dict(zip(range(4),['Up','Down','Left','Right']))
            print(f'Scenario: {scene_number}')
            print(f'{move_map[move_code]} movement:')
            print(f'Inplace={repr(inplace)}')
            print(newline)
            grid_scene = core_grid.copy()
            grid_karmafalit = board_instance.karma(
                                                    move_code, grid_external=grid_scene,inplace=inplace) #vaam
            print('Grid input:', grid_scene, 'Grid output', grid_karmafalit, sep = '\n'*2)
            print('-'*20)
        
        # scene 1: left, no inplace
        scene_runner(1,2,core_grid,inplace=False)
        
        #scene 2: left, inplace
        scene_runner(2,2,core_grid,inplace=True)
        
        #scene 3: right, no inplace
        scene_runner(3,3,core_grid,inplace=False)
        
        #scene 4: right, inplace
        scene_runner(4,3,core_grid,inplace=True)
        
        #"""
        init_time = time.time()
        K = 1_000_000
        grid_scene=core_grid.copy()
        for i in range(K):
            #grid_mahimafalam=board_instance.mahimafalam(
            #random.choice(range(4)),inplace=False,grid_external=grid_scene,return_copy=True
            #)
            grid_karmafalam,changed = board_instance.karma(
                            random.choice(range(4)), inplace=False,grid_external=grid_scene)
        exit_time = time.time()
        
        print(f'Time taken for {K} moves: {exit_time-init_time:>.6}s')
        print(newline * 2)
        #"""
        
        #board minimum changed (which is now the king, the normal Board)
        #mahimafalam: Time taken for 100000 moves: 1.16121s
        #karma: Time taken for 100000 moves: 2.83758s
        
        #board minimum changed but not hybrid, ie only using changed shifter and not simpler shifters
        #karma: Time taken for 100000 moves: 2.84753s
        # makes sense.
        # The simpler operations are simpler with 3 tasks, 1. changed = 0, 2. changed = 1 for some cases,
        # 3. in some returns, ternary operator that changed if ... else 1 or 0 But those are too basic, so can ignore Specially considering those if else. But surely hybrid is better, even if very less margin.
        # for this, range I saw for few runs is 2.76 to 2.88 sec per lakh runs. For hybrid, 2.83 is highest
                
        ###################################################################                
        # TODO: Very special note. The 'cause' of making simpler versions in parallel is so remarkable.
        # TODO: The cause is: functions can't switch behavior AND give speed along the way two functions can do it.
        # TODO: The above is like using the meta language hack to speedup the language
        # TODO: So basically you're using C indirectly more efficiently than the interface the language provides you.
        ##################################################################
        
        
        # board no changed (depending on numpy equals to check)
        #mahimafalam: Time taken for 100000 moves: 1.10926s
        #karma: Time taken for 100000 moves: 3.41448s
        
    
    def test_vect_sum(self,*args):
        #left and right both
        return
        board_instance = Board()
        core_grid = np.asarray([[2,2,0,0],[4,4,0,0],[4,2,4,2],[0,0,0,0]])
        
        
        arr = [[2,2,0,0],
                [2,4,2,4],
                [0,0,0,0],
                [0,0,2,0],
                [0,2,0,2],
                [0,0,0,2],
                [2,0,0,0],
                [2,2,2,4]]
        
        for vect in arr:
            row = [0,0,0,0]
            *row,changed= board_instance.vect_sum_left(*vect)
            print(f'Vect {vect} summed left as {row} and vect is {"not " if not changed else ""}changed')

        print(newline)
        for vect in arr:
            row = [0,0,0,0]
            *row, changed= board_instance.vect_sum_right(*vect)
            print(f'Vect {vect} summed right as {row} and vect is {"not " if not changed else ""}changed')

        print('-'*20)
    
    def test_getChildren(self,*args):
        board_instance = Board()
        for i in range(10):
            board_instance.karma(random.choice(range(4)))
        
        print(f'Initial Grid\n{board_instance.grid}')
        human_children = getChildren(board_instance.grid,human=True)
        
        print(f'Printing human chilren')
        for child in human_children:
            print(child)
            print(newline*2)
        print(f'Printing nature children')
        nature_children = getChildren(board_instance.grid,human=False)
        for child in nature_children:
            print(child)
            print(newline*2)
        


if __name__ == '__main__':
    unittest.main()

#metaobs: unittest module although is same as normal test run, but it can smoothly support build up
# this tells, any specialized software is just to reduce maya, as things gets hard for us to grow outward
