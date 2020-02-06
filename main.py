import random
import numpy as np
from sys import argv
from functions import c,isvalid, fillnums, next_play, minimaxab, getMove, getChildren, score_G
import key, strings
import time

gen = lambda: random.choice([2]*9+[4]*1)

class twnty48:
    def __init__(self, l1):
        self.l1 = l1
        self._l1 = l1 #safe l1
        self.moves = list(range(4))
    time_s= 0
        
    @classmethod
    def prettyprint(cls, move, l1, count = 0):
        l1 = np.where(l1 == 0, '.', l1) 
        init= 1
        m = ["UP   ", "DOWN ", "LEFT ", "RIGHT"]
        print('\r' ' '*5) #extra print needed due to key detection.
        for i in l1:
            if init:
                print(eval(strings.s7),eval(strings.s9),'\n') ; init = 0
            else: print(eval(strings.s8),'\n')
        for i in range(2*len(l1) + 1): print("\033[F",end='', flush=True)
    
    def run(self, plays_c, mode = 0,show = True):
        count = 1
        history_c = [np.asarray([0])]*(10 if show else 5)
        tempranmove = False
        move = 0
        if mode==1: Keyobj = key.Key()
        twnty48.time_s = time.time()#self.time_s = time.time() was updating time of obj's attribute.
        while isvalid(self.l1):
            if mode == 1:
                Keyobj.listen()
                move = Keyobj.Keys.index(Keyobj.key)
                if move not in self.moves:break
            else:
                if not tempranmove:
                    move = getMove(data = self.l1.copy(), plays_c = plays_c) 
                else:
                    if (self.l1[-1] == [0]*4).all(): move = random.choice(self.moves) 
                    #intense need of down move, prob=.25
                    else:move = random.choice([0,2,0,0,2,3,3,0,2]); tempranmove= False 
                    # when game stuck, down move prob = 0.
                    
                history_c=history_c[1:] + [self.l1.copy()]
                if all([(i==j).all() for i in history_c for j in history_c]): tempranmove = True
                
            self.l1 = next_play(self.l1.copy(), move)
            if not show: continue
            self.prettyprint(move, self.l1.reshape(4,4), count = count)
            count += 1
        score = self.l1.max()
        if not show:
            return count, score, time.time() - twnty48.time_s
        print('\n'*(2*len(l1)))
        final_T = time.time() - twnty48.time_s
        print(f"Steps: {count:>4}, Score: {score:>2},",'Time: {:>6.6}s,'.format(final_T),end = '')
        print(f" Average Steps/s: {count/final_T:5.4}")
        if score >= 2048:
            if mode==1:print(strings.s6)
            else: print(strings.s5)

if __name__ == '__main__':
    # mode 0: AI Autoplay, mode 1: human manual play
    if len(argv[1:]) == 0:
        print(strings.s1)
        mode,AI_level = 1,0
    elif len(argv[1:]) == 1:
        if int(argv[1]) != 1:
            print(strings.s2)
            mode, AI_level = 0, 4
        else: mode, AI_level = 1, 0
    elif len(argv[1:]) >= 2 and int(argv[1]) not in [1,0] or int(argv[2]) not in range(1,10):
        mode, AI_level = 1,0
        print(strings.s3)
    else: mode, AI_level = int(argv[1]), int(argv[2])
    
    if mode: print(strings.s4)
    l1 = np.asarray([0 for i in range(16)])
    l1 = fillnums(fillnums(l1)).reshape(4,4)
    f = twnty48(l1)
    if mode: f.prettyprint(0, l1)
    f.run(AI_level, mode = mode)





