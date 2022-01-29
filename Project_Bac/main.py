# Imports
from functions import *
from dsi_24_montage import ch_pos
import mne
from mne.time_frequency import psd_welch
from fooof import FOOOFGroup
from fooof.bands import Bands
from fooof.analysis import get_band_peak_fg
from fooof.plts.spectra import plot_spectrum
from mne.viz import plot_topomap
# make sure to support vedo: https://github.com/marcomusy/vedo
import numpy as np

raw = mne.io.read_raw_edf("Data_01_filtered_01_30.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
#raw.filter(8,12,fir_design="firwin2")
print(raw.info["ch_names"])

raw.plot(duration=100)
raw.plot_psd()
s_edf = "Test_Data.edf"
s_obj = "Head.obj"

#raw.plot()

data = get_data_from_raw_edf(raw)

f_data = []
for i in range(0,len(data)):
    if i == 13:
        f_data.append(data[13])
    elif i == 14:
        f_data.append(data[14])
    else:
        f_data.append([0]*len(data[i]))
        
print(len(data))
    
        
        


test_data = [1.4163747478831715e-06, 4.14125764170079e-06, 5.085762826688711e-06, 4.234749406127594e-06, 3.971483195731643e-06, 3.0456608715792426e-06, 1.2877115723770402e-06, 2.6315636904426714e-06, 4.833254160529337e-06, 6.262575272639049e-06, 8.030891584852211e-06, 6.973788155416181e-06, 3.0208964392932297e-06, 1.4670727629087545e-06, 1.6568362918653862e-06, 1.0343461100708259e-05, 1.4458459306627834e-05, 6.143860453501565e-06, 3.109986656619854e-06, 6.5331944370251785e-06]


print(len(data))
mesh = get_mesh(s_obj)
sensor_pts = get_sensor_3DLocations(ch_pos)
print(sensor_pts)
print([d[0] for d in data])
pts = findVert(sensor_pts,mesh)



rb = RBF_Interpolation(mesh,pts,test_data)


points = Points(pts)
# for j in range(50):
    
#     test_data = [i[6000+j] for i in data]
rb = RBF_Interpolation(mesh,pts,test_data)
mesh.addQuality().cmap('jet', input_array=rb,arrayName="Quality", on="points")
#     mesh.rotateX(-90)
#     mesh.write(f"C:\\Users\\ameen\\OneDrive\\Desktop\\EEG_Data\\EEG_{j}.ply")
#     mesh = get_mesh(s_obj)
# print(len(data[0]))

li = Linear_Interpolation(mesh,pts,test_data)



#print(mesh.polydata())
#mesh.rotateX(-90)
#mesh.write("C:\\Users\\ameen\\OneDrive\\Desktop\\EEG_Data\\file.ply")
#print(len(data))
show(mesh,points)
#enhanced_animation(raw,mesh,pts)
animate_data_span(raw,mesh,pts)
#plot_edf(raw)
#animate(mesh,pts,raw,6000,6100) # This is experimental still
#animate(mesh,pts,raw,t1=4000,t2=7000,f=0.01)
