
import aiohttp
import mne
from vedo import *
import os

from flask import Flask, redirect, url_for, render_template,request
import time
import json
from functions import *
from dsi_24_montage import ch_pos, chnls
import asyncio
from matplotlib import cm
import matplotlib.pyplot as plot
import socket
settings.allowInteraction = True
host, port = socket.gethostbyname(socket.gethostname()), 5050
ADDR = (host, port)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

app = Flask(__name__)
raw = mne.io.read_raw_edf("./mainPy/edf_data/Data_03_raw.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz', 'Trigger'])
#raw.filter(6,12)
dir_path = os.path.dirname(os.path.realpath(__file__))
data = [0] * 20
data = [d[100] for d in raw.get_data()]
ch_names = raw.info["ch_names"]
headPath = f"{dir_path}/3dmodel/Head.obj"
sensor_locations = get_sensor_3DLocations(ch_pos,"TRG")
sensor_locations_2D = get_sensor_2DLocations(ch_pos,"TRG")
mesh = get_mesh(headPath)
vMin = -1
vMax = 1
intrp = RBF_Interpolation(mesh,sensor_locations,data)
# mesh.cmap('jet', intrp,vmin=vMin,vmax=vMax)
mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")

plot.show()




# def getRGB(actor, alpha=True, on='points'):
#     lut = actor.mapper().GetLookupTable()
#     poly = actor.polydata(transformed=False)
#     if 'point' in on:
#         vscalars = poly.GetPointData().GetScalars()
#     else:
#         vscalars = poly.GetCellData().GetScalars()
#     cols =lut.MapScalars(vscalars, 0,0)
#     arr = utils.vtk2numpy(cols)
#     if not alpha:
#         arr = arr[:, :3]
#     return arr


# def slider(widget,event):
#     value = widget.GetRepresentation().GetValue()
#     ch_name = widget.GetRepresentation().GetTitleText()
#     ch_idx = mne.pick_channels(ch_names,include=[f"{ch_name}"])
#     data[ch_idx[0]] = value

#     #print(ch_idx[0],value)
#     intrp = RBF_Interpolation(mesh,sensor_locations,data)
#     mesh.cmap('jet', intrp,vmin=vMin,vmax=vMax)
#     mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
#     #clrs = getRGB(mesh).tolist()
    


# idx = 0
# txts = []
# for pt in sensor_locations:
#     txt = Text3D(f"{chnls[idx][4:6]}",pt,s=0.004,c='k')
#     txt.followCamera()
#     txts.append(txt)
#     idx+=1
# sensor_pts = Points(sensor_locations,r=9)
# ranges = np.linspace(.035,.95,20)
# idx = 0
# for i in ranges:
#     show(interactive=0).addSlider2D(slider,0,vMax,pos=[(0.075,i),(.25,i)],titleSize=0.5, title= f"{chnls[idx]}",showValue=False,tubeWidth=0.0025,sliderWidth=0.0070)
#     idx+=1
# i = 0
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# print(host)
# sock.bind(ADDR)

# #show(mesh,sensor_pts,*txts,interactive=0)
# print(f"[LISTENING] Server is listening on {host}")
# show(mesh,sensor_pts,*txts,interactive=0)
# while True:
#     time.sleep(1)
    
#     #print(f"[LISTENING] Server is listening on {host}")
#     # intrp = RBF_Interpolation(mesh,sensor_locations,data)
#     # mesh.cmap('jet', intrp,vmin=-vMin,vmax=vMax)
#     # mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
#     colors = getRGB(mesh,on="points").tolist()
    
#     show(mesh,sensor_pts,*txts,interactive=0)
#     response = json.dumps({f"mylist":colors})
#     sock.sendall(bytes(response,encoding="utf-8"))
#     print("yo")
    

    
    






    
