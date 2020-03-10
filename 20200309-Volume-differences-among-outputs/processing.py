

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import csv
import datetime

file = 'meseta' #'meseta' 'c50'

# Reading data
####################
print("Reading data ... "),
time = []
fdata = []
vdata = []
pastTime = ''

with open('ebc-'+file+'.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[0] != pastTime:
            pastTime = row[0]
            t = datetime.datetime.strptime(pastTime, "%H:%M:%S,%f")
            t = t - datetime.datetime(1900, 1, 1)
            t = t.total_seconds()
            print t
        time.append(t)
        fdata.append(float(row[1]))
        vdata.append(float(row[2]))


fdata = [i if i>0.2 else 0.0 for i in fdata]
vdata = [i if i>=0.0 else 0.0 for i in vdata]
plt.plot(time,fdata,label='alveolar')
plt.plot(time,vdata,label='dead-space')
plt.legend()
plt.show()
        