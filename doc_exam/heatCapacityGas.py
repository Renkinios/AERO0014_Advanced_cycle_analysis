#!/usr/bin/python3

from numpy import *
import pandas
import scipy

def gasHeatCapacity(name,T):
    fname = "heatCapacity_g%s.csv"%name
    data = pandas.read_csv(fname,dtype=float64,header=None,names=["T","Cp"])
    return interp(T,data["T"],data["Cp"])*1000
    
