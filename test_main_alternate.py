from unittest.mock import patch
from unittest import TestCase
import unittest
import numpy as np

from main_alternate import Board


class MainAlternateTestCases(TestCase):
    
    #@patch()
    def test_karmafalam(self,*args):
        board_instance = Board()
        core_grid = np.asarray([[2,2,0,0],[4,4,0,0],[4,2,4,2],[0,0,0,0]])
        
        print('scenario 1: no inplace, defaults to True')
        grid_scene_1 = core_grid.copy()
        grid_mahimafalit = board_instance.mahimafalam(2, grid_external=grid_scene_1,return_copy=True) #vaam
        print(grid_scene_1, grid_mahimafalit, sep = '\n'*2)
        
        print('scenario 2: inplace = False')
        grid_scene_2 = core_grid.copy()
        grid_mahimafalit = board_instance.mahimafalam(
                            2, inplace=False,grid_external=grid_scene_2,return_copy=True) #vaam
        print(grid_scene_2, grid_mahimafalit, sep = '\n'*2)
       


if __name__ == '__main__':
    unittest.main()

#metaobs: unittest module although is same as normal test run, but it can smoothly support build up
# this tells, any specialized software is just to reduce maya, as things gets hard for us to grow outward
