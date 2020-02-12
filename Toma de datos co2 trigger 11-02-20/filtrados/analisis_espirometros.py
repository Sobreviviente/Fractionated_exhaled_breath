# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:37:11 2020

@author: Carlos
"""



import numpy as np 
import matplotlib.pyplot as plt


#my_data = np.genfromtxt('datos_espirometro_pieza_lilly.txt', delimiter='\t')

time = []
data = []
import csv
counter = 0
pastTime = ''

conta_repeticion = 0 

marca_temporal = 1 



with open('datos_espirometro_pieza_lilly.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if row[0] != pastTime:
            counter += 1
            pastTime = row[0]
        time.append(counter)
        data.append([float(i) for i in row[1].split(',')])
        
        #print(time[-1],':',data[-1])

items = time.count(time[0])
conta_repeticion = 0
base = time[0]

for t in range(1,len(time)): 
    # print(time[t],conta_repeticion)
    if time[t]!=base:
        base = time[t]
        items = time.count(time[t])
        conta_repeticion = 0
    else:
        conta_repeticion += 1
        time[t] += conta_repeticion*1/items
    #print(time[t])

fig, ax = plt.subplots()

#plt.plot(time,data)
lineObjects = plt.plot(time,data)
plt.legend(iter(lineObjects),('presion','volumen','flujo volumetrico','velocidad de flujo','trigger'))



plt.grid()
plt.show()

#print(my_data.shape)
#print(my_data)
#counter=0 