import numpy as np
import mne
import scipy.interpolate as si
from vedo import *
from scipy.interpolate import Rbf,RBFInterpolator

from vedo import show, interactive
import matplotlib.pyplot as plt
import time
from PyQt5 import QtWidgets
from matplotlib.widgets import SpanSelector
import keyboard
import matplotlib.animation as animation
from matplotlib.backend_bases import MouseButton
from Cursor import Cursor
mne.set_log_level(0)




def get_data_from_raw_edf(raw):
    data = raw.get_data()[0:len(raw.get_data())-1]
    f_data = []
    
    for i in range(0,len(data)):
        if i == 13:
            f_data.append(data[13])
        elif i == 14:
            f_data.append(data[14])
        else:
            f_data.append([0]*len(data[i]))
    return f_data 

def get_times(raw):
    df = raw.to_data_frame()
    return df.iloc[:,0]
def clean_ax(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_ticks([])
def plot_data_from(raw,channels):
    fig,ax = plt.subplots(len(raw))
    c = 0
    for d in raw:

        ax[c].plot(range(len(d)),d, c='blue',linewidth=0.5)
        ax[c].set_ylabel(f"{channels[c]}", rotation=0)
       
        clean_ax(ax[c])
        c+=1
    plt.show()
def plot_data_from_edf(raw,channels):
    fig,ax = plt.subplots(len(raw.get_data()))
    times = [t/1000 for t in get_times(raw)]
    c = 0
    for d in get_data_from_raw_edf(raw):
        ax[c].plot(times,d, c='blue',linewidth=0.5)
        ax[c].set_ylabel(f"{channels[c]}", rotation=0)
       
        clean_ax(ax[c])
        c+=1
    plt.show()
def plot_data(data):
    fig,ax = plt.subplots()
    ax.plot(range(0,len(data)), data)
    plt.show()
def get_text(t1,t2):
    return Text2D(f'{t1/1000} - {t2/1000} in s',s=2,c='r')   
def get_average(data):
    return np.average(data,axis=0)
def animate_data_span(raw,mesh,pts):
    fig,ax = plt.subplots()
    times = [t/1000 for t in get_times(raw)]
    for d in get_data_from_raw_edf(raw):
        line, = ax.plot(times,d,linewidth=0.5,c='blue')
        
    def onselect(xmin, xmax):
        indmin, indmax = np.searchsorted(times, (xmin, xmax))
        indmax = min(len(times) - 1, indmax)
        
        region_x = times[indmin:indmax]
        plt.close() 
        animate(mesh,pts,raw,times.index(min(region_x)),times.index(max(region_x)),0.01)


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
        mesh.origin(0,-0.01,-0.05) # mesh.origin(0,-0.015,-0.05)
        mesh.scale(0.09)#  mesh.scale(0.09)
        return mesh
def get_sensor_3DLocations(l):
    pts = []
    for i, k in l.items():
        if i != 'TRG':
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
    itr = Rbf(x,y,z,data,function='gaussian')
    xi, yi, zi = np.split(mesh.points(), 3, axis=1) 
    return itr(xi,yi,zi)

def plot_edf(raw):
    raw.plot(duration=30)
    plt.show()
def plot_tfa(raw):
    raw.plot_psd()
    plt.show()
   
def animate(mesh,pts,raw,t1,t2,f=1,text=''):
    # Rbf or Linear

    data = get_data_from_raw_edf(raw)
    times = get_times(raw)
    
    #print(len(times))
    if t1 < 0 and t1 < t2:
        print("please insert a valid starting time-point")
    if t2 > len(data[0]) and t2 > t1 :
        print("please insert a valid ending time-point")
    vmin = min([min(i[t1:t2]) for i in data])
    #[t1:t2]
    vmax = max([max(i[t1:t2]) for i in data])
    print("yo")
    text = get_text(times[t1],times[t2])
    
    points= Points(pts,r=9,alpha=0.7,c='w')
    plot = show(interactive=False,bg='k')
    datas= []
    
    for i in range(t1,t2):
        text2 = Text2D(f'\n \n {times[i]/1000} ')
        intpr = RBF_Interpolation(mesh,pts,[j[i] for j in data])
        datas = [l[i] for l in data]
        points.cmap('jet', datas, vmin=vmin, vmax=vmax)
        mesh.cmap('jet', intpr, vmin=vmin, vmax=vmax)
        plot.show(mesh,points,text,text2) # ,text2
        plot.remove(text)
        plot.remove(text2)
        time.sleep(f)
    plot.close()
    quit()

def enhanced_animation(raw,mesh,pts):
    
    fig,ax = plt.subplots()
    times = [t/1000 for t in get_times(raw)]
    data = get_data_from_raw_edf(raw)

    try:
        win = fig.canvas.manager.window
    except AttributeError:
        win = fig.canvas.window()
    toolbar = win.findChild(QtWidgets.QToolBar)
    toolbar.setVisible(False)


    
    for d in get_data_from_raw_edf(raw):
        line, = ax.plot(times,d,linewidth=0.5,c='blue')
    cursor = Cursor(ax)
    fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
    cid = fig.canvas.mpl_connect('button_press_event', cursor.on_mouse_click)
    print(cid)
    plot = show(interactive=False,bg='k')
    i = 0
    # while i < 9000:
    #     text2 = Text2D(f'\n \n {times[i]/1000} ')
    #     intpr = RBF_Interpolation(mesh,pts,[j[i] for j in data])
    #     datas = [l[i] for l in data]
    #     mesh.cmap('jet', intpr)
    #     plot.show(mesh,text2) # ,text2
    #     plot.remove(text2)
    
    plt.show()
        
    