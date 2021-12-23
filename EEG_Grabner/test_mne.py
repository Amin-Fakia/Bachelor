# import the libraries

import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from vedo import show, interactive
from functions import *
from dsi_24_montage import ch_pos

raw = mne.io.read_raw_edf("Data_01_filtered_01_30.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
raw.filter(9,11)

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
    print(ln)
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
        ax[1].set_ylim((0,2e-6))
        ax[1].plot(frequency,ps)
        plt.draw()
        min_win +=step
        max_win +=step
        return ln,

    def play(event):
        
        plt.show()
        
    
    
    ax[0].plot(times,data)
    ax[0].legend(["EEG O1"])
    ani = FuncAnimation(fig, update, interval=10,
                    init_func=init, blit=True)
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
        
        
    
    


data = raw.get_data()





#O1 = data[10]
#plot_window(O1,300,3,0.1)


dota = get_power_values(data,300,3,1,(len(data[0])/300))

dota = dota.tolist()
dota = [d for d in dota[:len(dota)-1]] # exclude TRG channel
# with open("output.txt", "w") as txt_file:

#     txt_file.write(str(dota)) # works with any number of elements in a line



# dete = [[0]*len(dota[0])] * len(dota)
# dete[13] = [d for d in dota[13]]
# dete[14] = [d for d in dota[14]]



# TODO: delete this
s_obj = "Head.obj"
sensor_pts = get_sensor_3DLocations(ch_pos)
mesh = get_mesh(s_obj)
pts = findVert(sensor_pts,mesh)
t1,t2 = 0,len(dota[0])

plot = show(interactive=False,bg='k')
vmin = min([min(i[t1:t2]) for i in dota])
    #[t1:t2]
vmax = max([max(i[t1:t2]) for i in dota])
for i in range(t1,t2):
    print(i)
    intpr = RBF_Interpolation(mesh,pts,[j[i] for j in dota])
    mesh.cmap('jet', intpr, vmin=vmin, vmax=vmax)
    plot.show(mesh)
    time.sleep(0.2)
plot.close()
    






