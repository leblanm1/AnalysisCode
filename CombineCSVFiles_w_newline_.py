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


rootdir = raw_input('root directory: ') # location of the CSV files to be combined

csv_list = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        #print os.path.join(subdir, file)
        # filepath = subdir + os.sep + file
        filepath = file
        if filepath.endswith("WLCFit.csv"):
             csv_list.append(filepath)

with open('output_file.csv', 'w') as outfile:
    for fname in csv_list:
        with open(fname) as infile:
            outfile.write(fname)
            outfile.write('\n')
            outfile.write(infile.read())
            outfile.write('\n')
