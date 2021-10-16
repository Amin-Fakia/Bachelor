# Imports
from functions import *
from dsi_24_montage import ch_pos
# make sure to support vedo: https://github.com/marcomusy/vedo
s_edf = "..\\Bachelor\\Project_Bac\\Test_Data.edf"
s_obj = "..\\Bachelor\\Project_Bac\\Head.obj"
data_set = get_data_from_raw_edf(s_edf)
# test_data = np.array([i[800] for i in data_set])
mesh = get_mesh(s_obj)
sensor_pts = get_sensor_3DLocations(ch_pos)
pts = findVert(sensor_pts,mesh)
# li = Linear_Interpolation(mesh,sensor_pts,test_data)
# rb = RBF_Interpolation(mesh,pts,test_data)
# mesh.addQuality().cmap('jet', rb)

#plot_data_from_edf('Test_Data.edf')
animate_data_span(s_edf,mesh,pts,data_set) # This is experimental still, run it on your own risk
#animate(mesh,pts,data_set,t1=0,t2=7000,f=0.01)
