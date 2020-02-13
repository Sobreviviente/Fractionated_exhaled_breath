# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:37:11 2020

@author: Carlos
"""




import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import csv
import datetime

nFile = '-2'

# Utilities
####################
def separateSeconds(time):
    rep = 0.0
    base = time[0]
    items = time.count(base)

    for t in range(1,len(time)): 
        if time[t]!=base:
            base = time[t]
            items = time.count(base)
            rep = 1.0
        else:
            time[t] += rep*(1.0/items)
            rep += 1.0

def handle_close(evt):
    print('Closed Figure!')
    exit(0)

# Reading Trigger data
####################
trigger_time = []
trigger_data = []
pastTime = ''

with open('trigger'+nFile+'.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[0] != pastTime:
            pastTime = row[0]
            t = datetime.datetime.strptime(pastTime, "%H:%M:%S")
            t = t - datetime.datetime(1900, 1, 1)
            t = t.total_seconds()
        trigger_time.append(t)
        trigger_data.append(float(row[1]))
        
separateSeconds(trigger_time)

trigger_data = np.array(trigger_data)
trigger_time = np.array(trigger_time)
triggPos = np.argmax(trigger_data>0)
start = trigger_time[triggPos]
print triggPos
print start

# Reading CO2 data
####################
co2_time = []
co2_data = []
pastTime = ''
r = 0
with open('co2'+nFile+'.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        r += 1
        if row[0] != pastTime:
            pastTime = row[0]
            t = datetime.datetime.strptime(pastTime, "%H:%M:%S")
            t = t - datetime.datetime(1900, 1, 1)
            t = t.total_seconds()
        co2_time.append(t)
        co2_data.append(float(row[1]))

separateSeconds(co2_time)
co2_time = np.array(co2_time)
print co2_time[0]
co2TimePos = np.arange(np.argmax(co2_time>=start))
startCo2 = np.argmax(co2_time>=start)
co2_time = co2_time[startCo2:]- co2_time[startCo2]
co2_data = co2_data[startCo2:]

# Reading Spirometer data
####################

spi_all = np.genfromtxt('registro-para-co2'+nFile+'.txt', delimiter='\t')

subsample = 50

spi_time = spi_all[::subsample,0]
spi_flow = spi_all[::subsample,1]
spi_vol  = spi_all[::subsample,2]

#spi_flow += -1
#spi_flow.clip(min=0)

fig, ax = plt.subplots()

ax.plot(spi_time,spi_flow,'.r',label='Flow',alpha=0.5)
ax.plot(spi_time,spi_vol,'.g',label='Vol',alpha=0.5)
ax.plot(co2_time[::subsample],co2_data[::subsample],'.b',label='CO_2',alpha=0.5)
current_xticks = ax.get_xticklabels()
newTicks = []
plt.show(block=False)
plt.pause(1)

# for xtick in current_xticks:
#     x,y = xtick.get_position()
#     txt = xtick.get_text()
#     if txt == '':
#         tPos = 0
#     else:
#         txt = txt.replace(u"\u2212", "-")
#         print float(str(txt))
#         tPos = sum(i < float(txt) for i in spi_time) - 1
#     txt = text(x,y,str(spi_vol[tPos]),visible=False)
#     newTicks.append(txt)
# 
# ax.set_xticklabels(newTicks)
ax.legend()

plt.grid()

plt.savefig('c50-flow'+nFile+'.png')
plt.savefig('c50-flow'+nFile+'.pdf')

while True:
    plt.waitforbuttonpress()