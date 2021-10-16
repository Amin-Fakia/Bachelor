# Imports
from functions import *
from dsi_24_montage import ch_pos
import mne
# make sure to support vedo: https://github.com/marcomusy/vedo


s_edf = "..\\Bachelor\\Project_Bac\\Test_Data.edf"
s_obj = "..\\Bachelor\\Project_Bac\\Head.obj"
raw = mne.io.read_raw_edf(s_edf)

mesh = get_mesh(s_obj)
sensor_pts = get_sensor_3DLocations(ch_pos)
pts = findVert(sensor_pts,mesh)
data = get_data_from_raw_edf(raw)
test_data = [i[588] for i in data]
li = Linear_Interpolation(mesh,sensor_pts,test_data)
rb = RBF_Interpolation(mesh,pts,test_data)
mesh.addQuality().cmap('jet', li)

show(mesh)

#plot_data_from_edf(raw)

#animate_data_span(raw,mesh,pts) # This is experimental still
#animate(mesh,pts,raw,t1=4000,t2=7000,f=0.01)
