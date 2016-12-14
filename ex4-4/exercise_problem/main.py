# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 18:26:29 2016

@author: queky
"""
import numpy as np
import itertools
from CarRentalState import CarRentalState
import sys

def polEval(policy):
    assert policy.shape == (CarRentalState.state_max+1,CarRentalState.state_max+1)
    V = np.zeros((CarRentalState.state_max+1,CarRentalState.state_max+1))
    (Pa,Pb,Ra,Rb) = CarRentalState.stateTransEnv()
    
    diff = 1 # just for entering while loop
    while diff > 0.01:
        diff = 0
        for stateA,stateB in itertools.product(range(CarRentalState.state_max+1),
                                               range(CarRentalState.state_max+1)):
            tmp = 0
            cars2move = policy[stateA,stateB]
            stateA_moved,stateB_moved = CarRentalState.moveCars(stateA,stateB,cars2move)
            
            # One free move if moving from first to second
            free_move = 0
            if cars2move > 0:
                free_move = 1
            
            for new_stateA,new_stateB in itertools.product(range(CarRentalState.state_max+1),
                                                           range(CarRentalState.state_max+1)):
                tmp += Pa[stateA_moved,new_stateA]*Pb[stateB_moved,new_stateB]* \
                       (Ra[stateA_moved,new_stateA]+Rb[stateB_moved,new_stateB]-
                       abs(cars2move)*2 + 2*free_move + 0.9*V[new_stateA,new_stateB])
                       
            diff = max(diff,abs(V[stateA,stateB]-tmp))
            V[stateA,stateB] = tmp  
    return V

def polImprove(policy):
    (Pa,Pb,Ra,Rb) = CarRentalState.stateTransEnv()
    stable = False
    while not stable:
        print "one iteration"
        stable = True
        V = polEval(policy)
        for stateA,stateB in itertools.product(range(CarRentalState.state_max+1),
                                               range(CarRentalState.state_max+1)):
            old_action = policy[stateA,stateB]
            new_action_value = -100
            for cars2move in range(-5,6):
                try:
                    stateA_moved,stateB_moved = CarRentalState.moveCars(stateA,stateB,cars2move)
                except ValueError:
                    continue
                tmp = 0
                for new_stateA,new_stateB in itertools.product(range(CarRentalState.state_max+1),
                                                               range(CarRentalState.state_max+1)):
                    tmp += Pa[stateA_moved,new_stateA]*Pb[stateB_moved,new_stateB]* \
                           (Ra[stateA_moved,new_stateA]+Rb[stateB_moved,new_stateB]-
                           abs(cars2move)*2+0.9*V[new_stateA,new_stateB])
                if tmp > new_action_value:
                    new_action_value = tmp
                    new_action = cars2move
            if old_action != new_action:
                policy[stateA,stateB] = new_action
                stable = False                
    return policy
    
policy = np.ones((CarRentalState.state_max+1,CarRentalState.state_max+1)).astype(np.int32)
policy[0,:] = 0
V = polImprove(policy)