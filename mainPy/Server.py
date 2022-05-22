import numpy as np
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
import socket
settings.allowInteraction = True
dr = 'C:/Users/ameen/Desktop/Bachelor_Arbeit/Bachelor/mainPy/'
raw = mne.io.read_raw_edf(dr + "edf_data/Data_03_raw.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz', 'Trigger'])
#raw.filter(6,12)
dir_path = os.path.dirname(os.path.realpath(__file__))
data = [0] * 20
ch_names = raw.info["ch_names"]
headPath = f"{dir_path}/3dmodel/Head.obj"
sensor_locations = get_sensor_3DLocations(ch_pos,"TRG")

mesh = get_mesh(headPath)
vMin = -1
vMax = 1



def getRGB(actor, alpha=True, on='points'):
    lut = actor.mapper().GetLookupTable()
    poly = actor.polydata(transformed=False)
    if 'point' in on:
        vscalars = poly.GetPointData().GetScalars()
    else:
        vscalars = poly.GetCellData().GetScalars()
    cols =lut.MapScalars(vscalars, 0,0)
    arr = utils.vtk2numpy(cols)
    if not alpha:
        arr = arr[:, :3]
    return arr


def slider(widget,event):
    value = widget.GetRepresentation().GetValue()
    ch_name = widget.GetRepresentation().GetTitleText()
    ch_idx = mne.pick_channels(ch_names,include=[f"{ch_name}"])
    data[ch_idx[0]] = value
    n_data = str(data)
    n_data = n_data[1:len(n_data)-1]
    
    with open(dr+"test.txt", "w") as f:
          f.write(n_data)
    
    intrp = RBF_Interpolation(mesh,sensor_locations,data)
    mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points",vmin=vMin,vmax=vMax)
    websockets.serve(server,"localhost",5050)
    #clrs = getRGB(mesh).tolist()

idx = 0
txts = []
for pt in sensor_locations:
    txt = Text3D(f"{chnls[idx][4:6]}",pt,s=0.004,c='k')
    txt.followCamera()
    txts.append(txt)
    idx+=1
sensor_pts = Points(sensor_locations,r=9)
ranges = np.linspace(.035,.95,20)
idx = 0
intrp = RBF_Interpolation(mesh,sensor_locations,data)
mesh.cmap('jet', intrp,vmin=vMin,vmax=vMax)
for i in ranges:
    show(interactive=0).addSlider2D(slider,0,vMax,pos=[(0.075,i),(.25,i)],titleSize=0.5, title= f"{chnls[idx]}",showValue=False,tubeWidth=0.0025,sliderWidth=0.0070)
    idx+=1
i = 0
# show(mesh,sensor_pts,*txts,interactive=1)

import asyncio
import websockets
from concurrent.futures import ProcessPoolExecutor
show(mesh,interactive=1)
print("Listening on " + str(5050))
connected = set()
# async def server(websocket,path):
#     #show(mesh,interactive=1)
#     print("connected")
    
#     connected.add(websocket)
#     await websocket.send(json.dumps({"yo":[1,2,3]}))
    # try:
    #     async for message in websocket:
    #         await websocket.send(json.dumps({"yo":[1,2,3]}))
    #         # await websocket.send(f"new message: yo")
    #         # for conn in connected:
    #         #     if conn != websocket:
    #         #         await conn.send(f"new message: {message}")
    # finally:
    #     connected.remove(websocket)

#start_server = websockets.serve(server,"localhost",5050)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()


# WEBSOCKET