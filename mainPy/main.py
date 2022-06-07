# import the libraries

import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from vedo import show, interactive,settings
from functions import *
from dsi_24_montage import ch_pos
#from dsi24_montage import ch_pos
import scipy
from scipy.signal import savgol_filter
import easygui
import os 
settings.allowInteraction = 1
dir_path = os.path.dirname(os.path.realpath(__file__))
#plt.style.use('dark_background')
#edf_file= easygui.fileopenbox()
edf_file= f"{dir_path}/edf_data/Data_04_raw.edf"
# Data_02_raw.edf
headPath = f"{dir_path}/3dmodel/Head.obj"
plot = Plotter(axes=0)
exc_chnls=['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz','Trigger','EEG A1-Pz','EEG A2-Pz']
raw = mne.io.read_raw_edf(edf_file ,preload=True).drop_channels(exc_chnls)
raw.filter(8,12)
# raw.plot(duration=100)
#fig, ax = plt.subplots(2)

def get_times(raw):
    df = raw.to_data_frame()
    return df.iloc[:,0]
def plot_window(data,sampling_rate,win_size,step):
    times = [i*(1/sampling_rate) for i in range(len(data))]
    ft = np.abs(np.fft.rfft(data))
    
    ps = np.square(ft)
    frequency = np.linspace(0, sampling_rate/2, len(ps))
    aspan_list = []
    
    ax[0].axvspan(0,times[int(len(times)/3)], color='red',alpha=0.2)
    ax[0].axvspan(times[int(len(times)/3)],times[int(len(times)/1.1)], color='green',alpha=0.2)
    ax[0].axvspan(times[int(len(times)/1.1)],times[int(len(times))-1], color='red',alpha=0.2)
    min_win = 0
    max_win = win_size
    ln, = ax[1].plot(frequency, ft)
    
    def nxt(event):
        nonlocal max_win
        nonlocal min_win
        ax[0].cla()
        ax[1].cla()
        #aspan_list.append(ax[0].axvspan(min_win,max_win, color='red',alpha=0.2))
        #ax[0].axvspan(min_win,max_win, color='yellow',alpha=0.2)
        ax[0].axvspan(min_win,max_win, color='red',alpha=0.2)

        ax[0].plot(times,data)
        ax[0].set_xlabel("time in s")
        ax[0].set_ylabel("Amplitude in V")
        ax[0].legend(["EEG O1"])

        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        
        ft = np.abs(np.fft.rfft(data[pos_x1:pos_x2]))
        #ps = np.square(ft)
        frequency = np.linspace(0, sampling_rate/2, len(ft))
        #frequency = np.linspace(pos_x1, pos_x2, len(ft))
        ax[1].set_ylim((0,10e-3))
        ax[1].plot(frequency, ft,color='red')
        
        #ax[1].set_xlim((0,len(data)))
        ax[1].set_ylabel("Intensity (arb. u.)")
        ax[1].set_xlabel("Frequency in Hz")
        
        min_win +=step
        max_win +=step
        
        plt.draw()
        
    def init():
        ax[1].set_ylim((0,10e-7))
        return ln,    
    def update(frame):
        ax[1].cla()
        nonlocal max_win
        nonlocal min_win
        #aspan_list.append(ax[0].axvspan(min_win,max_win, color='red',alpha=0.2))
        #ax[0].axvspan(min_win,max_win, color='yellow',alpha=0.2)
        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        
        ft = np.abs(np.fft.rfft(data[pos_x1:pos_x2]))
        ps = np.square(ft)
        frequency = np.linspace(0, sampling_rate/2, len(ps))
        ax[1].set_ylim((0,7e-6))
        ax[1].plot(frequency,ps)
        plt.draw()
        min_win +=step
        max_win +=step
        return ln,

    def play(event):
        
        plt.show()
    
    ax[0].plot(times,data)
    ax[0].set_xlabel("time in s")
    ax[0].set_ylabel("Amplitude in V")
    ax[0].legend(["Time Window"])

    # axnext = plt.axes([0.88, 0.05, 0.1, 0.075])
    # bnext = Button(axnext, 'Next')
    # bnext.on_clicked(nxt)
    
    plt.show()

    
# def get_power_values(data,sampling_rate,win_size,step,itr):
    
#     min_win = 0
#     max_win = win_size
#     data_array = []
#     while(max_win < itr):
#         pos_x1 = int((min_win)*sampling_rate)
#         pos_x2 = int((max_win)*sampling_rate)
        
#         sums = []
        
#         for d in data:
#             ft = np.abs(np.fft.rfft(d[pos_x1:pos_x2]))
#             #ps = np.square(ft)
            
#             sums.append(sum(ft))
        
#         data_array.append(sums)
#         min_win +=step
#         max_win +=step
#     return np.transpose(data_array)
        
def get_ERP_values(data,sampling_rate,win_size,step,itr):
    min_win = 0
    max_win = win_size
    data_array = []
    while(max_win < itr):
        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        sums = []
        for d in data:
            sums.append(sum(d[pos_x1:pos_x2]))
        data_array.append(sums)
        min_win +=step
        max_win +=step
    return np.transpose(data_array)      
    
    


data = raw.get_data()
print(len(data))
erp_data = get_ERP_values(data,300,3,1,(len(data[0])/300))




O1 = data[13]
#plot_window(O1,300,3,0.1)
#plot_window_with_ax(O1,300,2,(1/300)*2,event_time=15.5,tmin=13,tmax=20)

data = raw.get_data(start=11*300,stop=21*300)
dota = get_power_values(data,300,3,(1/300)*20)
print(len(data[0]))
print(len(dota[0]))
dota = dota.tolist()
dota = [d for d in dota[:len(dota)]] # exclude TRG channel
dota_smooth = []
for d in dota:
    dota_smooth.append(savgol_filter(d, 71, 3))
#plot_data(dota[13])    
dota = dota_smooth

from dsi_24_montage import chnls
#plot_data(dota[13])
from matplotlib.colors import ListedColormap
from matplotlib import cm
mesh = get_mesh(headPath)
t1,t2 = 0,len(dota[0])
vmin = min([min(i[t1:t2]) for i in dota])
vmax = max([max(i[t1:t2]) for i in dota])
print([j[0] for j in dota])
sensor_pts = get_sensor_3DLocations(ch_pos,["TRG","Pz","A1","A2"])
print(len(sensor_pts))
print(len(dota))

intpr = RBF_Interpolation(mesh,sensor_pts,[j[0] for j in dota])
shade_n = 20
jett = cm.get_cmap('YlOrRd')
# white = np.array([255/256, 255/256, 255/256, 1])
# newcolors = jett(np.linspace(0, 1, shade_n))
# newcolors[:1] = white
# jett = ListedColormap(newcolors)
mesh.addQuality().cmap(jett, input_array=intpr,arrayName="Quality", on="points", vmin=vmin, vmax=vmax).addScalarBar(pos=(0.8,0.3))
mesh.write("test.obj")
pts = Points(sensor_pts,r=9)
txts = []
i = 0
for pt in sensor_pts:
    txt = Text3D(f"{chnls[i][4:6]}",pt,s=0.006,c='k')
    txt.followCamera()
    txts.append(txt)
    i+=1
            
def slider1(widget, event):
    value = int(widget.GetRepresentation().GetValue())
    
    intpr = RBF_Interpolation(mesh,sensor_pts,[j[value] for j in dota],'gaussian')
    mesh.cmap(jett, intpr, vmin=vmin, vmax=vmax)
    
def buttonfunc():
    
    if(bu.statusIdx == 0):
        bu.switch()
        txt = Text2D("Starting Animation",c='r')
        
        #plot.show(txt,mesh,interactive=False)
        for i in range(t1,t2):
            if(bu.statusIdx ==0):
                bu.switch()
                break
            txt2= Text2D(f"{i}",pos="top-right")
            
            intpr = RBF_Interpolation(mesh,sensor_pts,[j[i] for j in dota])
            mesh.cmap('jet', intpr, vmin=-vmax, vmax=vmax)
            plot.show(mesh,txt2,txt,interactive=False)
            
            sl.GetRepresentation().SetValue(i)
            plot.remove(txt2)
            plot.remove(txt)
          
        plot.remove(txt)
        plot.render()
    bu.switch()
    
    
        
    
import json
def save_btn():
    
    test = {}
    for i in range(len(dota[0])):
        rb = RBF_Interpolation(mesh,sensor_pts,[j[i] for j in dota])
        mesh.addQuality().cmap('jet', input_array=rb,arrayName="Quality", on="points", vmin=-vmax, vmax=vmax)
        rgb_c = getRGB(mesh).tolist()
        test[f"{i}"] = rgb_c
        # with open('json_data.txt', 'w') as outfile:
        #     json.dump({f"{i}":rgb_c}, outfile)
        #mesh.write(f"ply_data\\EEG_{i}.ply")
    print(i)
    #mesh.write(f"ply_data\\EEG_{i}.ply")
    sv_btn.switch()
    
    
def get_moveAverage(data):
    moving_averages = []
    data = np.transpose(data)
    i=0
    for d in data:
        moving_averages.append(sum(d)/len(d))
        
        # while i < len(d) - win_size + 1:
        #     this_window = d[i : i + win_size]
        #     window_average = sum(this_window) / win_size
        #     moving_averages.append(window_average)
        #     i += 1
    return np.transpose(moving_averages)

# import pandas as pd

# dataFrame = pd.DataFrame(np.transpose(dota))
# print(dataFrame.iloc[:600].sum(axis=1))


avgs = get_moveAverage(dota)
 
#data_smooth = savgol_filter(avgs, 31, 3)

animate_vline(avgs,41)

#plot = Plotter(axes=0)
# sl = plot.addSlider2D(slider1, 0, len(dota[0])-1, value=0,
#                pos="bottom-right", title="Window Number",c='k')
#scl = mesh.addScalarBar(pos=(0.8,0.15))
# bu = plot.addButton(
#     buttonfunc,
#     pos=(0.1, 0.05),  # x,y fraction from bottom left corner
#     states=["Play", "Stop"],
#     c=["w", "w"],
#     bc=["dg", "dv"],  # colors of states
#     font="courier",   # arial, courier, times
#     size=25,
#     bold=True,
#     italic=False,
# )
# sv_btn = plot.addButton(
#     save_btn,
#     pos=(0.2, 0.05),  # x,y fraction from bottom left corner
#     states=["Save","Saved"],
#     c=["w","w"],
#     bc=["dg", "dr"],  # colors of states
#     font="courier",   # arial, courier, times
#     size=25,
#     bold=True,
#     italic=False,
# )

# txt1 = Text2D(f"{((len(data[0])/300)/len(dota[0]))}",pos="bottom-left",c='w')
# #plt.screenshot("mypic.png")

txt2= Text2D(f"{0}",pos="top-right")
intpr = RBF_Interpolation(mesh,sensor_pts,[j[50] for j in dota])
mesh.addQuality().cmap(jett, input_array=intpr,arrayName="Quality", on="points", vmin=vmin, vmax=vmax).addScalarBar(pos=(0.8,0.3))
mesh.write('test.stl')
plot.show(mesh,txt2 ,bg='w',viewup='z',interactive=False)
# time.sleep(10)

# for i in range(t1,t2):
    
#     txt2.text(f"{i}")
    
#     intpr = RBF_Interpolation(mesh,sensor_pts,[j[i] for j in dota])
#     mesh.cmap(jett, intpr, vmin=vmin, vmax=vmax)
#     plot.show(mesh,*txts,pts,txt2,interactive=False)
    
#     #sl.GetRepresentation().SetValue(i)
#     plot.render()
#     plot.screenshot(f"{dir_path}/vedoVideo/{i}.png")
    


# plot.show(mesh,txt1 ,bg='w',viewup='z')
# plot.close()








