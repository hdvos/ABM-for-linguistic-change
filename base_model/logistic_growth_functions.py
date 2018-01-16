# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 11:17:57 2016

@author: hdevos
"""
import math
import matplotlib.pyplot as plt

c = 1 # if c = 1 x = 0 equals p = .5
a = .1 # steepness
xlim = 100




def sigmoid(x, c, a):
    if x <= 5000 and x >= -5000:
        return 1 / (1 + c * math.exp(-a * x))
    elif x > 5000:
        return 1 / (1 + c * math.exp(-a * 5001))
    elif x < -5000:
        return 1 / (1 + c * math.exp(-a * (-5001)))


# an implementation of -((math.log((1/y - 1) / c)) / a)
# Different steps are for the sake of debugging
# This formula is the sigmoid formula with the x isolated and the y as the known variable
def inverse_sigmoid(y, c, a):    
    step_1 = 1/y -1
    step_2 = step_1 / c
    step_3 = math.log(step_2)
    step_4 = step_3 / a
    step_5 = -1 * step_4
    return step_5    
        
    





















def test_sigmoid(a,c,xlim):
    track = []
    x_axis = []
    
    for x in range(-xlim,xlim):
        y = sigmoid(x,c,a)
        track.append(y)
        x_axis.append(x)
        
    
    
    plt.plot(x_axis, track)
    
def test_inverse_sigmoid(a,c, precision):
    track = []
    x_axis = []
    
    
    for y in range(1,precision):
        y_2 = y/precision
        x = inverse_sigmoid(y_2,c,a)
        track.append(x)
        x_axis.append(y)
    
    plt.plot(track,x_axis)
  
