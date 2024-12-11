from unittest.mock import patch
from unittest import TestCase
import unittest
import numpy as np
import time
import random

from main_alternate import Board

newline='\n'


class MainAlternateTestCases(TestCase):
    
    #@patch()
    def test_karmafalam(self,*args):
        board_instance = Board()
        core_grid = np.asarray([[2,2,0,0],[4,4,0,0],[4,2,4,2],[0,0,0,0]])
        
        def scene_runner(scene_number,move_code,core_grid,inplace=False):
            move_map = dict(zip(range(4),['Up','Down','Left','Right']))
            print(f'Scenario: {scene_number}')
            print(f'{move_map[move_code]} movement:')
            print(f'Inplace={repr(inplace)}')
            print(newline)
            grid_scene = core_grid.copy()
            grid_mahimafalit,changed = board_instance.mahimafalam(move_code, grid_external=grid_scene,inplace=inplace,return_copy=True) #vaam
            print('Grid input:', grid_scene, 'Grid output', grid_mahimafalit, sep = '\n'*2)
            print('-'*20)
        
        # scene 1: left, no inplace
        scene_runner(1,2,core_grid,inplace=False)
        
        #scene 2: left, inplace
        scene_runner(2,2,core_grid,inplace=True)
        
        #scene 3: right, no inplace
        scene_runner(3,3,core_grid,inplace=False)
        
        #scene 4: right, inplace
        scene_runner(4,3,core_grid,inplace=True)
        
        
        init_time = time.time()
        K = 1_000_000
        grid_scene=core_grid.copy()
        for i in range(K):
            grid_mahimafalit,changed = board_instance.mahimafalam(
                            random.choice(range(4)), inplace=False,grid_external=grid_scene,return_copy=True)
        exit_time = time.time()
        
        print(f'Time taken for {K} moves: {exit_time-init_time:>.6}s')
        print(newline * 2)
        
    
    def test_vect_sum(self,*args):
        #left and right both
    
        board_instance = Board()
        core_grid = np.asarray([[2,2,0,0],[4,4,0,0],[4,2,4,2],[0,0,0,0]])
        
        
        arr = [[2,2,0,0],
                [2,4,2,4],
                [0,0,0,0],
                [0,0,2,0],
                [0,2,0,2],
                [0,0,0,2],
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



if __name__ == '__main__':
    unittest.main()

#metaobs: unittest module although is same as normal test run, but it can smoothly support build up
# this tells, any specialized software is just to reduce maya, as things gets hard for us to grow outward
