import pandas
import numpy
import csv
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

count = 0

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail
    
    
def findSpikesandDwells (CombinedFilesNames, saveDir): 
    
    saveDir = saveDir
    ZSensor_filename = CombinedFilesNames[0]#filename will end up being ZSensor0.txt.csv if the original csv file is named ZSensor0.txt
    Defl_filename = CombinedFilesNames[1]
    NotePath = CombinedFilesNames[2]
    print ZSensor_filename   #makes it easier to track which results go with which file
    # print Defl_filename
    # print NotePath
    
    OpenedFile = open(NotePath, "r")
    for line in OpenedFile:
        fields = line.split(";")
        for i in fields:
            if "K=" in i:
                CleanSpringConstant = float(i.replace("K=",""))
                springConstant = CleanSpringConstant * 1E3 #converts spring constant from N/m to pN/nm
                
            if "NearestForcePull=" in i:
                SimplifiedRampNumber = i.replace("NearestForcePull=","")
                SimplifiedRampNumber = SimplifiedRampNumber[-7:]
                
            if "DefVOffset=" in i:
                CleanDefVOffset = float(i.replace("DefVOffset=",""))
                
            if "SamplingRate_Hz=" in i:
                SampleRate = float(i.replace("SamplingRate_Hz=",""))
                
            if "Invols=" in i:
                CleanInvols = float(i.replace("Invols=",""))
                
            if "Force_N=" in i:
                Force = float(i.replace("Force_N=",""))
                
            if "Iteration=" in i and "Script" not in i:
                Iteration = str(int(i.replace("Iteration=","")))
                
            if "ZLVDTSens=" in i:
                Zsensitivity = float(i.replace("ZLVDTSens=",""))
                
            if "ZLVDTOffset" in i:
                ZSenseOffset = float(i.replace("ZLVDTOffset=",""))

    CombinedValues = []
    CombinedValues.append(CleanSpringConstant)
    CombinedValues.append(CleanDefVOffset)
    CombinedValues.append(CleanInvols)
    CombinedValues.append(SampleRate)
    CombinedValues.append(Force)
    
    print CombinedValues # Provides a single list with the spring constant, DefVOffset, Invols, and Sample rate (Hz), and Force (N) directly from the parameters file
    
        
    
    
    colnames_ZSensor = ['time_s', 'position_Z_nm']              #the two columns in the csv are time and Z sensor position
    data_ZSensor = pandas.read_csv(ZSensor_filename, names=colnames_ZSensor)    #read in the data from the csv with the assigned names

    time_s = data_ZSensor.time_s.tolist()                       #write the time data into a list - not currently used for anything
    position_Z_nm = data_ZSensor.position_Z_nm.tolist()             #write the zSensor position into a list
    
    
    colnames_Defl = ['time_ms_defl', 'Deflection_nm', 'Force_pN']               #the two columns in the csv are time and Z sensor position
    data_Defl = pandas.read_csv(Defl_filename, names=colnames_Defl) #read in the data from the csv with the assigned names

    time_ms_defl = data_Defl.time_ms_defl.tolist()                      #write the time data into a list - not currently used for anything
    Defl_nm = data_Defl.Deflection_nm.tolist()  #write the zSensor position into a list
    Force_pN = data_Defl.Force_pN.tolist()
    
    combined_Z_Defl = []
    combined_Z_Defl = zip(position_Z_nm, Defl_nm)
    
    
    
    Extension = []
    for x, y in combined_Z_Defl:
        ext = x-y
        Extension.append(ext)
        
    timevsextension= zip(time_s, Extension)
    
    # with open(ZSensor_filename+'_extension.csv', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(timevsextension)
        
    
    if SampleRate == 1000:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 2000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 9, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    elif SampleRate == 10000:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 3000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 15, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    elif SampleRate == 50000:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 5000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 31, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    else:
        print "sample rate not 1000 or 50000, leaving extension alone"
        Smooth_Extension = Extension
        xx = numpy.linspace(time.min(), time.max(), 3000)

        
        
    time_vs_smoothExtension = zip(xx, Smooth_Extension)
    
    # with open(ZSensor_filename+'_SmoothExtension.csv', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(time_vs_smoothExtension)

    # plt.close()
    # plt.plot(time_s, Force_pN)
    # plt.show()

    # plt.close()
    # plt.plot(time_s, position_Z_nm)
    # plt.show()
    
    
    
    
    # plt.close()
    # plt.plot(time_s, Extension)
    # plt.plot(xx, Smooth_Extension, color ='red')
    # plt.ylim(1000, 1300)
    # plt.show()

    # # with open('test.txt', 'w') as f:
        # # for item in differential:
            # # f.write("%s\n" % item)

    spiketimes = []
    rawIndex = []
    rawValue = []
    rawDelta = []
    combiList = []
    
    rawIndexDwell = []
    rawValueDwell = []
    rawDeltaDwell = []
    combiListDwell = []
    
    DwellDrop = []
    combiListDwellDrop = []

    def findTotalClampTime(time, Extension, lowthreshold=5, highthreshold=5000000):             #this program identifies when the differential between data points
        count = 0
        listLength = len(Extension)
        prev = None     #is above and below the set thresholds. Changing the thresholds changes the sensitivity
        while count < len(time):
            i = time[count]
            v = Extension[count]
            if prev is None:
                prev = v
                continue

            delta = abs(v - prev)
            if delta >= lowthreshold and delta <= highthreshold:
                print("Found unsmoothed spike at index %d (value %f) (jump %s)" % (i, v, delta))
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawIndex.append(i)
            
            if delta >= lowthreshold and delta <= highthreshold:
                rawValue.append(v)
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawDelta.append(delta)
            
            # if delta >= lowthreshold and delta <= highthreshold:
                # break
                
            if count == (listLength-1):
                print "no large spike detected, writing the last value as the time"
                
            if count == (listLength-1):
                rawIndex.append(i)
            if count == (listLength-1):
                rawValue.append(v)
            if count == (listLength-1):
                rawDelta.append(delta)


            prev = v
            count += 1


    
    spiketimes = []
    smoothedIndex = []
    smoothedValue = []
    smoothedDelta = []
    combiList = []
    
    smoothedIndexDwell = []
    smoothedValueDwell = []
    smoothedDeltaDwell = []
    combiListDwell = []
    
    def findTotalClampTimeSmooth(time, Extension, lowthreshold=3, highthreshold=5000000):               #this program identifies when the differential between data points
        count = 0
        listLength = len(Extension)
        prev = None     #is above and below the set thresholds. Changing the thresholds changes the sensitivity
        while count < listLength:
            i = time[count]
            print count
            v = Extension[count]
            if prev is None:
                prev = v
                continue

            delta = abs(v - prev)
            if delta >= lowthreshold and delta <= highthreshold:
                print("Found smooth spike at index %d (value %f) (jump %s)" % (i, v, delta))
                print count, i, v, delta
                
            if delta >= lowthreshold and delta <= highthreshold:
                smoothedIndex.append(i)
            
            if delta >= lowthreshold and delta <= highthreshold:
                smoothedValue.append(v)
                
            if delta >= lowthreshold and delta <= highthreshold:
                smoothedDelta.append(delta)
            
            # if delta >= lowthreshold and delta <= highthreshold:
                # break
                
            if count == (listLength-1):
                print "no large spike detected, writing the last value as the time"
                
            if count == (listLength-1):
                smoothedIndex.append(i)
            if count == (listLength-1):
                smoothedValue.append(v)
            if count == (listLength-1):
                smoothedDelta.append(delta)


            prev = v
            count += 1
    
    
    def findSpikes(data, lowthreshold=0.5, highthreshold=5000000):                #this program identifies when the differential between data points
        prev = None                                                           #is above and below the set thresholds. Changing the thresholds changes the sensitivity
        for i, v in enumerate(data):
            if prev is None:
                prev = v
                continue

            delta = abs(v - prev)
            if delta >= lowthreshold and delta <= highthreshold:
                print("Found spike at index %d (value %f) (drop %s)" % (i, v, delta))
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawIndex.append(i)
            
            if delta >= lowthreshold and delta <= highthreshold:
                rawValue.append(v)
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawDelta.append(delta)
            
            if delta >= lowthreshold and delta <= highthreshold:
                spiketimes.append(i)
                
            

            prev = v

    def findSpikeDwells(data, lowthreshold=2, highthreshold=100000000):       #this program takes in the spike times and identify the dwell time between the spikes
        prev = None                                                           #this allows you identify and store the lifetimes at each step
        for i, v in enumerate(data):
            if prev is None:
                prev = v
                continue

            delta = abs(v - prev)
            if delta >= lowthreshold and delta <= highthreshold:
                print("Spike dwell at index %d (value %f) (dwell %s)" % (i, v, delta))
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawIndexDwell.append(i)
            
            if delta >= lowthreshold and delta <= highthreshold:
                rawValueDwell.append(v)
                
            if delta >= lowthreshold and delta <= highthreshold:
                rawDeltaDwell.append(delta)
                
            

            prev = v
    
	print len(time_s), len(Force_pN)
    findTotalClampTime(time_s, Extension)
    findTotalClampTimeSmooth(xx, Smooth_Extension)
    # findSpikes(Extension)
    # findSpikeDwells(spiketimes)
    # print spiketimes
    
    ForceList = []
    ForceListSmooth = []
    lenForceMake = len(rawIndex)
    lenForceSmooth = len(smoothedIndex)
    count =0
    while count <= lenForceMake:
        ForceList.append(Force)
        count +=1
    count =0
    while count <= lenForceSmooth:
        ForceListSmooth.append(Force)
        count +=1
    combiList = zip(rawIndex, rawValue, rawDelta, ForceList)
    smoothCombiList = zip(smoothedIndex, smoothedValue, smoothedDelta, ForceListSmooth)
    combiListDwell = zip(rawIndexDwell, rawValueDwell, rawDeltaDwell)
    # print rawValue
    # print combiList
    
    
    
    
    # for i in combiListDwell:    #necessary to associate the spike changes to their associated step dwell times
        # tempvar = 0
        # indexpos = 0
        # dropvalue = 0
        # tempvar = i[1]
        # indexpos = spiketimes.index(tempvar)
        # dropvalue = combiList[indexpos][2]
        # DwellDrop.append(dropvalue)
    
    # combiListDwellDrop = zip(rawValueDwell, DwellDrop, rawDeltaDwell) # this will likely be the most useful file. writes out zsensor position, height of the step, and length of the step
    
    # print combiList
    # print combiListDwell
    # print combiListDwellDrop
    
    
    # with open(ZSensor_filename+'_Spikes.txt', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(combiList)
        
    # with open(ZSensor_filename+'_Dwells.txt', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(combiListDwell)
        
    # with open(ZSensor_filename+'_highsens_DropDwells.csv', "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(combiListDwellDrop)

    with open(saveDir+'\_'+Iteration+'_'+SimplifiedRampNumber+'_'+str(Force)+'_'+'Force_Jumps.csv', "wb") as NewFile:
        writer = csv.writer(NewFile)
        writer.writerows(combiList)
        
    with open(saveDir+'\_'+Iteration+'_'+SimplifiedRampNumber+'_'+str(Force)+'_'+'Force_SJumps.csv', "wb") as NewFile:
        writer = csv.writer(NewFile)
        writer.writerows(smoothCombiList)
        
    
    return



rootdirNotes = raw_input('root directory Notes: ') # location of the notes as txt files
rootdirZSensor = raw_input('root directory ZSensor: ') # location of the zSensor data - preconverted to CSV
rootdirDefl = raw_input('root directory Deflection: ') # location of the deflection data - preconverted to CSV
# rootdirExtension = raw_input('root directory Extension: ') # location of the deflection data - preconverted to CSV

saveDir = raw_input('where do you want to save files ')

ZSensorPaths_lst = []
for subdir, dirs, files in os.walk(rootdirZSensor):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith("_C.csv"):
             ZSensorPaths_lst.append(filepath)
             
NotesPath = []             
for subdir, dirs, files in os.walk(rootdirNotes):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith("note.txt"):
             NotesPath.append(filepath)
    
DeflPaths_lst = []
for subdir, dirs, files in os.walk(rootdirDefl):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file

        if filepath.endswith("_C.csv"):
             DeflPaths_lst.append(filepath)


ZandDeflPath_lst = zip(ZSensorPaths_lst, DeflPaths_lst, NotesPath)



for i in ZandDeflPath_lst:
    findSpikesandDwells(i, saveDir)
    




 
 
# from decimal import Decimal
# import itertools
# import os
# import numpy


# #rawVoltage = float(input('rawVolts: ')) # Use for variable rawVoltage numbers
# rawVoltage = float('1.707E-7') # Use for constant rawVoltage numbers

# #fileName = raw_input('File Name: ')

# count = 0
# rootdir = raw_input('root directory: ') # location of the zSensor data


# def ConvertAndSave (file, number):
    # fileName = str(number)+".csv"
    # print fileName


    # Volts = numpy.loadtxt(file, usecols=1)
    # Volts_lst = numpy.array(Volts).tolist()

    # ms = numpy.loadtxt(file, usecols = 0)
    # ms_lst = numpy.array(ms).tolist()



    # Voltage_to_meters = [i * -rawVoltage for i in Volts_lst]  

    # meters_to_nm = [i * 1E9 for i in Voltage_to_meters] 

    # combinedLists = zip(ms_lst, meters_to_nm)


    # with open(fileName, "wb") as NewFile:
        # writer = csv.writer(NewFile)
        # writer.writerows(combinedLists)
        
    # return;
        
# for subdir, dirs, files in os.walk(rootdir):
    # for file in files:
        # #print os.path.join(subdir, file)
        # filepath = subdir + os.sep + file

        # if filepath.endswith(".txt"):
             # ConvertAndSave(filepath, count)
    # count +=1
    # print count
