import pandas
import numpy
import csv
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
from numpy import median

count = 0

def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail
    
    
def findSpikesandDwells (CombinedFilesNames): 
    
    
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
    
    with open(ZSensor_filename+'_extension.csv', "wb") as NewFile:
        writer = csv.writer(NewFile)
        writer.writerows(timevsextension)
        
    #These values allow small differences in sample rate to be dealt with
    DividedSampleRate = SampleRate/1000
    RoundedSampleRate = round(DividedSampleRate, 0)
    
    #because for an unknown reason the extension is sometimes different than the time, this corrects for that by extending the extension list with the last value
    if len(time_s)>len(Extension):
        print len(time_s), len(Extension)
        count = len(Extension)
        copyValue = Extension[count-1]
        while len(Extension) < len(time_s):
            Extension.append(copyValue)
        print "there was a difference in length of time and extension that was corrected for"
        testStop = raw_input('press enter to continue ') #so you know when there was a mismatch and to ensure that the mismatch wasn't too large
    
    if RoundedSampleRate == 1:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 2000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 9, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    elif RoundedSampleRate == 10:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 3000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 15, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    elif RoundedSampleRate == 50:
        print 'time length is: ' , len(time_s), 'Extension length is: ', len(Extension)
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 5000)
        interpolated_time_extension = interp1d(time_s, Extension, kind = 'linear')  
        window_size, poly_order = 31, 2
        Smooth_Extension = savgol_filter(interpolated_time_extension(xx), window_size, poly_order)
        
    else:
        print "sample rate not 1000 or 50000, leaving extension alone"
        time = numpy.asarray(time_s)
        Smooth_Extension = Extension
        # xx = numpy.linspace(time.min(), time.max(), 2000)
        xx = time_s
################################################################################################################################        
    if RoundedSampleRate == 1:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 2000)
        interpolated_time_position_Z_nm = interp1d(time_s, position_Z_nm, kind = 'linear')  
        window_size, poly_order = 9, 2
        Smooth_position_Z_nm = savgol_filter(interpolated_time_position_Z_nm(xx), window_size, poly_order)
        
    elif RoundedSampleRate == 10:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 3000)
        interpolated_time_position_Z_nm = interp1d(time_s, position_Z_nm, kind = 'linear')  
        window_size, poly_order = 15, 2
        Smooth_position_Z_nm = savgol_filter(interpolated_time_position_Z_nm(xx), window_size, poly_order)
        
    elif RoundedSampleRate == 50:
        time = numpy.asarray(time_s)
        xx = numpy.linspace(time.min(), time.max(), 5000)
        interpolated_time_position_Z_nm = interp1d(time_s, position_Z_nm, kind = 'linear')  
        window_size, poly_order = 31, 2
        Smooth_position_Z_nm = savgol_filter(interpolated_time_position_Z_nm(xx), window_size, poly_order)
        
    else:
        print "sample rate not 1000 or 50000, leaving extension alone"
        Smooth_position_Z_nm = position_Z_nm
        # xx = numpy.linspace(time.min(), time.max(), 3000)
        xx = numpy.asarray(time_s)

        
        
    time_vs_smoothExtension = zip(xx, Smooth_Extension)
    
    time_vs_smoothZposition = zip(xx, Smooth_position_Z_nm)
    
    with open(ZSensor_filename+'_SmoothExtension.csv', "wb") as NewFile:
        writer = csv.writer(NewFile)
        writer.writerows(time_vs_smoothExtension)
        
    time_vs_Force = zip(time_s, Force_pN)    
    with open(ZSensor_filename+'_Force.csv', "wb") as NewFile:
        writer = csv.writer(NewFile)
        writer.writerows(time_vs_Force)
        
    medianZ = median(position_Z_nm)
    mZMinus = medianZ - 1
    mZPlus = medianZ + 1
    
    medianForce = median(Force_pN)

    medianExtension = median(Extension)
    mExtensionMinus = medianExtension - 10
    mExtensionPlus = medianExtension + 10
    
    
    print len(time_s), len(Force_pN)
    print len(time_ms_defl), len(Force_pN)
	
    if len(time_ms_defl) > len(Force_pN):
        Force_pN.append(Force_pN[-1])
	
               
    if len(time_ms_defl) == len(Force_pN):
        plt.close()
        plt.plot(time_ms_defl, Force_pN)
        plt.title(Iteration+'_'+SimplifiedRampNumber + '_' + str(Force))
        plt.savefig(Iteration+'_'+SimplifiedRampNumber +'_'+str(Force)+ 'F_full.png')
  



    # plt.close()
    # plt.plot(time_s, position_Z_nm)
    # plt.plot(xx, Smooth_position_Z_nm, color = 'red')
    # plt.savefig(SimplifiedClampNumber + SimplifiedRampNumber + 'Z_full.png')
    
    # plt.close()
    # plt.plot(time_s, position_Z_nm)
    # plt.plot(xx, Smooth_position_Z_nm, color = 'red')
    # plt.ylim(mZMinus, mZPlus)
    # plt.savefig(SimplifiedClampNumber + SimplifiedRampNumber + 'Z_zoom.png')
    

    if len(time_s) == len(Extension):
        plt.close()
        plt.plot(time_s, Extension)
        plt.plot(xx, Smooth_Extension, color ='red')
        plt.title(Iteration+'_'+SimplifiedRampNumber + '_' + str(Force))
        plt.savefig(Iteration+'_'+SimplifiedRampNumber +'_'+str(Force)+ 'E_full.png')
    
    if len(time_s) == len(Extension):
        plt.close()
        plt.plot(time_s, Extension)
        plt.plot(xx, Smooth_Extension, color ='red')
        plt.ylim(mExtensionMinus, mExtensionPlus)
        plt.title( Iteration+'_'+SimplifiedRampNumber + '_' + str(Force))
        plt.savefig(Iteration+'_'+SimplifiedRampNumber +'_'+str(Force)+ 'E_zoom.png')
        plt.close()



        
    
    return


rootdirNotes = raw_input('root directory Notes: ') # location of the notes as txt files
rootdirZSensor = raw_input('root directory ZSensor: ') # location of the zSensor data - preconverted to CSV
rootdirDefl = raw_input('root directory Deflection: ') # location of the zSensor data - preconverted to CSV



# rootdir = 'C:\Users\lebla\Downloads\4MarcAndre-20190118T110431Z-001\4MarcAndre\IgorPythonDemo\data\testzsensor'
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
    findSpikesandDwells(i)

#use this if you need to start analysis at a different point: typically used when some files are too large and throw memory errors
# count = 35
# while count <= len(ZandDeflPath_lst):
    # findSpikesandDwells(ZandDeflPath_lst[count])
    # count += 1
    




