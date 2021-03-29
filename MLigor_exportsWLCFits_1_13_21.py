#This program will take an igor file within the same folder as this python file and extract the force clamp data


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
import os.path




"""
<Description>

Args:
   param1: This is the first param.
    
Returns:
   This is a description of what is returned.
    """
experiment = loadpxp("./210202.FLSopE2_BestTraces_clean.pxp")
# experiment = loadpxp("./2019.01.01.SdrGBullCantileverRampClamp_delTraceClean.pxp")
# unpack the pxp
_, file_structure = experiment
    
# get the folder we care about
folder_we_care_about = file_structure['root']['MyForceData']['WLCFits']
dictkeys = []
dictkeys = folder_we_care_about.keys()
print (dictkeys)
print (len(dictkeys))
print(type(folder_we_care_about))
count = 0
combinedData = numpy.array([])
for i in dictkeys:
    print (str(i))
    file_we_care_about = folder_we_care_about[i].wave
    
    DefV_wave = file_we_care_about
    DefV_data = numpy.array ([])
    DefV_data = DefV_wave['wave']['wData']
    
    CharacterList1 = [item[0] for item in DefV_data]
    CharacterList2 = [item[1] for item in DefV_data]
    CharacterList3 = [item[2] for item in DefV_data] #contour length (meters)
    CharacterList4 = [item[3] for item in DefV_data] #persistence length (meters)
    CharacterList5 = [item[4] for item in DefV_data] #contour length guess (meters)
    CharacterList6 = [item[5] for item in DefV_data] #persistence length guess (meters)
    CharacterList7 = [item[6] for item in DefV_data] #blank (kept because it matches old format)
    CharacterList8 = [item[7] for item in DefV_data] #blank (kept because it matches old format)
    CharacterList9 = [item[8] for item in DefV_data] #Rupture force (newtons)
    CharacterList10 = [item[9] for item in DefV_data] #loading rate (N/s)
    CharacterList11 = [item[10] for item in DefV_data] #velocity (m/s)
    CharacterList12 = []
    CharacterList13 = []
    CharacterList14 = []
    CharacterList15 = []
    if len(CharacterList3) > 1:
        CharacterList12 = [1E9*x for x in CharacterList3] #convert contour length into nm
        CharacterList12.append(0)
        print(CharacterList12)
        print(CharacterList3)
        CharacterList13 = [] #calculate change in contour length
        tempCount = 0
        holdValue = 0
        for x in CharacterList12:
            if tempCount == 0:
                holdValue = x
                tempCount += 1
            else:
                tempValue = x - holdValue
                CharacterList13.append(tempValue)
                holdValue = x
                tempCount += 1
        print (CharacterList13)
        CharacterList14 = [1E12*x for x in CharacterList9] #Convert rupture force to pN
        CharacterList15 = [1E12*x for x in CharacterList10] #Convert loading rate to pN/s
        CharacterList12.pop()
        print (CharacterList12)
    
    
    ArrayedList = numpy.array([CharacterList1, CharacterList2, CharacterList3, CharacterList4, CharacterList5, CharacterList6, CharacterList7, CharacterList8, CharacterList9, CharacterList10, CharacterList11, CharacterList12, CharacterList13, CharacterList14, CharacterList15])
    TransposeList = numpy.transpose(ArrayedList)
    
    if len(CharacterList1) >1:
        with open(i+'first_WLCFit.csv', "wb") as NewFile:
            writer = csv.writer(NewFile)
            writer.writerows(TransposeList)
    
    if count == 0:
        # with open('combined_WLCFit.csv', "wb") as NewFile:
            # writer = csv.writer(NewFile)
            # writer.writerows(TransposeList)
        count += 1
    else:
        # with open('combined_WLCFit.csv', "a") as NewFile:
            # writer = csv.writer(NewFile)
            # writer.writerows(TransposeList)
        count += 1
    
    # print(type(DefV_data))
    
    
    
    # with open(i + '_WLCFit.csv', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerow(DefV_data)


        
    
    
# while count < len(dictkeys):
    # print (count)
    # strCount = str(count)
    
    
    # count +=1
    # default = 'CSP_5long_error_WLCF.wave'
    
    # file_name = 'CSP_5long_'+strCount+'_WLCF.wave'
    # a = folder_we_care_about.get(file_name, default)

    # print (a)
    # file_we_care_about = folder_we_care_about[file_name].wave
    
    # if file_we_care_about in folder_we_care_about:
        # print ("exists")
        # count +=1
    # else:
        # print ("does not exists")
        # count +=1
        
        
    # if os.path.isfile(file_we_care_about):
        # print ("File exist")
    # else:
        # print ("File not exist")
    
    # count +=1
    # if path.exists(file_we_care_about) == True
        # DefV_wave = file_we_care_about
        # DefV_data = DefV_wave['wave']['wData']
        
        # with open(strCount+'_WLCFit.csv', "wb") as NewFile:
            # writer = csv.writer(NewFile)
            # writer.writerow(DefV_data)
            
        # count += 1
    # else 
        # count += 1

        
      # # get the data waves ( I think these are the ones you wanted for V and Z?)
      # print off the settings and callback
    # DefV_wave = a
    
    # DefV_data = DefV_wave['wave']['wData']
    
    # with open(strCount+'_WLCFit.csv', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerow(DefV_data)

    
    # count += 1
        
    
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