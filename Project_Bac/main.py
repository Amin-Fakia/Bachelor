# Imports
from functions import *
from dsi_24_montage import ch_pos
# make sure to support vedo: https://github.com/marcomusy/vedo

data_set = get_data_from_raw_edf("Test_Data.edf")
test_data = np.array([i[800] for i in data_set])
mesh = get_mesh('Head.obj')
sensor_pts = get_sensor_3DLocations(ch_pos)
pts = findVert(sensor_pts,mesh)
li = Linear_Interpolation(mesh,sensor_pts,test_data)
rb = RBF_Interpolation(mesh,pts,test_data)
mesh.addQuality().cmap('jet', rb)
plot = show(mesh,interactive=False)
animate(mesh,pts,data_set,plot,t1=500,t2=700,f=0.01)
