#!/usr/bin/env python
import netcdf_helpers
from scipy import *
import numpy
from optparse import OptionParser
import sys
import os
from PIL import Image
from xml.dom.minidom import parse
from emotion_data_process import *
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
#command line options
parser = OptionParser()
#parse command line options
(options, args) = parser.parse_args()
if (len(args)<2):
	print "usage: -options input_filename output_filename"
	print options
	sys.exit(2)

inputFilename = args [0]
ncFilename = args[1]
print options
print "input filename", inputFilename
print "data filename", ncFilename

#read data from txt file and anvil file into netcdf file
#variables definitions
labels = ["Anger", "Neutral", "Frustration","Sadness","Happiness","Excited","Other"]
inputMeans = []
inputStds = []
seqDims = []
seqLengths = []
targetStrings = []
seqTags = []
filenames = []
inputs = []
emotion_label =[]
start_time =[]
end_time = []
oldlen = 0
print "reading file data"
inputlines = file(inputFilename).readlines()

#open and read the txt file one by one
for line in inputlines:
	mocap_fname = line.strip()
	emotion_label = []
	start_time = []
	end_time = []
	if len(mocap_fname):
		print mocap_fname
		emotion_file = mocap_fname.replace('txt', 'anvil')
		print emotion_file
		#check the gender is male or female
		if 'M' in mocap_fname:
			gender = "Male"
		elif 'F' in mocap_fname:
			gender = "Female"
		else:
			print "there is an error in the name of ", mocap_fname
		if os.path.exists(emotion_file):
			emotion_file_parse = parse(emotion_file)
			body = emotion_file_parse.getElementsByTagName('body')
			index = []
			#find the location of emotion body in the anvil file
			for i in range(0,len(body)):
				track = body[i].getElementsByTagName('track')
				for j in range(0,len(track)):
					if track[j].getAttribute('name') == (gender+".Emotion"):
						index = track[j].getElementsByTagName('el')
						break
				if len(index) != 0:
					break

			if len(index) == 0:
				print "didn't find emotion data in the anvil file"

			for i in range(0,len(index)):          
				start_time.append(float(index[i].getAttribute('start')))
				end_time.append(float(index[i].getAttribute('end')))
				emotion_label.append(index[i].getElementsByTagName('attribute')[0].getAttribute('name'))
				if emotion_label[-1] == u'Neutral state':
					emotion_label[-1]= u'Neutral'
				if emotion_label[-1] not in labels:
					emotion_label.pop()
					start_time.pop()
					end_time.pop()
		print "emotion_label length is ", len(emotion_label)
		mocap = open(mocap_fname,'r')
		mark = 0
		for frame in mocap.readlines():
		    pt=frame.split(' ')
		    
		    if 'Frame#' in pt: 
		        face_point_name = pt
		        face_point_name.pop(0)
		        face_point_name.pop(0)
		        
		    elif 'X01' in pt:
		        coordnum = len(pt)
		    else:
		        frame_time = float(pt[1])
		        
		        for i in range(0,len(emotion_label)):
		
		            if frame_time < start_time[0]:
		                break
		                
		            elif frame_time>= start_time[i] and frame_time <= end_time[i]:
		                face_point_coord = pt
		                face_point_coord.pop(0)
		                face_point_coord.pop(0)
		                face_point_coord[-1]=face_point_coord[-1].strip()
		                newlist = list(map(float,face_point_coord))
		                
		                if mark != i:
		                    print 'mark=',mark
		                    targetStrings.append(emotion_label[mark].encode('ascii'))
		                    seqTags.append((mocap_fname+str(mark)))
		                    seqLengths.append(len(inputs) - oldlen)
		                    seqDims.append([seqLengths[-1]])
		                    mark = i + 0
		                    oldlen = len(inputs)
		                inputs.append(newlist)
		                break
		            elif i == (len(emotion_label)-1):
						break
		            elif frame_time> end_time[i] and frame_time < start_time[i+1]:
		                break
		                
		targetStrings.append(emotion_label[mark].encode('ascii'))
		seqTags.append((mocap_fname+str(mark)))
		seqLengths.append(len(inputs) - oldlen)
		seqDims.append([seqLengths[-1]])
		oldlen = len(inputs)
	else:
	    inputlines.remove(line)
print len(labels), "labels:"
print labels
#normalization
imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(array(inputs))
Imputer(axis=0, copy=True, missing_values='NaN', strategy='mean', verbose=0)
arrayinputs = imp.transform(array(inputs))
inputs = preprocessing.scale(arrayinputs).tolist()

#create a new .nc file
file = netcdf_helpers.NetCDFFile(ncFilename, 'w')

#create the dimensions
netcdf_helpers.createNcDim(file,'numSeqs',len(seqLengths))
netcdf_helpers.createNcDim(file,'numTimesteps',len(inputs))
netcdf_helpers.createNcDim(file,'inputPattSize',len(inputs[0]))
netcdf_helpers.createNcDim(file,'numDims',1 )
netcdf_helpers.createNcDim(file,'numLabels',len(labels))

#create the variables
netcdf_helpers.createNcStrings(file,'seqTags',seqTags,('numSeqs','maxSeqTagLength'),'sequence tags')
netcdf_helpers.createNcStrings(file,'labels',labels,('numLabels','maxLabelLength'),'labels')
netcdf_helpers.createNcStrings(file,'targetStrings',targetStrings,('numSeqs','maxTargStringLength'),'target strings')
netcdf_helpers.createNcVar(file,'seqLengths',seqLengths,'i',('numSeqs',),'sequence lengths')
netcdf_helpers.createNcVar(file,'seqDims',seqDims,'i',('numSeqs','numDims'),'sequence dimensions')
netcdf_helpers.createNcVar(file,'inputs',inputs,'f',('numTimesteps','inputPattSize'),'input patterns')

#write the data to disk
print "closing file", ncFilename
file.close()
#read data from txt file and anvil file into netcdf file

