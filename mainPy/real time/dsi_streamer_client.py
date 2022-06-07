import sys

# setting path
sys.path.append('../Bachelor/mainPy')
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
import json
from queue import Queue
import threading
# CONSTANTS
TCP_IP = "127.0.0.1"
TCP_PORT = 9067
UNITY_PORT = 6050
host,port = socket.gethostbyname(TCP_IP ), UNITY_PORT
BUFFER_SIZE = 5
NUMBER_OF_THREADS = 6
JOB_NUMBER = [1, 2, 3]
queue = Queue()
win_idx = 0

global colors
colors = []

# GET Paths
dir_path = '../Bachelor/mainPy'
headPath = f"{dir_path}/3dmodel/Head.obj"


# Initialize Plotter
sensor_pts = get_sensor_3DLocations(ch_pos,["TRG"])
mesh = get_mesh(headPath)
plot = Plotter(axes=0)



# Connect socket
new_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
new_s.connect((TCP_IP, TCP_PORT))




# calculate fourier transform
def calcFFT(data):
    fftVal = []
    for d in data: # get every row
        ft = np.abs(np.fft.rfft(d))
        # ps = np.square(ft)
        fftVal.append(sum(ft))
    return fftVal




scbar = mesh.addScalarBar()

new_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



def start():
    print("waiting for connection")
    counter = 0
    
    global colors
    while counter < 100:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            colors =  getRGB(mesh).tolist()
            msg = json.dumps({"mylist": colors,"win_idx":win_idx})
            s.sendall(bytes(msg,encoding="utf-8"))
            time.sleep(1/60)
        except:
            print("Connection Failed, retrying..")
            counter+=1
            time.sleep(1)
        
    s.close()    
    


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
def plot_FFT():
    global ftvalues

    

def start_dsi_client():
    global colors
    global win_idx
    print("starting dsi client")
    ftvalues = np.empty((20))
    step = 20
    win_size = 100
    ix = 0
    while True:    
        data = new_s.recv(BUFFER_SIZE)
        
        if data == None:
            break
        if data == "@ABCD".encode():
            
            data += new_s.recv(BUFFER_SIZE)
            data += new_s.recv(dc.decodeBytes_packetLength(data))
            
            # if dc.decodeBytes_packetType(data) == 5:
            #     dc.printEventPacket(data)
            
            if dc.decodeBytes_packetType(data) == 1:
                #o1 = np.array(dc.decodeBytes_ChData(data, offset=23+14*4, len=4),dtype=object).T
                #y.append(np.array(dc.decodeBytes_ChData(data, offset=23+14*4, len=4),dtype=object).T)
                
                eeg_data = dc.printsensorDataPacket(data)
                ftvalues = np.c_[ftvalues,eeg_data]
                if ix>= win_size and ix % step == 0:
                    win_idx = ix//step
                    psds = calcFFT(ftvalues)
                    vmax = max(psds)
                    intpr = RBF_Interpolation(mesh,sensor_pts,psds)
                    mesh.addQuality().cmap('jet', input_array=intpr,arrayName="Quality", on="points",vmin=0)

                    st = f"Step: { step }, Window Size: {win_size}\nMax Value: {vmax/1e6:.3f}"
                    
                    #txt.text(st)
                    #scbar = mesh.addScalarBar()
                    # plot.show(mesh,txt,interactive=False)
                    # plot.remove(scbar)
                    ftvalues = np.delete(ftvalues,range(step),1)

                ix+=1
    

# Start threading
def work():
    while True:
        x = queue.get()
        if x == 1:
            start()
        if x == 2:
            start_dsi_client()
        if x == 3:
            plot_FFT()
        queue.task_done()

        
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()

create_workers()
create_jobs()


# Original script
# while True:    
#     data = s.recv(BUFFER_SIZE)
    
#     if data == None:
#         break
#     if data == "@ABCD".encode():
        
#         data += s.recv(BUFFER_SIZE)
#         data += s.recv(dc.decodeBytes_packetLength(data))
        
#         # if dc.decodeBytes_packetType(data) == 5:
#         #     dc.printEventPacket(data)
        
#         if dc.decodeBytes_packetType(data) == 1:
            
#             #o1 = np.array(dc.decodeBytes_ChData(data, offset=23+14*4, len=4),dtype=object).T
#             #y.append(np.array(dc.decodeBytes_ChData(data, offset=23+14*4, len=4),dtype=object).T)

#             eeg_data = dc.printsensorDataPacket(data)
#             ftvalues = np.c_[ftvalues,eeg_data]
#             if ix>= win_size and ix % step == 0:
#                 psds = calcFFT(ftvalues)
#                 vmax = max(psds)
#                 intpr = RBF_Interpolation(mesh,sensor_pts,psds)
#                 mesh.addQuality().cmap('jet', input_array=intpr,arrayName="Quality", on="points",vmin=0)
                
#                 #print(len(ftvalues[0]))
#                 st = f"Step: { step }, Window Size: {win_size}\nMax Value: {vmax/1e6:.3f}"
                
#                 txt.text(st)
#                 scbar = mesh.addScalarBar()
#                 show(mesh,txt,interactive=False)
#                 plot.remove(scbar)
#                 ftvalues = np.delete(ftvalues,range(step),1)

#             ix+=1
            


            
            


            
            

