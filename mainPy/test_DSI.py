import vtk
from vedo import *


logpic = Picture("https://user-images.githubusercontent.com/32848391/110343974-530a4e00-802d-11eb-88c0-129753028ff9.png")

imagemapper = vtk.vtkImageMapper()
imagemapper.SetInputData(logpic._data)
imagemapper.SetColorWindow(255)
imagemapper.SetColorLevel(127.5)
# imagemapper.RenderToRectangleOn()  # no longer able to set the scale, but at least the image does not deform anymore
# aspect = logpic.shape[1]/logpic.shape[0] # (width / height)

image = vtk.vtkActor2D()
image.SetMapper(imagemapper)

# https://vtk.org/doc/nightly/html/classvtkCoordinate.html

position1_coordinate = image.GetPositionCoordinate()

# position1 : The position variable controls the lower left corner of the Actor2D
# position2 is the position of the upper-right corner of the actor. It is by default relative to Position and in normalized viewport coordinates.

refpos = vtk.vtkCoordinate()
refpos.SetCoordinateSystemToNormalizedViewport()
refpos.SetValue(1,1)  # upper right corner
#
# # Define the lower-left corner relative to the ref-position and in pixels
position1_coordinate.SetReferenceCoordinate(refpos)
position1_coordinate.SetCoordinateSystemToViewport() #  x-y pixel values in viewport
position1_coordinate.SetValue(-logpic.shape[0],-logpic.shape[1])

# # Now try to do the same with position2
#
# Position2 is supposed to set the upper-right corner of the actor
# but it doens't work for me
#
# position2_coordinate = image.GetPosition2Coordinate()
# position2_coordinate.SetReferenceCoordinate(refpos)
# position2_coordinate.SetCoordinateSystemToViewport() # x-y pixel values in viewport
# position2_coordinate.SetValue(0,0)

plotter = Plotter()
plotter.show(Sphere(), image, axes=1)