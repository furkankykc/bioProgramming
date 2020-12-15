#! /usr/bin/env python
# A better way to compute intersections
import time

start = time.time()

a = list("ABCDEFGHIJKXYZ")
b = list("QRSACDTUGHVIJKXZ")
intersection = []

# "mark" each item in a
mark = {}
for i in a:
    mark[i] = 0

# intersection = any "marked" item in b
for j in b:
    if j in mark.keys():
        intersection.append(j)

print(*intersection, "elapsed time :{:.6f} ms".format(time.time() - start))
