

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import csv
import datetime
import sys

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
        time.append(t)
        fdata.append(float(row[1]))
        vdata.append(float(row[2]))


modify = ('filter','shift','threshold')
if len(sys.argv)>1:
    modify = str(sys.argv[1:])

fdata_proc = fdata[:]
vdata_proc = vdata[:]

if 'filter' in modify:
    print("Filtering")
    alpha = 0.2
    for i in range(1,len(fdata)):
        fdata_proc[i] = fdata[i]*alpha + fdata_proc[i-1]*(1-alpha)
        vdata_proc[i] = vdata[i]*alpha + vdata_proc[i-1]*(1-alpha)
if 'shift' in modify:
    print("Shifting")
    fdata_proc = [i-0.2 for i in fdata_proc]
    vdata_proc = [i+0.1 for i in vdata_proc]
if 'threshold' in modify:
    print("Cutting-off")
    base = 2e-6
    fdata_proc = [i if i>=base else 0.0 for i in fdata_proc]
    vdata_proc = [i if i>=base else 0.0 for i in vdata_proc]

starts_f = []
starts_v = []
fstate = 'searching'
vstate = 'searching'

for i in range(1,len(fdata)):
    # print fstate,time[i],'\t',fdata_proc[i-1],'/',fdata_proc[i],'\t',
    if fstate == 'searching' and fdata_proc[i-1] == 0 and fdata_proc[i]>0:
        fstate = 'reading'
        starts_f.append(i)
    if fstate == 'reading':
        if fdata_proc[i] > 0.1:
            fstate = 'safe'
        elif fdata_proc[i] == 0:
            starts_f.pop()
            fstate = 'searching'
    if fstate == 'safe':
        if fdata_proc[i] == 0:
            fstate = 'searching'
    # print '->',fstate,


    # print '\t\t',vstate,time[i],'\t',vdata_proc[i-1],'/',vdata_proc[i],'\t',
    if vstate == 'searching' and vdata_proc[i-1] == 0 and vdata_proc[i]>0:
        vstate = 'reading'
        starts_v.append(i)
    if vstate == 'reading':
        if vdata_proc[i] > 0.1:
            vstate = 'safe'
        elif vdata_proc[i] == 0:
            starts_v.pop()
            vstate = 'searching'
    if vstate == 'safe':
        if vdata_proc[i] == 0:
            vstate = 'searching'
    # print '->',vstate

print "alveolar count:",len(starts_f)
print "dead-space count:",len(starts_v)

# utils
def show_fullsize(filename):
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    if filename:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(14, 7)
        plt.savefig(filename+'.pdf')
    plt.show()


plt.subplot(221)
plt.title('Complete registers')
plt.plot(time,fdata,alpha=0.3,linewidth=3)
for p in starts_f:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.plot(time,fdata_proc,'b',label='alveolar')
plt.ylabel('Alveolar\nexhaled flow')
#plt.xlabel('Time [s]')
plt.legend()
plt.subplot(223)
plt.plot(time,vdata,alpha=0.3,linewidth=3)
for p in starts_v:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.plot(time,vdata_proc,'orange',label='dead-space')
plt.xlabel('Time [s]')
plt.ylabel('Dead-space\nexhaled flow')
plt.suptitle('Exhaled flow')
plt.legend()

plt.subplot(222)
plt.title('Smaller window')
plt.plot(time[:starts_f[10]],fdata_proc[:starts_f[10]],'b')
for p in starts_f[:10]:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
#plt.xlabel('Time [s]')
plt.subplot(224)
plt.plot(time[:starts_v[10]],vdata_proc[:starts_v[10]],'orange')
for p in starts_v[:10]:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.xlabel('Time [s]')

show_fullsize('flow')

volumes_f = []
volumes_v = []
for i in range(len(starts_f)-1):
    volumes_f.append(sum(fdata_proc[starts_f[i]:starts_f[i+1]]))
for i in range(len(starts_v)-1):
    volumes_v.append(sum(vdata_proc[starts_v[i]:starts_v[i+1]]))

print volumes_f,volumes_v
bins = range(0,100,3)
plt.subplot(211)
plt.plot(volumes_f,'*',label='alveolar')
plt.plot(volumes_v,'*',label='dead-space')
plt.ylabel('Volume per exhalation')
plt.xlabel('Exhalation')
plt.legend()
plt.subplot(212)
plt.hist(volumes_f,bins,label='alveolar',alpha=0.4)
plt.hist(volumes_v,bins,label='dead-space',alpha=0.4)
plt.xlabel('Volume [L]')
plt.ylabel('Counts')
plt.suptitle('Exhaled volumes')
plt.legend()
show_fullsize('volumes')