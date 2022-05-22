import matplotlib.pyplot as plt
import matplotlib
#matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['axes.spines.right'] = False
matplotlib.rcParams['axes.spines.top'] = False
import numpy as np
from scipy.spatial import distance
from scipy.interpolate import Rbf

p = [0,0,0]
p1 = [-2.89,-2.89,-2.89]
p2 = [2.89,2.89,2.89]
p3 = [4,9,2]
p4 = [1,2,-3.4]
p5= [1,-10,1]
data = [3,5,0,-5,-10]
pts = [p1,p2,p3,p4,p5]
i = 0
test = []
for pn in pts:
    dist = distance.euclidean(pn,p)
    test.append((dist)*data[i])
    i+=1
print(sum(test))
x, y, z = np.split(np.array(pts), 3, axis=1)
itr = Rbf(x,y,z,data,function='linear')
xi, yi, zi = 0,0,0
print(itr(xi,yi,zi))



# def test(lis,d,p):

