"""Picture in picture plotting"""
from vedo import *
from vedo.pyplot import plot
import numpy as np
import networkx as nx

settings.defaultFont = 'Theemim'

# ------------------------------------------------------------
# Build plot: network
# ------------------------------------------------------------
G = nx.gnm_random_graph(n=10, m=15, seed=1)
nxpos = nx.spring_layout(G, dim=3, seed=1)

nxpts = [nxpos[pt] for pt in sorted(nxpos)]
nx_lines = [(nxpts[i], nxpts[j]) for i, j in G.edges()]

pts = Points(nxpts, r=12)
edg = Lines(nx_lines).lw(4)

# node values
values = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [30, 80, 10, 79, 70, 60, 75, 78, 65, 10],
          [1, .30, .10, .79, .70, .60, .75, .78, .65, .90]]
time = [0.0, 0.1, 0.2]  # in seconds

pts1 = pts.cmap('Blues', values[0])
vplt = show(
    pts1, edg,
    axes=False,
    bg='white',
    at=0,
    interactive=False,
    zoom=1.3,
)
np_pic = Picture(screenshot(returnNumpy=True, scale=1))
vplt.close()

# ------------------------------------------------------------
# Build plot: exponential
# ------------------------------------------------------------
x = np.arange(0, 4, 0.1)
y = 3*np.exp(-x)

plt1 = plot(
    x, y,
    title=__doc__,
    xtitle='time in seconds',
    ytitle='some function [a.u.]',
)

np_pic.scale(0.0025).x(2).y(1.)

show(plt1, np_pic, size=(800,600), zoom=1.2)