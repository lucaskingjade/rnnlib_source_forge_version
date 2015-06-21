#!/usr/bin/env python
import netcdf_helpers
from scipy import *
from optparse import OptionParser
import sys

coordinates = []
mocap = open('Ses01F_impro01.txt','r')
for frame in mocap.readlines():
    pt=frame.split(' ')
    if 'Frame#' in pt :
        continue
                
    elif 'X01' in pt :
        continue
                
    else:
        pt.pop(0)
        pt.pop(0)  
        newpt = []
        for elements in pt:
            if elements == 'NaN':
                float_element = 0.0
            else:
                float_element = float(elements)    
            newpt.append(float_element)
        coordinates.append(newpt)        
print len(coordinates)
inputmean = zeros(len(coordinates[0]))
inputstd = zeros(len(coordinates[0]))
for i in range(len(inputmean)):
    sum = 0.0
    for j in range(len(coordinates)):
        sum = sum + coordinates[j][i]
    inputmean[i] = sum/len(coordinates)
    sum = 0.0
    for j in range(len(coordinates)):
        sum = sum + pow((coordinates[j][i]- inputmean[i]),2)
    inputstd[i] = sqrt(sum/len(coordinates))
print 'inputmean is\n',inputmean
print 'inputstd is\n',inputstd
print 'you have finish the computation'
    
print len(inputmean)

