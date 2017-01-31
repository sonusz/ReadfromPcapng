#!/usr/bin/env python
"""
Get random arrival time
"""
import random
import numpy as np

def rand_arr_time(option,number_of_packets,duratation):
    """
    options:
    0 random
    1 uniform
    2 gauss
    3 poisson
    4 poisson with random expectation of interval
    5 poisson of poisson with random expectation of interval
    6 poisson with sin(i*10) as expectation of interval
    7 poisson with sin(i)*rand() as expectation of interval
    8 randomly pick one of above functions
    """
    out=[]
    timestamp=0.0
    out.append(timestamp)
    rand_range=2*float(duratation)/float(number_of_packets)
    if option==0:
        for i in range(number_of_packets):
            timestamp+=random.random()*rand_range
            out.append(timestamp)
    elif option==1:
        for i in range(number_of_packets):
            timestamp+=random.uniform(0,rand_range)
            out.append(timestamp)
    elif option==2:
        for i in range(number_of_packets):
            timestamp+=max(0,random.gauss(rand_range/2,rand_range/10))
            out.append(timestamp)
    elif option==3:
        for i in range(number_of_packets):
            timestamp+=np.random.poisson(rand_range/2)
            out.append(timestamp)
    elif option==4:
        for i in range(number_of_packets):
            timestamp+=np.random.poisson(random.random()*rand_range)
            out.append(timestamp)
    elif option==5:
        for i in range(number_of_packets):
            timestamp+=np.random.poisson(np.random.poisson(random.random()*rand_range))
            out.append(timestamp)
    elif option==6:
        for i in range(number_of_packets):
            timestamp+=np.random.poisson((1+np.sin(i*10))*rand_range/2)
            out.append(timestamp)
    elif option==7:
        for i in range(number_of_packets):
            timestamp+=np.random.poisson((1+np.sin(i*10))*random.random()*rand_range)
            out.append(timestamp)
    elif option==8:
        for i in range(number_of_packets):
            temp=rand_arr_time(random.randint(0, 7),1,0.01)
            timestamp += float(temp[1])
            out.append(timestamp)
    return out
