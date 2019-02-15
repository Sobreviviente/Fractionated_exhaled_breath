# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 01:05:08 2019

@author: Carlos
"""

import numpy as np 
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update(
    {
        'text.usetex': False,
        'font.family': 'stixgeneral',
        'mathtext.fontset': 'stix',
    }
)

my_data = np.genfromtxt('dat_20190122.txt',delimiter = ',')

fig, ax = plt.subplots(figsize=(10,4))

print(my_data.shape)

time = my_data[:,0]
data1 = my_data[:,1]
data2 = my_data[:,2]

lista_promedio=[]
lista_tiempo_promedio=[]
def initVal():
    global maximo, minimo
    maximo = float(-2)
    minimo = float(4)


dd = np.zeros(data1.shape)
val = np.zeros(data1.shape)
dd[0] = data1[0]
alpha = 0.99
value = 0
value_2=0
puntos_estado=dd.copy()
ff = np.zeros(data1.shape)
puntos_del_filtro=[]
cuenta = 0
revisando = 0
estado_curva=0
step=0

def promedio(a,b):
    resultado = (a+b)/2
    return resultado 
    

for i in range(1,data2.size):
    muestra = data1[i]
    value = alpha * value + (1-alpha) * muestra
    val[i] = value    
    dd[i] = (val[i] - val[i-1])/((time[i]-time[i-1])/1000000.0)
    muestra_2 = dd[i]
    value_2=alpha*value_2+(1-alpha)*muestra_2
    ff[i]=value_2
    
    if (value > 1 and not revisando):
        revisando = True
        initVal()
        print(time[i])
    elif (value<=0.05 and revisando):
        lista_promedio.append(promedio(minimo,maximo))
        lista_tiempo_promedio.append(time[i])
        cuenta+=1
        print (cuenta)
        print (promedio(minimo,maximo))
        print (time[i])
        revisando = False
        
    if revisando:
        if (value<minimo):
            minimo=value
            
        elif (value>maximo):
            maximo=value
            
        #if (value_2<0.2):
        #    break
      
        ##PUNTOS DEL FILTRO 
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
        
       
        
print (lista_promedio)        
print(lista_tiempo_promedio)       
        
        
        
print(time.shape)
print(data1.shape)
ax.plot(time,data1,linewidth=3,alpha=0.8,label='Sensor ($CO_2$)')
#ax.plot(time,data2,label='Sensor signal2')
#ax.plot(time,dd,':',label='diff')
#ax.plot(time,val,':',label='filtro')
#ax.plot(puntos_x,puntos_y,'yo')
#ax.plot(time,ff,':',label='filtro_diff' )
index = np.where (puntos_estado != 0)
#ax.plot(time[index],puntos_estado[index],'o',label = 'Ref estados')

ind_c50 = []
ind_c50_3 = []

##Busqueda tiempo punto C50    
for i in range(1,data2.size):
    muestra = data1[i]
    value = alpha * value + (1-alpha) * muestra
    val[i] = value    
    dd[i] = (val[i] - val[i-1])/((time[i]-time[i-1])/1000000.0)
    muestra_2 = dd[i]
    value_2=alpha*value_2+(1-alpha)*muestra_2
    ff[i]=value_2 
    
    if (len(ind_c50) <= step and value>=lista_promedio[step]):
        ind_c50.append(i)
    if (step > 3 and len(ind_c50_3) <= step and value>=np.mean(lista_promedio[step-3:step])):
        ind_c50_3.append(i)
    if (time[i]==lista_tiempo_promedio[step]): 
       step+=1
       print (step) 
       if step>=len(lista_tiempo_promedio):
           break
       
for n in puntos_del_filtro:
    #print(n)
    index_t = np.where (time <= n)
    #print (index_t)
    if (n==puntos_del_filtro[0]):
        ax.plot(time[index_t[0][-1]],data1[index_t[0][-1]],'bo',alpha=.6, label='DM')        
    else:
        ax.plot(time[index_t[0][-1]],data1[index_t[0][-1]],'bo',alpha=.6)
#for p in ind_c50:
    #print(p)
    #index_p = np.where(time <= p)
    #print(index_p)
ax.plot(time[ind_c50],data1[ind_c50],'ro',label='C50',alpha=.6)     

ax.plot(time[ind_c50_3],data1[ind_c50_3],'go',label='$C50_3$',alpha=.6)        

ax.set_xlim((time[1],time[-1:]))
locs, labels = plt.xticks()
ax.set_xticklabels(locs/1000000)

ax.set_ylabel('Amplitude',fontsize=12)
ax.set_xlabel('Time [s]',fontsize=12)
ax.set_title('Detection of Dead Space and Alveolar air separation',fontweight="bold",fontsize=14)

chartBox = ax.get_position()
ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.9, chartBox.height])

ax.legend(loc='upper center', bbox_to_anchor=(1.13, .98), frameon = False)

        
#ax.legend(framealpha=0.7)      
        
plt.grid(linestyle='--',alpha=0.4)
plt.savefig('fig.pdf',bbox_inches='tight')
plt.show()