# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:42:33 2016

@author: Work
"""
import numpy as np

diff = 1
V = np.zeros(101)
while diff > 0.01:
    diff = 0
    for capital1 in range(1,100):
        max_stake = min(capital1,100-capital1)
        temp = -100
        for stake in range(1,max_stake):
            temp = max(temp,0.4*0.9*V[capital1+stake] + 0.6*0.9*V[capital1-stake])
        if capital1 < 50:
            temp = max(temp,0.4*0.9*V[capital1+max_stake] + 0.6*0.9*V[capital1-stake])
        elif capital1 >= 50:
            temp = max(temp,0.4*(0.9*V[capital1+max_stake] + 1) + 0.6*0.9*V[capital1-stake])
        diff = max(diff,abs(temp-V[capital1]))
        V[capital1] = temp

policy = np.zeros(99)        
for capital1 in range(1,100):
    max_stake = min(capital1,100-capital1)
    optimal_val = -100
    for stake in range(1,max_stake):
        temp = 0.4*0.9*V[capital1+stake] + 0.6*0.9*V[capital1-stake]
        if temp > optimal_val:
            optimal_val = temp
            policy[capital1-1] = stake