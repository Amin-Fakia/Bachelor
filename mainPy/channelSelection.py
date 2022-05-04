import matplotlib.pyplot as plt
import mne
import numpy as np
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from vedo import show, interactive
from functions import *
from dsi_24_montage import ch_pos
import scipy
from scipy.signal import savgol_filter
import easygui
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

edf_file= f"{dir_path}/edf_data/Data_02_raw.edf"
# Data_02_raw.edf
#mesh 3d
headPath = f"{dir_path}/3dmodel/Head.obj"
mesh = get_mesh(headPath)
# sensor points

sensor_pts = get_sensor_3DLocations(ch_pos)
pts = Points(sensor_pts,r=7)
proj_pts = findVert(sensor_pts,mesh)


arrows = Arrows(sensor_pts, proj_pts, s=0.2, c='red')
#plot
plot = Plotter(axes=0)
plot.show(mesh,pts,arrows)

#data
raw = mne.io.read_raw_edf(edf_file ,preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
raw.filter(8,12)