#This program will take an igor file within the same folder as this python file and extract the force clamp data
# May require moving clamp data to be directly under root

# force floating point division. Can still use integer with //
from __future__ import division
# other good compatibility recquirements for python3
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from igor.packed import load as loadpxp


import numpy 
from decimal import Decimal
import itertools
import csv
import os
import numpy
import re
import pandas
import numpy
import matplotlib.pyplot as plt



"""
<Description>

Args:
   param1: This is the first param.
	
Returns:
   This is a description of what is returned.
	"""
experiment = loadpxp("./2019.01.01.SdrGBullCantileverRampClamp_clean.pxp")
# experiment = loadpxp("./2019.01.01.SdrGBullCantileverRampClamp_delTraceClean.pxp")
# unpack the pxp
_, file_structure = experiment
	
count = 0
	
# get the folder we care about
folder_we_care_about = file_structure['root']['ForceClamp']['SavedData']
print(count)
while count < 2000:
	print (count)
	strCount = str(count)
	
	Defl_wave = folder_we_care_about['DefV'+strCount].wave
	Defl_labels = Defl_wave['wave']['labels']
	Defl_data = Defl_wave['wave']['wData']
	Defl_note = Defl_wave['wave']['note']
	print (Defl_note)
	# I save the values out as strings, it was the only way I could get a clean list of strings out of the note. Note is a dictionary function
	with open(strCount+"_note.txt", "w") as output:
		output.write(str(Defl_note))
	with open(strCount+"_note.txt", 'r') as f:
		lines=f.read().split(';')
		
	#get the values I care about
	# springConstant = float(re.sub('K=', '', lines[0]))
	# DeflInvols = float(re.sub('Invols=', '', lines[1]))
	# SamplingRate = float(re.sub('SamplingRate_Hz=', '', lines[15]))
	# Force = float(re.sub('Force_N=', '', lines[16]))
	# DeflOffset = float(re.sub('DefVOffset=', '', lines[17]))
	# RampTrace = re.sub('NearestForcePull=', '', lines[36])
	
	# ValuesIWant = []
	# ValuesIWant.append(springConstant)
	# ValuesIWant.append(DeflInvols)
	# ValuesIWant.append(SamplingRate)
	# ValuesIWant.append(Force)
	# ValuesIWant.append(DeflOffset)
	# ValuesIWant.append(RampTrace)
	
	# print (ValuesIWant)
	# with open(strCount+'_ValuesIWant.csv', "wb") as NewFile:
		# writer = csv.writer(NewFile)
		# writer.writerow(ValuesIWant)
		
	  # # get the data waves ( I think these are the ones you wanted for V and Z?)
	  # print off the settings and callback
	DefV_wave = folder_we_care_about['DefV'+strCount].wave
	DefV_data = DefV_wave['wave']['wData']
	
	with open(strCount+'_DeflV.csv', "wb") as NewFile:
		writer = csv.writer(NewFile)
		writer.writerow(DefV_data)
		
		
	Zsensor_wave = folder_we_care_about['ZSensor'+strCount].wave
	Zsensor_data = Zsensor_wave['wave']['wData']
	
	with open(strCount+'_ZsensorV.csv', "wb") as NewFile:
		writer = csv.writer(NewFile)
		writer.writerow(Zsensor_data)
		
	# plt.close()
	# plt.plot(V.wave['wave']['wData'], Z.wave['wave']['wData'])
	# plt.show()
	
	count += 1
		
	
# print off the settings and callback
# callback_wave = folder_we_care_about['FCWaveNamesCallback0'].wave
# callback_labels = callback_wave['wave']['labels']
# callback_data = callback_wave['wave']['wData']
# print("Callback labels: {:s}, data: {:s}".format(str(callback_labels),
									   # str(callback_data)))
	
	
# # do the same for the settings
# settings_wave = folder_we_care_about['FCSettings0'].wave
# settings_labels = settings_wave['wave']['labels']
# settings_data = settings_wave['wave']['wData']
# print("Settings labels: {:s}, data data: {:s}".format(str(settings_labels),
										   # str(settings_data)))
   

  # # get the data waves ( I think these are the ones you wanted for V and Z?)
# V, Z = folder_we_care_about['DefV0'], folder_we_care_about['ZSensor0']
# plt.close()
# plt.plot(V.wave['wave']['wData'], Z.wave['wave']['wData'])
# plt.show()