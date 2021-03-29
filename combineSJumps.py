# This program combines the individual .csv files and sorts them by the clamp force

import numpy 
from decimal import Decimal
import itertools
import csv
import os
import numpy
import re
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import os.path


# rootdir = raw_input('root directory: ') # location of the CSV files to be combined

#get the filepath for where the python script is run from
absFilePath = os.path.abspath(__file__)
print(absFilePath)
fileDir = os.path.dirname(os.path.abspath(__file__))
print(fileDir)

csv_list = []
for subdir, dirs, files in os.walk(fileDir):
    for file in files:
        #print os.path.join(subdir, file)
        # filepath = subdir + os.sep + file
        filepath = file
        if filepath.endswith("SJumps.csv"):
             csv_list.append(filepath)

# with open('output_file.csv', 'w') as outfile:
    # for fname in csv_list:
        # with open(fname) as infile:
            # outfile.write(fname)
            # outfile.write('\n')
            # outfile.write(infile.read())
            # outfile.write('\n')

# outfile_100 = open('combined_100.csv', 'w')
# outfile_200 = open('combined_200.csv', 'w')
# outfile_400 = open('combined_400.csv', 'w')
# outfile_800 = open('combined_800.csv', 'w')
# outfile_1600 = open('combined_1600.csv', 'w')
# outfile_3200_6400 = open('combined_3200_6400.csv', 'w')

#make a list of all unique velocities across all files
force_list = []
unique_list = []
str_unique_list = []
for fname in csv_list:
    with open(fname) as infile:
        reader = csv.reader(infile)
        templist = list(reader)
        force = float(templist[0][3])
        force_list.append(force)  

for vel in force_list:
    if vel not in unique_list:
        unique_list.append(vel)
        
print unique_list

    
Headers = ['Time (s)', "Extension (nm)", "Delta (nm)", "Force (N)"]

for vel in unique_list:
    force_pn_ = int(vel*1E12)
    str_vel = str(force_pn_)
    filename = "combined_"+str_vel+"pN_clamps.csv"
    with open(filename, 'w') as file:
        dw = csv.DictWriter(file, fieldnames=Headers)
        dw.writeheader()
    
    outfile = open(filename, "a")
    
    for fname in csv_list:
        with open(fname) as infile:
            reader = csv.reader(infile)
            templist = list(reader)
            force = float(templist[0][3])
            # print force
            
            if force == vel:
                with open(fname) as infile:
                    outfile.write(fname)
                    outfile.write('\n')
                    outfile.write(infile.read())
                    outfile.write('\n')
                    


# count=0
# for val in unique_list:
    # string_val = str(val)
    # file_variable = "outfile_"+string_val
    
    # filename = open(filename, 'w')
    
    



        