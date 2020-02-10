def left(grid):
    #assumption: grid is 4 x 4 numpy matrix
    l = grid.copy()
    res = []
    merged = False
    for i in range(4):
        t = l[-i-1]
        if t==0:continue
        if res and t == res[-1] and not merged:
            res[-1] += t
            merged = True
        else:
            if res: merged = False
            res.append(t)
    for i in range(4 - len(res)): res=[0]+res
    l = res[::-1]
    return l

def right(grid):
    l = grid.copy()
    res = []
    merged = False
    for i in range(4):
        t = l[i]
        if t == 0: continue
        if res and t == res[-1] and not merged:
            res[-1]+=t
            merged = True
        else:
            if res: merged = False
            res.append(t)
    for i in range(4-len(res)): res = [0]+res
    l = res
    return l

t = [0] + [2**i for i in range(1, 20)]
set1 = set([])
from itertools import combinations_with_replacement as cwr
from itertools import permutations as pm

for i in cwr(t, 4):
    for j in pm(i):
        set1.add(j)

print(len(set1))

list1 = list(set1)
d1, d2 = {}, {}
for i in list1:
    v = list(i)
    d1[i] = left(v)
    d2[i] = right(v)
print(len(d1), len(d2))
ds=[d1, d2]

import pickle
with open('ds1.pickle', 'wb') as var:
    pickle.dump(ds, var)


















