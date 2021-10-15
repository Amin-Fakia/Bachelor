import numpy as np
import mne
import scipy.interpolate as si
from vedo import *
from scipy.interpolate import Rbf
from dsi_24_montage import ch_pos
from vedo import settings, Line, show, interactive
import tkinter as tk
import matplotlib.pyplot as plt
import time

def get_data_from_raw_edf(s):
    if isinstance(s,str):
        raw = mne.io.read_raw_edf(s) 
        return raw.get_data()
def get_mesh(s):
    if isinstance(s,str):
        mesh = Mesh("Head.obj")
        mesh.triangulate().clean().normalize()
        mesh.rotateX(90)
        mesh.rotateZ(180)
        mesh.origin(0,-0.01,-0.04)
        mesh.scale(0.09) 
        return mesh
def get_sensor_3DLocations(l):
    pts = []
    for i, k in l.items():
        pts.append([k[0],k[1],k[2]])
    return pts
def findMinD(x,pts,mesh):
    dist = []
    for p in mesh.points():
        dist.append(np.linalg.norm(pts[x]-p))
    return dist.index(min(dist))

def findVert(pts,mesh):
    vrt =[]
    for i in range(0,len(pts)):
        vrt.append(findMinD(i,pts,mesh))
    return [mesh.points()[i] for i in vrt]

def Linear_Interpolation(mesh,pts,data):

    xi, yi, zi = np.split(mesh.points(), 3, axis=1) 
    lir = si.LinearNDInterpolator(pts,data)
    return [[i] for i in np.squeeze(lir(xi, yi, zi))]
    
def RBF_Interpolation(mesh,pts,data):
    x, y, z = np.split(np.array(pts), 3, axis=1)
    itr = Rbf(x, y, z, data) 
    xi, yi, zi = np.split(mesh.points(), 3, axis=1) 
    return itr(xi,yi,zi)
def animate(mesh,pts,data,plot,t1,t2,f=0.02):
    if t1 < 0:
        print("please insert a valid starting time-point")
    if t2 > len(data[0]):
        print("please insert a valid ending time-point")
    vmin = min([min(i[t1:t2]) for i in data])
    vmax = max([max(i[t1:t2]) for i in data])
    for i in range(t1,t2):
        intpr = RBF_Interpolation(mesh,pts,[j[i] for j in data])
        mesh.cmap('jet', intpr,vmax=vmax,vmin=vmin)
        plot.show(mesh)
        time.sleep(f)
        
    