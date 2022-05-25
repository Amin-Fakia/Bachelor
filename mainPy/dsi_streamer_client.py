import socket
from DSIStream import filter, DSI24_ByteStream_Decoder as dc
import numpy as np
import matplotlib.pyplot as pylot
import os
from dsi_24_montage import ch_pos
import time
from vedo import *

from functions import *
settings.allowInteraction = 1
dir_path = os.path.dirname(os.path.realpath(__file__))
headPath = f"{dir_path}/3dmodel/Head.obj"
sensor_pts = get_sensor_3DLocations(ch_pos,["TRG"])
mesh = get_mesh(headPath)
plot = Plotter(axes=0)


TCP_IP = "127.0.0.1"
TCP_PORT = 8844
BUFFER_SIZE = 5
y=np.array([])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("connected: ", s)

ftvalues = np.empty((20))
maxus = []
minus = []
def calcFFT(data):
    fftVal = []
    for d in data: # get every row
        ft = np.abs(np.fft.rfft(d))
        # ps = np.square(ft)
        fftVal.append(sum(ft))
    return fftVal

def get_data(data):
    return data
ix = 0
maxV = 0
# pylot.ion()
# fig, ax = plt.subplots()
xdata, ydata = [], []



# ln, = ax.plot([], [])
x,y = np.arange(101),[]
while True:

    
    data = s.recv(BUFFER_SIZE)
    #plot.show(mesh ,bg='w',interactive=0)
    #print("lol")
    if data == None:
        #plt.close()
        break


    if data == "@ABCD".encode():
        
        data += s.recv(BUFFER_SIZE)
        data += s.recv(dc.decodeBytes_packetLength(data))
        
        # if dc.decodeBytes_packetType(data) == 5:
            
        #     dc.printEventPacket(data)
        
        if dc.decodeBytes_packetType(data) == 1:
            #eeg_data = dc.printsensorDataPacket(data)
            
            y.append(dc.decodeBytes_ChData(data, offset=23+14*4, len=4))
            if ix>= 100 and ix % 5 == 0:
                psds = calcFFT(y)
                intpr = RBF_Interpolation(mesh,sensor_pts,psds,vmin=0)
                mesh.addQuality().cmap('jet', input_array=intpr,arrayName="Quality", on="points",vmin=0)
                show(mesh,interactive=False)
                # ln.set_xdata(range(len(y)))
                # ln.set_ydata(y)
                # ax.relim()
                # ax.autoscale_view()
                # fig.canvas.draw()
                # fig.canvas.flush_events()
                y =  y[5:]
            ix+=1
            
            #dt = np.array([e/10e6 for e in eeg_data[0:len(eeg_data)-4]],dtype=object).T
            
            
            #ftvalues = np.c_[ftvalues,dt]
            
            # norm = np.linalg.norm(eeg_data[0:len(eeg_data)-4])
            # normal_array = eeg_data[0:len(eeg_data)-4]/norm
            # # calcVals = calcFFT(ftvalues)
            # intpr = RBF_Interpolation(mesh,sensor_pts,normal_array)
            # mesh.addQuality().cmap('jet', input_array=intpr,arrayName="Quality", on="points",vmin=-1,vmax=1)
            # plot.show(mesh ,bg='w',interactive=0)
            #time.sleep(2)
            # if(ix >= 100 and ix % 5 == 0):
                
            #     #print(len(calcFFT(ftvalues)))
                
            #     calcVals = calcFFT(ftvalues)
                
            #     # print(calcVals)
            #     # print(len(calcVals))
            #     # print(len(sensor_pts))

            #     #max_value = max(calcVals) # 1.list [[5],[8], [3]] => max_value = 8,  2.list [[2],[1],[3]] => max_value = 3
            #     # what i want max_value = 8 FeelsDankMan
                
            #     #normal_array = calcVals/np.linalg.norm(calcVals)
                
            #     #maxV = max(max(calcVals),maxV)

            #     intpr = RBF_Interpolation(mesh,sensor_pts, calcVals)
            #     mesh.addQuality().cmap('jet', input_array=intpr,arrayName="Quality", on="points",vmin=0)
            #     ftvalues = np.delete(ftvalues,[0,5],1)
            # ix +=1
    
    
        
        
                  
    
                # plt.plot(fr,ps)
                # plt.pause(0.05)
            
            

            
            
            # 


            
            


            
            

