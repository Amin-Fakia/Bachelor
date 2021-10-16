import numpy as np
import mne
import scipy.interpolate as si
from vedo import *
from scipy.interpolate import Rbf
from vedo import show, interactive
import matplotlib.pyplot as plt
import time
from PyQt5 import QtWidgets
from matplotlib.widgets import SpanSelector

mne.set_log_level(0)
def get_data_from_raw_edf(s):
    if isinstance(s,str):
        raw = mne.io.read_raw_edf(s) 
        return raw.get_data()

def get_times(s):
    raw = mne.io.read_raw_edf(s)
    df = raw.to_data_frame()
    return df.iloc[:,0]
def clean_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_ticks([])

def plot_data_from_edf(s):
    fig,ax = plt.subplots()
    times = [t/1000 for t in get_times(s)]
    for d in get_data_from_raw_edf(s):
        ax.plot(times,d, c='blue',linewidth=0.5)
    plt.show()
    
def get_text(t1,t2):
    return Text2D(f'{t1} - {t2} in s')   
def animate_data_span(s,mesh,pts,data):
    fig,ax = plt.subplots()
    times = [t/1000 for t in get_times(s)]
    for d in get_data_from_raw_edf(s):
        line, = ax.plot(times,d, c='blue',linewidth=0.5)
        
    def onselect(xmin, xmax):
        indmin, indmax = np.searchsorted(times, (xmin, xmax))
        indmax = min(len(times) - 1, indmax)

        region_x = times[indmin:indmax]
        plt.close()
        animate(mesh,pts,data,times.index(min(region_x)),times.index(max(region_x)),0.02,get_text(min(region_x),max(region_x)))


    span = SpanSelector(ax, onselect, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor='tab:red'))
    try:
        win = fig.canvas.manager.window
    except AttributeError:
        win = fig.canvas.window()
    toolbar = win.findChild(QtWidgets.QToolBar)
    toolbar.setVisible(False)
    clean_ax(ax)
    plt.show()
def get_mesh(s):
    if isinstance(s,str):
        mesh = Mesh(s)
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

    
def animate(mesh,pts,data,t1,t2,f=0.02,text=Text2D('')):
    plot = show(interactive=False)
    if t1 < 0:
        print("please insert a valid starting time-point")
    if t2 > len(data[0]):
        print("please insert a valid ending time-point")
    vmin = min([min(i[t1:t2]) for i in data])
    vmax = max([max(i[t1:t2]) for i in data])
    for i in range(t1,t2):
        intpr = RBF_Interpolation(mesh,pts,[j[i] for j in data])
        mesh.cmap('jet', intpr,vmax=vmax,vmin=vmin)
        plot.show(mesh,text)
        plot.remove(text)
        time.sleep(f)
    plot.close()
    quit()
        
    