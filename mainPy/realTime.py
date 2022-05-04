import matplotlib.pyplot as plot
import numpy as np
import time
import csv
from functions import *
import os
import ast
import vtk
import matplotlib
import json
import vedo
from vedo import *
from dsi_24_montage import ch_pos,chnls
from vedo import show
dir_path = os.path.dirname(os.path.realpath(__file__))
headPath = f"{dir_path}/3dmodel/Head.obj"
mesh = get_mesh(headPath)
sensor_locations = get_sensor_3DLocations(ch_pos,"TRG")
import timeit
#settings.allowInteraction = True

# raw = mne.io.read_raw_edf("./mainPy/edf_data/Data_03_raw.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz', 'Trigger'])
# raw.filter(6,12)
# data = [r[400] for r in raw.get_data()]

# ch_names = raw.info["ch_names"]
# plt = Plotter()

# intrp = RBF_Interpolation(mesh,sensor_locations,data)
# def square_matrix(size,size2, *elements):
#     return np.array(elements).reshape(size, size2)

# # print(intrp)
# mesh.cmap('jet', intrp)
# mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
# # mesh.write(f"mainPy/ply_data/EEG_0.ply")

# # vMin = -1
# # vMax = 1


# def slider(widget,event):
#     value = widget.GetRepresentation().GetValue()
#     ch_name = widget.GetRepresentation().GetTitleText()
#     ch_idx = mne.pick_channels(ch_names,include=[f"{ch_name}"])
#     data[ch_idx[0]] = value 
#     intrp = RBF_Interpolation(mesh,sensor_locations,data)
#     mesh.cmap('jet', intrp,vmin=vMin,vmax=vMax)
# idx = 0
# txts = []
# for pt in sensor_locations:
#     txt = Text3D(f"{chnls[idx][4:6]}",pt,s=0.004,c='k')
#     txt.followCamera()
#     txts.append(txt)
#     idx+=1
# sensor_pts = Points(sensor_locations,r=9)
# ranges = np.linspace(.035,.95,20)
#intrp = RBF_Interpolation(mesh,sensor_locations,data)

# cmap = matplotlib.cm.get_cmap('jet')
# norm = plot.Normalize()
# rgba = cmap(norm(intrp))
# test = np.squeeze(rgba,1).tolist()





# mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
# show(mesh)
# #mesh.pointdata["colors"] = 
# poly = mesh.pointdata['Quality']
# print(poly)
# lol = vtk.vtkColorTransferFunction().convertToRGBA()
# print(lol)
# cmapname = 'RdBu_r'
# cmap = plt.get_cmap(cmapname)
# show(mesh)
# plot_arr = square_matrix(62,52, poly)
# plot.imshow(plot_arr,cmap='jet')
# plot.show()
#plot.imshow(poly)

# print(len(poly))
# n  = len(mesh.points())
# sn = int(np.sqrt(n))+1
# print(n)
# gr = vedo.Grid(resx=sn, resy=sn).pos(0.5,0.5).wireframe(False)
# rgb = np.zeros([gr.N(), 3]).astype(np.uint8)
# print(len(rgb))
# rgb[:n] = mesh.pointdata['Quality']
# gr.pointdata["RGBA"] = poly
# gr.pointdata.select("RGBA")

# arr = np.flip(rgb.reshape([sn+1,sn+1,3]), axis=0)
# pic = vedo.Picture(arr).write("t.png")
# show(pic)

# idx = 0
# for i in ranges:
#     show(mesh,interactive=0).addSlider2D(slider,0,vMax,pos=[(0.075,i),(.25,i)],titleSize=0.5, title= f"{chnls[idx]}",showValue=False,tubeWidth=0.0025,sliderWidth=0.0070)
#     idx+=1
# i = 0


#show(mesh,sensor_pts,interactive=1)
#show(mesh,sensor_pts,interactive=0)

# Text Real time
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




from flask import Flask, redirect, url_for, render_template,request
import time
import json
import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
app = Flask(__name__)
@app.route("/")
def home():
    if request.method == "GET":
        data = np.loadtxt("mainPy/test.txt", delimiter=",")
        intrp = RBF_Interpolation(mesh,sensor_locations,data)
        mesh.cmap('jet', intrp,vmin=-1,vmax=1)
        mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
        colors = getRGB(mesh,on="points").tolist()

        response = app.response_class( 
            response = json.dumps({f"mylist":colors}),
            status = 200,
            mimetype="application/json"
            )
        return response
    return "yo"


if __name__ == "__main__":
    app.run(debug=True)
#show(mesh)


# print(len(mesh.points()))


# st = time.time()
# i = 0
# while True:
    
#     data = np.loadtxt("mainPy/test.txt", delimiter=",")
    

#     #data = lines
    
#     intrp = RBF_Interpolation(mesh,sensor_locations,data)
    
#     mesh.cmap('jet', intrp,vmin=-1,vmax=1)
#     mesh.addQuality().cmap('jet', input_array=intrp,arrayName="Quality", on="points")
#     colors = getRGB(mesh,on="points").tolist()
#     with open('liveData.json','w') as f:
#         jtest = json.dumps({f"mylist_{i}":colors})
#         f.write(jtest)
    
#     time.sleep(2)
#     i+=1





    
    
