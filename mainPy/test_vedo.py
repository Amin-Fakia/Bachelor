import vedo
import numpy as np

vedo.settings.interpolateScalarsBeforeMapping=False

res=4

s = vedo.Sphere(res=res).lw(1)#.ps(20)
pts = s.points()
red = np.abs(pts[:,0])*255
gre = np.abs(pts[:,1])*255
blu = np.abs(pts[:,2])*255

s.pointdata["RGBA"] = np.c_[red,gre,blu].astype(np.uint8)
s.pointdata.select("RGBA")
print(s.pointdata.keys())
n  = len(pts)
sn = int(np.sqrt(n))+1

gr = vedo.Grid(resx=sn, resy=sn).pos(0.5,0.5).wireframe(False)
rgb = np.zeros([gr.N(), 3]).astype(np.uint8)
rgb[:n] = s.pointdata["RGBA"]
gr.pointdata["RGBA"] = rgb
gr.pointdata.select("RGBA")

arr = np.flip(rgb.reshape([sn+1,sn+1,3]), axis=0)
pic = vedo.Picture(arr).write("t.png")

s2 = vedo.Sphere(res=res).lw(1)#.ps(20)
tcoords = gr.points()[:,(0,1)] + (0.0,0.0)

s2.texture("t.png", tcoords=tcoords[:n], 
  interpolate=False, repeat=False,
)

vedo.show(
  s+s.labels('id'), 
  gr+gr.labels('id').c('white'), 
  pic,
  s2+s2.labels('id'), 
  N=4, sharecam=0, axes=1,
)