# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 19:26:51 2021
@summary: Basic Ant movement engine. Move radom, avoid walls, avoid each other.
@author: Shiv Muthukumar
"""

import random
import numpy as np
import scipy.spatial as spatial
from scipy.spatial.distance import cdist

def initAnts(n, sh, sw):
    pos_arr, theta_arr, color_arr, KNN_arr = [], [], [], []
    ants_set = set()
    while len(pos_arr) < n:
        x, y = random.randint(0, sh), random.randint(0, sw)
        if (x, y) not in ants_set:
            pos_arr.append((float(x), float(y)))
            theta_arr.append(random.randint(0, 360))
            color_arr.append((0, 0, 0))
            KNN_arr.append([])
            ants_set.add((x, y))
    ants_set = set()
    return np.array(pos_arr),np.array(theta_arr),np.array(color_arr),np.array(KNN_arr)

def updateAnts_vectorized(pos, theta, motivation, sh, sw, fov_th, find_knn):
    # UPDATE THETA
    # GENERATE NEW ANGLE IF MOTIVATED    
    rand_vec = np.random.rand(len(pos))
    min_th_vec = theta - fov_th/2
    max_th_vec = theta + fov_th/2
    rand_theta = np.random.randint(min_th_vec, max_th_vec)
    theta = np.where(rand_vec>=1-motivation, rand_theta, theta)
    
    # FIND NEAREST NEIGHBOURS IF FIND_KNN = TRUE
    # IF DIST TO NEAREST NEIGHBOUR LESS THAN THRESHOLD
    #     GO OPPOSITE TO THE ANGLE BETWEEN POINT AND NEIGHBOUR
    # ELSE CONTINUE IN SAME DIRECTION
    if find_knn:
        point_tree = spatial.KDTree(pos)
        _ , KNN = point_tree.query(pos, k=2)
        posK1 = pos[KNN[:,1]]
        thetaBTW = np.degrees(np.arctan2((posK1[:,1] - pos[:,1]),(posK1[:,0] - pos[:,0])))
        theta = np.where(cdist(pos,posK1).diagonal() <= 10, (thetaBTW + 180) % 360, theta)
    
    # FORCE A NEW ANGLE THAT AVOID WALL COLLISION
    tx_vec = pos[:,0] + np.cos(np.radians(theta))
    ty_vec = pos[:,1] + np.sin(np.radians(theta))
    theta = np.where(tx_vec<=1, random.randint(270, 450) % 360, theta)
    theta = np.where(tx_vec>=sw-1, random.randint(90, 270), theta)
    theta = np.where(ty_vec<=1, random.randint(0, 180), theta)
    theta = np.where(ty_vec>=sh-1, random.randint(180, 360), theta)
    
    # UPDATE POS
    pos[:,0] = pos[:,0] + np.cos(np.radians(theta))
    pos[:,1] = pos[:,1] + np.sin(np.radians(theta))
    
    if find_knn:
        return pos,theta,KNN[:,1]
    else:
        return pos,theta