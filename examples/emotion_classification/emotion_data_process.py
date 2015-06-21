from scipy import *
import numpy
def mean_std_compute(inputFilename):
	#preprocessing: compute the mean and std variance of dataset
	coordinates = []

	for l in file(inputFilename).readlines():
		txtfile = l.strip()
		if len(txtfile):
			print txtfile
		#read the coordinate data.
		mocap = open(txtfile,'r')
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
		            float_element = float(elements)    
		            newpt.append(float_element)
		        coordinates.append(newpt)        
	print len(coordinates)
	inputmean = zeros(len(coordinates[0]))
	inputstd = zeros(len(coordinates[0]))
	for i in range(0,len(inputmean)):
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
	return (inputmean,inputstd)

