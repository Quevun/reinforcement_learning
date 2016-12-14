# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 18:52:07 2016

@author: Quek Yu Yang
"""

import numpy as np
import itertools
from CarRentalState import CarRentalState

#V = np.zeros((3,3))

def polEval(V):
    Pa,Pb,Ra,Rb = CarRentalState.stateTransEnv()
    policy = np.ones((CarRentalState.state_max+1,CarRentalState.state_max+1)).astype(np.int32)
    policy[0,:] = 0
    for stateA,stateB in itertools.product(range(3),range(3)):
        cars2move = policy[stateA,stateB]
        stateA_moved,stateB_moved = CarRentalState.moveCars(stateA,stateB,cars2move)
        tmp = 0
        for new_stateA,new_stateB in itertools.product(range(3),range(3)):
            tmp += Pa[stateA_moved,new_stateA]*Pb[stateB_moved,new_stateB]* \
                   (Ra[stateA_moved,new_stateA]+Rb[stateB_moved,new_stateB]-
                   abs(cars2move)*2 + 0.9*V[new_stateA,new_stateB])
        V[stateA,stateB] = tmp
    return V