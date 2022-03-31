# import the libraries

import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from vedo import show, interactive
from functions import *
from dsi_24_montage import ch_pos
import scipy
from scipy.signal import savgol_filter
import easygui

edf_file= easygui.fileopenbox()
# Data_02_raw.edf

head = "./3dmodel/Head.obj"
raw = mne.io.read_raw_edf(edf_file ,preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
raw.filter(8,12)
raw.plot(duration=100)
fig, ax = plt.subplots(2)
def get_times(raw):
    df = raw.to_data_frame()
    return df.iloc[:,0]

def plot_window(data,sampling_rate,win_size,step):
    times = [i*(1/sampling_rate) for i in range(len(data))]
    ft = np.abs(np.fft.rfft(data))
    
    ps = np.square(ft)
    frequency = np.linspace(0, sampling_rate/2, len(ps))
    aspan_list = []
    min_win = 0
    max_win = win_size
    ln, = ax[1].plot(frequency, ps)
    
    def nxt(event):
        nonlocal max_win
        nonlocal min_win
        ax[1].cla()
        aspan_list.append(ax[0].axvspan(min_win,max_win, color='red',alpha=0.2))
        
        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        
        ft = np.abs(np.fft.rfft(data[pos_x1:pos_x2]))
        ps = np.square(ft)
        frequency = np.linspace(0, sampling_rate/2, len(ps))
        
        ax[1].set_ylim((0,10e-6))
        ax[1].plot(frequency, ps,color='red')
        
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
        aspan_list.append(ax[0].axvspan(min_win,max_win, color='red',alpha=0.2))
        
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
    ax[0].legend(["EEG O1"])
    axnext = plt.axes([0.88, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(nxt)
    
    plt.show()

    
def get_power_values(data,sampling_rate,win_size,step,itr):
    
    min_win = 0
    max_win = win_size
    data_array = []
    while(max_win < itr):
        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        
        sums = []
        
        for d in data:
            ft = np.abs(np.fft.rfft(d[pos_x1:pos_x2]))
            ps = np.square(ft)
            
            sums.append(sum(ps))
        
        data_array.append(sums)
        min_win +=step
        max_win +=step
    return np.transpose(data_array)
        
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
erp_data = get_ERP_values(data,300,3,1,(len(data[0])/300))




O1 = data[13]
plot_window(O1,300,3,1)


dota = get_power_values(data,300,3,0.3,(len(data[0])/300))

dota = dota.tolist()
dota = [d for d in dota[:len(dota)-1]] # exclude TRG channel
dota_smooth = []
for d in dota:
    dota_smooth.append(savgol_filter(d, 71, 3))
plot_data(dota[13])    
dota = dota_smooth

from dsi_24_montage import chnls
plot_data(dota[13])
# with open("output.txt", "w") as txt_file:

#     txt_file.write(str(dota)) # works with any number of elements in a line



# dete = [[0]*len(dota[0])] * len(dota)
# dete[13] = [d for d in dota[13]]
# dete[14] = [d for d in dota[14]]



# TODO: delete this


#slider

mesh = get_mesh(head)
t1,t2 = 0,len(dota[0])
vmin = min([min(i[t1:t2]) for i in dota])
vmax = max([max(i[t1:t2]) for i in dota])
sensor_pts = get_sensor_3DLocations(ch_pos)
intpr = RBF_Interpolation(mesh,sensor_pts,[j[0] for j in dota])
mesh.cmap('jet', intpr, vmin=-vmax, vmax=vmax).addScalarBar(pos=(0.8,0.3))
def slider1(widget, event):
    value = int(widget.GetRepresentation().GetValue())
    
    intpr = RBF_Interpolation(mesh,sensor_pts,[j[value] for j in dota])
    mesh.cmap('jet', intpr, vmin=-vmax, vmax=vmax)
def buttonfunc():
    
    if(bu.statusIdx == 0):
        bu.switch()
        txt = Text2D("Starting Animation",c='r')
        
        plot.show(txt,mesh,interactive=False)
        for i in range(t1,t2):
            if(bu.statusIdx ==0):
                bu.switch()
                break
            txt2= Text2D(f"{i}",pos="top-right")
            
            intpr = RBF_Interpolation(mesh,sensor_pts,[j[i] for j in dota])
            mesh.cmap('jet', intpr, vmin=-vmax, vmax=vmax)
            plot.show(mesh,txt2)
            time.sleep(1/20)
            plot.remove(txt2)
            
        
        plot.remove(txt)

    bu.switch()
    plot.render()
def save_btn():
    
    
    for i in range(len(dota[0])):
        rb = RBF_Interpolation(mesh,sensor_pts,[j[i] for j in dota])
        mesh.addQuality().cmap('jet', input_array=rb,arrayName="Quality", on="points", vmin=-vmax, vmax=vmax)
        mesh.write(f"ply_data\\EEG_{i}.ply")
    sv_btn.switch()
    
    

plot = Plotter(axes=0)
sl = plot.addSlider2D(slider1, 0, len(dota[0])-1, value=0,
               pos="bottom-right", title="Window Number",c='k')
#scl = mesh.addScalarBar(pos=(0.8,0.15))
bu = plot.addButton(
    buttonfunc,
    pos=(0.1, 0.05),  # x,y fraction from bottom left corner
    states=["Play", "Stop"],
    c=["w", "w"],
    bc=["dg", "dv"],  # colors of states
    font="courier",   # arial, courier, times
    size=25,
    bold=True,
    italic=False,
)
sv_btn = plot.addButton(
    save_btn,
    pos=(0.2, 0.05),  # x,y fraction from bottom left corner
    states=["Save","Saved"],
    c=["w","w"],
    bc=["dg", "dr"],  # colors of states
    font="courier",   # arial, courier, times
    size=25,
    bold=True,
    italic=False,
)
txt1 = Text2D(f"{((len(data[0])/300)/len(dota[0]))}",pos="bottom-left",c='w')
plot.show(mesh,txt1,bg='w')
plot.close()








