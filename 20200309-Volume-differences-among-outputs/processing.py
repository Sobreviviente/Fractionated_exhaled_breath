

import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
import csv
from collections import OrderedDict
import datetime
import sys
from os import makedirs, path

# Config
####################
file = 'c50' #'meseta' 'c50'
resultsAt = 'results/'

# Making results folder
####################
if not path.exists(resultsAt):
    makedirs(resultsAt)

# Utils
####################
def show_fullsize(filename,block=False):
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    if filename:
        figure = plt.gcf() # get current figure
        figure.set_size_inches(14, 7)
        plt.savefig(filename+'.pdf')
        plt.savefig(filename+'.png')
    plt.show(block = block)

# Reading data
####################
print("Reading data ... "),
time = []
fdata = []
vdata = []
pastTime = ''
dt = 0.01

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

# Filtering data
####################

modify = ('filter','shift','threshold')
if len(sys.argv)>1:
    modify = str(sys.argv[1:])

fdata_proc = fdata[:]
vdata_proc = vdata[:]

if 'filter' in modify:
    print("Filtering")
    alpha = 0.05
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

# Detecting breathings on both signals
# f: alveolar, v: dead-space
####################

starts_f = []
starts_v = []
fstate = 'searching'
vstate = 'searching'

if file == 'c50':
    threshold = 0.1
    threshold_up = 2.5*threshold
    threshold_down = 0.7*threshold
elif file == 'meseta':
    threshold = 0.06
    threshold_up = 0.091
    threshold_down = 0

for i in range(1,len(fdata)):
    if fstate == 'searching' and fdata_proc[i-1] < threshold and fdata_proc[i]>threshold:
        fstate = 'reading'
        starts_f.append(i)
    if fstate == 'reading':
        if fdata_proc[i] > threshold_up:
            fstate = 'safe'
        elif fdata_proc[i] <= threshold_down:
            starts_f.pop()
            fstate = 'searching'
    if fstate == 'safe':
        if fdata_proc[i] <= threshold_down:
            fstate = 'searching'

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

print "alveolar count:",len(starts_f)
print "dead-space count:",len(starts_v)

# Plotting 
####################

plt.subplot(221)
plt.title('Breathing data')
plt.plot(time,fdata,alpha=0.3,linewidth=3)
for p in starts_f:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.plot(time,fdata_proc,'b',label='alveolar')
# plt.plot(time[1:],np.diff(fdata_proc)/np.diff(time),alpha=0.3,linewidth=3)
plt.ylabel('Alveolar\nexhaled flow [L/s]')
plt.legend()
plt.subplot(223)
plt.plot(time,vdata,alpha=0.3,linewidth=3)
# plt.plot(time[1:],np.diff(vdata_proc)/np.diff(time),alpha=0.3,linewidth=3)
for p in starts_v:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.plot(time,vdata_proc,'orange',label='dead-space')
plt.xlabel('Time [s]')
plt.ylabel('Dead-space\nexhaled flow [L/s]')
plt.suptitle('Exhaled flow')
plt.legend()

plt.subplot(222)
plt.title('Smaller window')
plt.plot(time[:starts_f[10]],fdata_proc[:starts_f[10]],'b')
for p in starts_f[:10]:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.ylabel('[L/s]')
plt.subplot(224)
plt.plot(time[:starts_v[10]],vdata_proc[:starts_v[10]],'orange')
for p in starts_v[:10]:
    plt.plot(time[p],0,'ro',linewidth=2.5,alpha=0.6)
plt.xlabel('Time [s]')
plt.ylabel('[L/s]')

show_fullsize(resultsAt+file+'-flow')

# Calculating volumes and storing
####################

volumes_f = []
volumes_v = []
for i in range(len(starts_f)-1):
    volumes_f.append(dt * sum(fdata_proc[starts_f[i]:starts_f[i+1]]))
for i in range(len(starts_v)-1):
    volumes_v.append(dt * sum(vdata_proc[starts_v[i]:starts_v[i+1]]))

volumes_t = []
pos_v = 0
pos_f = 0

volume = OrderedDict([('start',0),('end',0),('volume',0),('start-alveolar',0),('end-alveolar',0),('volume-alveolar',0),('start-dead-space',0),('end-dead-space',0),('volume-dead-space',0)])

with open(resultsAt+'ebc-'+file+'-total.csv', 'wb') as outputfile:
    wtr = csv.DictWriter(outputfile, volume.keys(),delimiter=',')
    wtr.writeheader()
    while(pos_v < len(starts_v)-1):
        if ((pos_f < len(starts_f)-1 and starts_f[pos_f+1] > starts_v[pos_v+1] and starts_v[pos_v+1] > starts_f[pos_f] and starts_f[pos_f] > starts_v[pos_v]) or 
                (starts_v[pos_v+1] > starts_f[pos_f] and starts_f[pos_f] > starts_v[pos_v])):
            # Same breath
            volumes_t.append(volumes_f[pos_f]+volumes_v[pos_v])

            volume['start'] = time[starts_v[pos_v]]
            volume['end'] = time[starts_v[pos_v+1]]
            volume['volume'] = volumes_t[-1]
            volume['start-alveolar'] = time[starts_f[pos_f]]
            volume['end-alveolar'] = time[starts_f[pos_f+1]]
            volume['volume-alveolar'] = volumes_f[pos_f]
            volume['start-dead-space'] = time[starts_v[pos_v]]
            volume['end-dead-space'] = time[starts_v[pos_v+1]]
            volume['volume-dead-space'] = volumes_v[pos_v]
            wtr.writerow(volume)

            pos_v += 1
            pos_f += 1
            continue
        if starts_v[pos_v+1] < starts_f[pos_f]:
            print "Jumping dead-space position at:",time[starts_v[pos_v]]
            pos_v += 1
            continue
        if starts_f[pos_f] <= starts_v[pos_v]:
            print "Jumping alveolar position at:",time[starts_f[pos_f]]
            pos_f += 1
            continue
        print "other case :(",time[starts_v[pos_v]],time[starts_f[pos_f]]


volume = OrderedDict([('start',0),('end',0),('volume',0)])

with open(resultsAt+'ebc-'+file+'-alveolar.csv', 'wb') as outputfile:
    wtr = csv.DictWriter(outputfile, volume.keys(),delimiter=',')
    wtr.writeheader()
    for i in range(len(starts_f)-1):
        volume['start'] = time[starts_f[i]]
        volume['end'] = time[starts_f[i+1]]
        volume['volume'] = volumes_f[i]
        wtr.writerow(volume)

with open(resultsAt+'ebc-'+file+'-dead-space.csv', 'wb') as outputfile:
    wtr = csv.DictWriter(outputfile, volume.keys(),delimiter=',')
    wtr.writeheader()
    for i in range(len(starts_v)-1):
        volume['start'] = time[starts_v[i]]
        volume['end'] = time[starts_v[i+1]]
        volume['volume'] = volumes_v[i]
        wtr.writerow(volume)

# Plotting
####################

top = 2.4
bins = np.arange(0,top,0.05)
plt.subplot(211)
plt.plot(volumes_f,'*',label='alveolar')
plt.plot(volumes_v,'*',label='dead-space')
plt.plot(volumes_t,'*',label='total')
plt.ylabel('Volume per exhalation [L]')
plt.ylim([0.0,top])
plt.xlabel('Exhalation')
plt.legend()
plt.subplot(212)
plt.hist(volumes_f,bins,label='alveolar',alpha=0.4)
plt.hist(volumes_v,bins,label='dead-space',alpha=0.4)
plt.hist(volumes_t,bins,label='total',alpha=0.4)
plt.xlabel('Volume [L]')
plt.ylabel('Counts')
plt.suptitle('Exhaled volumes')
plt.legend()
show_fullsize(resultsAt+file+'-volumes')