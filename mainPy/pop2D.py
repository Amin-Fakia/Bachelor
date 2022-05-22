from matplotlib.pyplot import axes
import scipy.interpolate
import numpy as np
from functions import *

import matplotlib
import os
import matplotlib.image as mpimg
from matplotlib.widgets import Slider
dir_path = os.path.dirname(os.path.realpath(__file__))

edf_file= f"{dir_path}/edf_data/Data_02_raw.edf"
raw = mne.io.read_raw_edf(edf_file ,preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz','Trigger'])
# close old plots
sensors = get_sensors_from_montage(raw.info['ch_names'])





xySensors = [v[0:2] for v in sensors.values()]
print(len(xySensors))

centroid = np.array(xySensors).mean(axis=0)

raw.filter(8,12)

data = raw.get_data()



#print(data)

plt.close("all")

# some parameters
N = 100           # number of points for interpolation
xy_center = centroid   # center of the plot
radius = .43      # radius

# mostly original code
psds = get_power_values(data,300)

koord = [[1,4],[3,4],[1,3],[3,3],[2,3],[1,2],[3,2],[2,2],[1,1],[3,1],[2,1],[1,0],[3,0],[0,3],[4,3],[0,2],[4,2],[0,1],[4,1]]
koord = xySensors
x,y = [],[]
for i in koord:
    x.append(i[0])
    y.append(i[1])

z = [i[0] for i in psds]

xi = np.linspace(-radius*1.55, radius*1.55, N)
yi = np.linspace(-radius*1.55, radius*1.55, N)
zi = scipy.interpolate.griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')

# set points > radius to not-a-number. They will not be plotted.
# the dr/2 makes the edges a bit smoother
# dr = xi[1] - xi[0]
# for i in range(N):
#     for j in range(N):
#         r = np.sqrt((xi[i] - xy_center[0])**2 + (yi[j] - xy_center[1])**2)
#         if (r - dr/2) > radius:
#             zi[j,i] = "nan"


# make figure
fig = plt.figure()

# set aspect = 1 to make it a circle
ax = fig.add_subplot(111, aspect = 1)

ax.get_xaxis().set_visible(False)
#hide y-axis 
ax.get_yaxis().set_visible(False)
ax.axis('off')
# use different number of levels for the fill and the lines
#ax.contourf(xi, yi, zi, 20, cmap = plt.cm.jet, zorder = 1)

head = matplotlib.patches.Ellipse(xy = xy_center, height = 1,width=.9,angle=0, edgecolor = "k", facecolor = "none",zorder=2)
whitearea = matplotlib.patches.Ellipse(xy = xy_center, height = 1.15,width=1.05,angle=0, edgecolor = "white", facecolor = "none",linewidth=30,zorder=1)
ear1 = matplotlib.patches.Ellipse(xy = [centroid[0]+radius*1.1575,centroid[1]], width = 0.1, height = .2, angle = 0, edgecolor = "k", facecolor = "none", zorder = 2)
ear2 = matplotlib.patches.Ellipse(xy = [centroid[0]-radius*1.1575,centroid[1]], width = 0.1, height = .2, angle = 0, edgecolor = "k", facecolor = "none", zorder = 2)


xy = [[centroid[0]-.06,radius*1.01], [centroid[0],radius*1.2],[centroid[0]+.06,radius*1.01]]
line = matplotlib.lines.Line2D([x[0] for x in xy], [x[1] for x in xy],color='k',linewidth=.9)
ax.add_line(line)
ax.add_patch(head)
ax.add_patch(whitearea)
ax.add_patch(head)
ax.add_patch(ear1)
ax.add_patch(ear2)

ax.scatter(x, y, marker = 'o', c = 'b', s = 15, zorder = 3)

axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
vmax = max([max(i[0:len(psds)]) for i in psds])
vmin = min([min(i[0:len(psds)]) for i in psds])
frame = 0
frame_slider = Slider(
    ax=axfreq,
    label="Window Number: ",
    valmin=0,
    valmax=len(psds[0])-1,
    valstep=1,
    valinit=frame,
    orientation="horizontal"
)

def update(val):
    frame = frame_slider.val
    
    ax.cla()
    zi = scipy.interpolate.griddata((x, y), [j[frame] for j in psds], (xi[None,:], yi[:,None]), method='cubic')
    #ax.imshow(zi,interpolation='gaussian',cmap=plt.cm.jet)
    ax.contourf(xi, yi, zi, 60, cmap =  plt.cm.jet, zorder = 1,vmin=-vmax,vmax=vmax)
    ax.add_patch(head)
    ax.add_patch(whitearea)
    ax.add_line(line)
    ax.add_patch(ear2)
    ax.add_patch(ear1)
    # #ax.scatter(x, y, marker = 'o', c = 'k', s = 15, zorder = 3)
    ax.axis('off')
    ax.set_title(f"power winodow: {frame}")

frame_slider.on_changed(update)

# plt.imshow(zi,interpolation='gaussian')
plt.show()
#ax.contour(xi, yi, zi, 15, colors = "grey", zorder = 2)
#plt.show()

i = 0
l = 0
while i < len(psds[0]):
    break
    ax.cla()
    zi = scipy.interpolate.griddata((x, y), [j[i] for j in psds], (xi[None,:], yi[:,None]), method='cubic')
    # ax.imshow(zi,interpolation='none',cmap=plt.cm.jet)
    # ax.contourf(xi, yi, zi, 20, cmap =  plt.cm.jet, zorder = 1,vmin=-vmax,vmax=vmax)
    # ax.add_patch(circle)
    # ax.add_patch(circle2)
    # ax.add_line(line)
    # ax.add_patch(ear2)
    # ax.add_patch(ear1)
    # ax.axis('off')
    # ax.set_title(f"power winodow: {i}")
    
    #plt.savefig(f'./EEGHoloLens2-main/mainPy/pics/{i}.png')


    if(l >= len(psds[0])*3):
        break
    if i == len(psds[0])-1:
        i = 0
    i+=1
    l+=1
    plt.pause(1/60) 
# import os
# lsdr = os.listdir('./EEGHoloLens2-main/mainPy/pics/')
# images = []
# for filename in lsdr:
#     images.append(imageio.imread(f'./EEGHoloLens2-main/mainPy/pics/{filename}'))
# imageio.mimsave('movie.gif', images)
# make a color bar
# cbar = fig.colorbar(CS, ax=ax)

# # add the data points
# # I guess there are no data points outside the head...


# # draw a circle
# # change the linewidth to hide the 
# circle = matplotlib.patches.Circle(xy = xy_center, radius = radius, edgecolor = "k", facecolor = "none")
# ax.add_patch(circle)

# # make the axis invisible 
# for loc, spine in ax.spines.items():
#     # use ax.spines.items() in Python 3
#     spine.set_linewidth(0)

# # remove the ticks
# ax.set_xticks([])
# ax.set_yticks([])

# # Add some body parts. Hide unwanted parts by setting the zorder low
# # add two ears
# circle = matplotlib.patches.Ellipse(xy = [0,2], width = 0.5, height = 1.0, angle = 0, edgecolor = "k", facecolor = "w", zorder = 0)
# ax.add_patch(circle)
# circle = matplotlib.patches.Ellipse(xy = [4,2], width = 0.5, height = 1.0, angle = 0, edgecolor = "k", facecolor = "w", zorder = 0)
# ax.add_patch(circle)
# # add a nose
# xy = [[1.5,3], [2,4.5],[2.5,3]]
# polygon = matplotlib.patches.Polygon(xy = xy, facecolor = "w", zorder = 0)
# ax.add_patch(polygon) 

# # set axes limits
# ax.set_xlim(-0.5, 4.5)
# ax.set_ylim(-0.5, 4.5)

