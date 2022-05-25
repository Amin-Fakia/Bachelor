import matplotlib.pyplot as plt
import mne
import time
import os
import numpy as np
from matplotlib import collections as matcoll
from vedo import show, interactive,settings
from functions import *
from dsi_24_montage import ch_pos
dir_path = os.path.dirname(os.path.realpath(__file__))
settings.allowInteraction = True
filepath = "mainPy/edf_data/Data_02_raw.edf"
exclud_channels = ['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz']
headPath = f"{dir_path}/3dmodel/Head.obj"
raw = mne.io.read_raw_edf(filepath ,preload=True).drop_channels(exclud_channels)
raw.filter(7,12)
#raw.plot_psd()
mesh = get_mesh(headPath)
sensor_pts = get_sensor_3DLocations(ch_pos,["TRG","Pz"])
print(len(sensor_pts ))
#raw.plot()
data = raw.get_data()
print(raw.info['ch_names'][13][4:9])
O1 = data[13]
times = np.linspace(0,len(data[0])/300,len(data[0]))
xs = times[:300]
ys = O1[:300]
psd,freq = mne.time_frequency.psd_welch(raw)
vmax = max([max(i) for i in psd])
vmin = min([min(i) for i in psd])
psds = []
print(psd)
plt.show(block=False)
for i in range(32):
    plt.cla()
    psd,_ = mne.time_frequency.psd_welch(raw,tmin=i,tmax=i+1)
    plt.plot(freq,psd[13],label='O1-Fz')
    
    plt.ylim(vmin,vmax)
    plt.legend()
    plt.pause(0.7)
    #time.sleep(.5)



    






# plt.xlabel("Time (in s)")
# plt.ylabel("Voltage (in V)")
# plt.xticks(rotation=90) 


# for xc in range(len(xcoords)):
#     plt.axvline(x=xc,ymin=0, ymax=ynorm[xc], alpha=0.5,linewidth=0.3,c='r')
#plt.legend()
#plt.scatter(times[:300],O1[:300],c='b',linewidths=0.5)


# raw.filter(8,12)