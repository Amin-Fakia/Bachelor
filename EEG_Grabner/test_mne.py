# import the libraries

import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.widgets import Button

raw = mne.io.read_raw_edf("Data_01_filtered_01_30.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])

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
    def nxt(event):
        nonlocal win_size
        nonlocal max_win
        nonlocal min_win
        ax[1].cla()
        aspan_list.append(ax[0].axvspan(min_win,max_win, color='red',alpha=0.2))
        
        pos_x1 = int((min_win)*sampling_rate)
        pos_x2 = int((max_win)*sampling_rate)
        
        ft = np.abs(np.fft.rfft(data[pos_x1:pos_x2]))
        ps = np.square(ft)
        frequency = np.linspace(0, sampling_rate/2, len(ps))
        ax[1].plot(frequency, ps,color='red')
        min_win +=step
        max_win +=step
        plt.draw()
        
    def get_freq_window():
        pass
        
        
    ax[1].plot(frequency, ps)
    
    ax[0].plot(times,data)
    ax[0].legend(["EEG O1"])

    axnext = plt.axes([0.88, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(nxt)

    plt.show()
    
    



data = raw.get_data()
O1 = data[13]


plot_window(O1,300,3,1)





# working function
    # def nxt(event):
    #     nonlocal win_size
    #     nonlocal idx
    #     ax[1].cla()
    #     aspan_list.append(ax[0].axvspan(min_win+win_size,max_win+win_size, color='red',alpha=0.2))
        
    #     pos_x1 = int((win_size)*sampling_rate)
    #     pos_x2 = int((win_size+step)*sampling_rate)
        
    #     ft = np.abs(np.fft.rfft(data[pos_x1:pos_x2]))
    #     ps = np.square(ft)
    #     frequency = np.linspace(0, sampling_rate/2, len(ps))
    #     ax[1].plot(frequency, ps,color='red')
    #     idx += 0.1
    #     win_size +=step
    #     plt.draw()