'''The solution will consist of processing all rows first, then columns one by one, considering whether among all legal arrangements it can infer that
some field is painted in the same color in every arrangement. If so, it adds the row corresponding to that field to the queue. If I was considering
a column earlier, I do the same operation symmetrically for the column until the queue is not empty'''

from cmath import inf
from hashlib import shake_128
import random

file = open('zad_input.txt')
p = 0
a = 0
b = 0
i = []
j = []
for line in file:
    list_of_all = line.split()
    num = [int(s) for s in list_of_all if s.isdigit()]
    if p == 0:
        a = num[0]
        b = num[1]
    elif p <= a:
        i.append(num)
    else:
        j.append(num)
    p += 1
tab = [[0] * b for i in range(a)]
cons = [[0] * b for i in range(a)]

prefcol = [[0] * a for k in range(b)]
for u in range(b):
    prefcol[u][0] = j[u][0]
for d in range(0, b):
    for c in range(1, len(j[d])):
        prefcol[d][c] = prefcol[d][c-1]+j[d][c]

row_pref = [[0] * b for k in range(a)]
for u in range(a):
    row_pref[u][0] = i[u][0]
for d in range(0, a):
    for c in range(1, len(i[d])):
        row_pref[d][c] = row_pref[d][c-1]+i[d][c]

sumcol = []
row_sum = []
for k in range(a):
    row_sum.append(sum(i[k]))
for k in range(b):
    sumcol.append(sum(j[k]))


def intersection(lst1, lst2):
    s1 = set(lst1)
    s2 = set(lst2)
    inter = s1.intersection(s2)
    list_of_all = list(inter)
    return list_of_all


def spr_z_cons(bit, list_of_all, wsp):
    if bit == 0:  # row
        for i in range(len(list_of_all)):
            if cons[wsp][i] == 1 and tab[wsp][i] != list_of_all[i]:
                return False
    else:  # column
        for i in range(len(list_of_all)):
            if cons[i][wsp] == 1 and tab[i][wsp] != list_of_all[i]:
                return False
    return True


def rekur_zap(list_of_all, bit, wsp, blocks, nr_b, pref, sum, where_end_of_prev_block):
    if nr_b == len(blocks):
        wyn = []
        for i in range(len(list_of_all)):
            if list_of_all[i] == 1:
                wyn.append((i, 1))
            else:
                wyn.append((i, 0))
        if spr_z_cons(bit, list_of_all, wsp):
            return wyn
        else:
            return [-1]
    else:
        if nr_b != 0:
            st = where_end_of_prev_block+1
            end = len(list_of_all)-(sum-pref[nr_b-1])-(len(blocks)-(nr_b+1))
        else:
            st = 0
            end = len(list_of_all)-sum-(len(blocks)-(nr_b+1))
        first = 1
        for i in range(st, end+1):
            list_of_all1 = list_of_all.copy()
            for j in range(i, i+blocks[nr_b]):
                list_of_all1[j] = 1
            if first == 1:
                intersect = rekur_zap(
                    list_of_all1, bit, wsp, blocks, nr_b+1, pref, sum, i+blocks[nr_b])
                if intersect != [-1]:
                    first = 0
            else:
                res1 = rekur_zap(list_of_all1, bit, wsp, blocks,
                                 nr_b+1, pref, sum, i+blocks[nr_b])
                if res1 != [-1]:
                    intersect = intersection(intersect, res1)
        return intersect


queue = []
for h in range(0, a):  # rows
    queue.append((0, h))
for h in range(0, b):
    queue.append((1, h))

while queue != []:
    bit, wsp = queue.pop(0)
    if bit == 0:  # row
        lis = []
        for ff in range(b):
            lis.append(0)
        res = rekur_zap(lis, bit, wsp, i[wsp],
                        0, row_pref[wsp], row_sum[wsp], 0)
        for ind, var in res:
            if cons[wsp][ind] != 1:
                tab[wsp][ind] = var
                cons[wsp][ind] = 1
                if (1, ind) not in set(queue):
                    queue.append((1, ind))
    else:
        lis = []
        for ff in range(a):
            lis.append(0)
        res = rekur_zap(lis, bit, wsp, j[wsp], 0, prefcol[wsp], sumcol[wsp], 0)
        for ind, var in res:
            if cons[ind][wsp] != 1:
                tab[ind][wsp] = var
                cons[ind][wsp] = 1
                if (0, ind) not in set(queue):
                    queue.append((0, ind))

file = open("zad_output.txt", "w")
for q in range(0, a):
    for g in range(0, b):
        if tab[q][g] == 1:
            print('#', end='', file=file)
        else:
            print('.', end='', file=file)
    print('', file=file)

file.close()
