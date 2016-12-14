# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 09:39:41 2016

@author: queky
"""
import numpy as np
import math

class CarRentalState(object):
    state_max = 20
    exp_rentA = 3
    exp_retA = 3
    exp_rentB = 4
    exp_retB = 2
    
    def __init__(self,stateA,stateB):
        assert type(stateA) == int
        assert type(stateB) == int
        assert stateA <= self.state_max
        assert stateB <= self.state_max
        self.stateA = stateA
        self.stateB = stateB
    
    @staticmethod
    def moveCars(stateA,stateB,a):
        assert isinstance(a,int)
        assert a <= 5 and a >= -5
        
        if (not stateA - a >= 0) or (not stateB + a >= 0):
            raise ValueError
        #assert stateA - a >= 0
        #assert stateB + a >= 0
        stateA_moved = min(stateA - a,CarRentalState.state_max)
        stateB_moved = min(stateB + a,CarRentalState.state_max)
        return stateA_moved,stateB_moved
        
    def getState(self):
        return (self.stateA,self.stateB)
    
    @staticmethod
    def stateTransEnv():
        Pa = np.zeros((CarRentalState.state_max+1,CarRentalState.state_max+1))
        Pb = np.zeros((CarRentalState.state_max+1,CarRentalState.state_max+1))
        Ra = np.zeros((CarRentalState.state_max+1,CarRentalState.state_max+1))
        Rb = np.zeros((CarRentalState.state_max+1,CarRentalState.state_max+1))
        for state1 in range(CarRentalState.state_max+1):
            for req in range(21):
                rent = min(req,state1)
                for returned in range(21):
                    state2 = min(state1 - rent + returned,CarRentalState.state_max)
                    # Transition probabilities
                    Pa[state1,state2] += poispdf(req,CarRentalState.exp_rentA)*   \
                                         poispdf(returned,CarRentalState.exp_retA)
                    Pb[state1,state2] += poispdf(req,CarRentalState.exp_rentB)*    \
                                         poispdf(returned,CarRentalState.exp_retB)
                    # Transition rewards
                    Ra[state1,state2] += poispdf(req,CarRentalState.exp_rentA)*    \
                                         poispdf(returned,CarRentalState.exp_retA)*rent
                    Rb[state1,state2] += poispdf(req,CarRentalState.exp_rentB)*    \
                                         poispdf(returned,CarRentalState.exp_retB)*rent
        Ra = Ra*10/Pa
        Rb = Rb*10/Pb
        return (Pa,Pb,Ra,Rb)
    
    def __sub__(self,other):
        return (self.s1 - other.s1,self.s2 - other.s2)
        
def poispdf(n,lamb):
    return lamb**n/float(math.factorial(n))*math.exp(-lamb)