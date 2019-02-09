# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
import numpy as np
import matplotlib.pyplot as plt

## Datos obtenidos 
##datos = open("datos_escaner.txt","r")

my_data = np.genfromtxt('dat_20190122.txt', delimiter=',')


fig, ax = plt.subplots()

print(my_data.shape)

t=0
estado_curva = 0 
time = my_data[:,0]
data1 = my_data[:,1]
data2 = my_data[:,2]

puntos_sujeto_1 = [(  1.06108*10**7,1.64925*10**7,2.07002*10**7,2.57464*10**7,3.06846*10**7),(3.635853,2.796659,2.832604,2.691077,2.694828)]
puntos_traslado_1 =[(150000 + 1.06108*10**7,150000+1.64925*10**7,150000+2.07002*10**7,150000+2.57464*10**7,150000+3.06846*10**7),(3.635853,2.796659,2.832604,2.691077,2.694828)]
puntos_del_filtro=[]
puntos_x = puntos_sujeto_1[0]
puntos_y = puntos_sujeto_1[1]
puntos_traslado_x = puntos_traslado_1[0]
puntos_traslado_y = puntos_traslado_1[1]
#puntos_prueba=[150904, 186827, 241686, 285501, 327939, 372910, 415944, 456669, 496717, 536898, 585990, 618449, 621574, 635106, 676321, 722500, 767374, 810954, 852340, 890045, 924166, 964979, 984141]

dd = np.zeros(data1.shape)
val = np.zeros(data1.shape)
dd[0] = data1[0]
alpha = 0.99
value = 0
value_2=0
puntos_estado=dd.copy()
ff = np.zeros(data1.shape)


for i in range(1,data2.size):
    muestra = data1[i]
    value = alpha * value + (1-alpha) * muestra
    val[i] = value    
    dd[i] = (val[i] - val[i-1])/((time[i]-time[i-1])/1000000.0)
    muestra_2 = dd[i]
    value_2=alpha*value_2+(1-alpha)*muestra_2
    ff[i]=value_2
    
    if (estado_curva==0 and ff[i] > 3.0): #pulso aviso curva en subida
       # print (ff[i])
        estado_curva = 1  #cambio de estado 
        puntos_estado[i]=100
        #if (ff[i]==3.0):
        #puntos_del_filtro.append(ff[i])
            
    elif (estado_curva==1 and ff[i]<0.5): #trigger 
        puntos_estado[i]=200
        estado_curva = 2    #cambio de estado 
        t=time[i]+150000   #punto de disparo encontrar en curva 
        #print (t)
        puntos_del_filtro.append(t)
        #print('hola '+str(t))
    
    elif (estado_curva==2 and (time[i]>t)):     #Activar salidas 
        estado_curva=3
        puntos_estado[i]=300
    
    elif (estado_curva==3 and data1[i]<0.05): #resetear todo 
        estado_curva = 0 
        puntos_estado[i]=50
        t=0
        #print (puntos_del_filtro)
        #print (len(puntos_del_filtro))
    
print(time.shape)
print(data1.shape)
ax.plot(time,data1,label='Sensor signal1')
ax.plot(time,data2,label='Sensor signal2')
ax.plot(time,dd,':',label='diff')
ax.plot(time,val,':',label='filtro')
ax.plot(puntos_x,puntos_y,'yo')
ax.plot(time,ff,':',label='filtro_diff' )
index = np.where (puntos_estado != 0)
ax.plot(time[index],puntos_estado[index],'o',label = 'Ref estados')
#ax.plot(time)

##ax.set_ylim(0,maxV+1)

for j in puntos_traslado_x:   #GRAFICA PUNTOS EN CURVA 
    index= np.where (time <= j)
    #print (index)
    #print (index[0][-1]) 
    ax.plot(time[index[0][-1]],data1[index[0][-1]],'ro')

for n in puntos_del_filtro:
    print(n)
    index_t = np.where (time <= n)
    print (index_t)
    ax.plot(time[index_t[0][-1]],data1[index_t[0][-1]],'bo')

ax.legend(framealpha=0.4)

plt.grid()
plt.show()
plt.savefig('figura.pdf')