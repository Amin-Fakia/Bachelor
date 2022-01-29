import sys
from PyQt5 import Qt
from vedo.mesh import Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter, Picture, Text2D, printc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from Cursor import Cursor
class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)
        self.frame = Qt.QFrame()
        self.vl = Qt.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
        sc = MplCanvas(self, width=10, height=2, dpi=100)
        
        # Create renderer and add the vedo objects and callbacks
        self.vp = Plotter(qtWidget=self.vtkWidget)
        self.id2 = self.vp.addCallback("key press", self.onKeypress)
        self.imgActor = Mesh("Head.obj")
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        cs = Cursor(sc.axes)
        sc.mpl_connect('motion_notify_event', cs.on_mouse_move)
        sc.mpl_connect('button_press_event', cs.on_mouse_click)
        self.text2d = Text2D("")
        self.vp.show(self.imgActor, self.text2d
                     )    # <--- show the vedo rendering

        # Set-up the rest of the Qt window
        #self.slider = Qt.QSlider(1)
        #self.slider.valueChanged.connect(self.sliderValueChange)
        #self.vl.addWidget(self.slider)
        self.vl.addWidget(sc)
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
        self.show()                     # <--- show the Qt Window

    def onKeypress(self, evt):
        printc("You have pressed key:", evt.keyPressed, c='b')
        if evt.keyPressed=='q':
            self.vp.close()
            self.vtkWidget.close()
            exit()
           
    def sliderValueChange(self, value):
        self.imgActor.GetProperty().SetColorWindow(value*10)
#        self.imgActor.GetProperty().SetColorLevel(10)
        self.text2d.text(f"window is: {value*10}")
        self.vp.render()
        return
#        img = utils.vtk2numpy(self.image[:, :, value-1])
#        if self.imgActor is not None:
#            self.vp.remove(self.imgActor)
#        self.imgActor = Picture(img)
#        self.vp.add(self.imgActor)

    def onClose(self):
        self.vtkWidget.close()

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    app.aboutToQuit.connect(window.onClose) # <-- connect the onClose event
    app.exec_()