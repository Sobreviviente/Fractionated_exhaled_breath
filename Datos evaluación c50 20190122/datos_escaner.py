# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import numpy as np
import matplotlib.pyplot as plt

## Datos obtenidos 
##datos = open("datos_escaner.txt","r")

my_data = np.genfromtxt('datos_escaner.txt', delimiter=',')


fig, ax = plt.subplots()

print(my_data.shape)

time = my_data[:,2]
data1 = my_data[:,3]
data2 = my_data[:,4]

dd = np.zeros(data1.shape)
val = np.zeros(data1.shape)
dd[0] = data1[0]
alpha = 0.999
value = 0
for i in range(1,data2.size):
    dd[i] = data1[i] - data1[i-1]
    muestra = data1[i]
    value = alpha * muestra + (1-alpha) * value
    val[i] = value    
    print (i)
print(time.shape)
print(data1.shape)
ax.plot(time,data1,label='Sensor signal1')
ax.plot(time,data2,label='Sensor signal2')
ax.plot(time,dd,':',label='diff')
ax.plot(time,val,':',label='filtro')

##ax.set_ylim(0,maxV+1)
ax.legend(framealpha=0.4)

plt.show()