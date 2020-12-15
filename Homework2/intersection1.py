#! /usr/bin/env python
# An inefficient way to compute intersections
import time

start = time.time()

a = list("ABCDEFGHIJKXYZ")
b = list("QRSACDTUGHVIJKXZ")
intersection = []
for i in a:
    for j in b:
        if i == j:
            intersection.append(i)
print(*intersection, "elapsed time :{:.6f} ms ".format(time.time() - start))
