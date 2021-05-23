# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:51:23 2021
@summary: Useful math functions
@author: Shiv Muthukumar
"""

# LINE FORM FROM TWO POINTS
# p1,p2 are tuples
# p1,p2 form line -> Ax + By = C
# returns A, B, C
def getLineForm(p1, p2):
    A = p2[1] - p1[1]
    B = p1[0] - p2[0]
    C = A * p1[0] + B * p1[1]
    return A, B, C

# LINE INTERSECT OF TWO INFINITE LENGHT LINES
# p1,p2,p3,p4 are tuples
# p1,p2 form line1 -> A1x+B1y=C1
# p3,p4 form line2 -> A2x+B2y=C2
# x = (C1*B2-C2*B1)/(A1*B2-A2*B1)
# y = (C2*A1-C1*A2)/(A1*B2-A2*B1)
# return intersection point x, y
def getLineIntersect(p1, p2, p3, p4):
    A1, B1, C1 = getLineForm(p1, p2)
    A2, B2, C2 = getLineForm(p3, p4)
    denominator = A1*B2-A2*B1
    if denominator == 0.0:
        return "NULL","NULL"
    x = (C1*B2-C2*B1)/denominator
    y = (C2*A1-C1*A2)/denominator
    return x, y
