# -*- coding: utf-8 -*-
"""
Created on Fri Dec 09 09:59:38 2016

@author: queky
"""
import math
import numpy as np

def poispdf(n,lamb):
    return lamb**n/float(math.factorial(n))*math.exp(-lamb)

def stateTransProb():
    Pa = np.zeros((21,21))
    Pb = np.zeros((21,21))
    for state1 in range(21):
        for req in range(21):
            rent = min(req,state1)
            for returned in range(21):
                state2 = min(state1 - rent + returned,20)
                Pa[state1,state2] += poispdf(req,3)*poispdf(returned,3)
                Pb[state1,state2] += poispdf(req,4)*poispdf(returned,2)
    return (Pa,Pb)
    
def stateTransRew():
    Pa,Pb = stateTransProb()
    Ra = np.zeros((21,21))
    Rb = np.zeros((21,21))
    for state1 in range(21):
        for req in range(21):
            rent = min(req,state1)
            for returned in range(21):
                state2 = min(state1 - rent + returned,20)
                Ra[state1,state2] += poispdf(req,3)*poispdf(returned,3)*rent
                Rb[state1,state2] += poispdf(req,4)*poispdf(returned,2)*rent
    Ra = Ra*10/Pa
    Rb = Rb*10/Pb
    return (Ra,Rb)