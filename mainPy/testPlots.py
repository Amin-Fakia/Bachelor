import matplotlib
from matplotlib import cm
import matplotlib.animation as anime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

np.random.seed(29680801)
 
fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
 
plt.xlim(-5, 5)
plt.ylim(-5, 5)
 
metadata=dict(title="Movie",artist="sourabh")
writer= anime.PillowWriter(fps=15,metadata=metadata)
 
def func(x,y,r,t):
    return np.cos(r/2+t)*np.exp(-np.square(r)/50)
 
xdata = np.linspace(-10, 10, 1000)
ydata = np.linspace(-10, 10, 1000)
 
x_list, y_list = np.meshgrid(xdata, ydata)
 
r_list = np.sqrt( np.square(x_list) + np.square(y_list) )
plt.show(block=False)
