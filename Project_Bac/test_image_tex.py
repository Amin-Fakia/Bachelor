import vedo
import numpy as np
from functions import *
from dsi_24_montage import ch_pos
from vedo import show, interactive
s_obj = "Head.obj"
mesh = get_mesh(s_obj)
raw = mne.io.read_raw_edf("Data_02_raw.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
raw.filter(8,12)

fig, ax = plt.subplots(2)
def get_times(raw):
    df = raw.to_data_frame()
    return df.iloc[:,0]

data = raw.get_data()[:len(raw.get_data())-1]
sensor_pts = get_sensor_3DLocations(ch_pos)
print(len(sensor_pts))
print(len([j[0] for j in data]))
intpr = RBF_Interpolation(mesh,sensor_pts,[j[100] for j in data])
#mesh.cmap('jet', intpr)
#plot = Plotter(axes=0)
#plot.show(mesh)

# s = vedo.Sphere()
pts = mesh.points()
red = np.abs(pts[:,0])*255
gre = np.abs(pts[:,1])*255
blu = np.abs(pts[:,2])*255

mesh.pointdata["RGBA"] = np.c_[red,gre,blu].astype(np.uint8)
mesh.pointdata.select("RGBA")

n=len(pts)
sn=int(np.sqrt(len(pts)))+1
# print(n, sn)

gr = vedo.Grid(resx=sn, resy=sn).pos(0.5,0.5).wireframe(False).lw(0)
rgb = np.zeros([gr.N(), 3]).astype(np.uint8)
rgb[:n] = mesh.pointdata["RGBA"]
# gr.pointdata["RGBA"] = rgb
# gr.pointdata.select("RGBA")

arr = np.flip(rgb.reshape([sn+1,sn+1,3]), axis=0)
pic = vedo.Picture(arr).write("t.png")

# s2 = vedo.Sphere()
# tcoords = gr.points()[:,(0,1)]
# s2.texture("t.png", tcoords=tcoords[:n], interpolate=False)

vedo.show(mesh, pic, N=2, sharecam=0, axes=1)