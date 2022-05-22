import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget

from DSI24 import Ch_Data


def amplitude(arr):
    if len(arr) > 1:
        return abs(max(arr))+abs(min(arr))
    else:
        return 0

class CH_Plot(GraphicsLayoutWidget):
    def __init__(self, conn):
        super().__init__()

        self.data= Ch_Data.data()

        self.conn = conn


        self.lw = GraphicsLayoutWidget(show=False)

        self.addLabel(text='P3', row=0, col=0)
        self.chP3 = self.addPlot(row=0, col=1)
        self.chP3L = pg.LabelItem('')
        self.chP3.hideAxis('bottom')
        self.chP3.hideAxis('left')
        self.addItem(self.chP3L, row= 0 , col=2)

        self.addLabel(text='C3', row=1, col=0)
        self.chC3 = self.addPlot(row=1, col=1)
        self.chC3.hideAxis('bottom')
        self.chC3.hideAxis('left')
        self.chC3L = pg.LabelItem('')
        self.addItem(self.chC3L, row=1, col=2)

        self.addLabel(text='F3', row=2, col=0)
        self.chF3 = self.addPlot(row=2, col=1)
        self.chF3.hideAxis('bottom')
        self.chF3.hideAxis('left')
        self.chF3L = pg.LabelItem('')
        self.addItem(self.chF3L, row=2, col=2)

        self.addLabel(text='Fz', row=3, col=0)
        self.chFz = self.addPlot(row=3, col=1)
        self.chFz.hideAxis('bottom')
        self.chFz.hideAxis('left')
        self.chFzL = pg.LabelItem('')
        self.addItem(self.chFzL, row=3, col=2)

        self.addLabel(text='F4', row=4, col=0)
        self.chF4 = self.addPlot(row=4, col=1)
        self.chF4.hideAxis('bottom')
        self.chF4.hideAxis('left')
        self.chF4L = pg.LabelItem('')
        self.addItem(self.chF4L, row=4, col=2)

        self.addLabel(text='C4', row=5, col=0)
        self.chC4 = self.addPlot(row=5, col=1)
        self.chC4.hideAxis('bottom')
        self.chC4.hideAxis('left')
        self.chC4L = pg.LabelItem('')
        self.addItem(self.chC4L, row=5, col=2)

        self.addLabel(text='P4', row=6, col=0)
        self.chP4 = self.addPlot(row=6, col=1)
        self.chP4.hideAxis('bottom')
        self.chP4.hideAxis('left')
        self.chP4L = pg.LabelItem('')
        self.addItem(self.chP4L, row=6, col=2)

        self.addLabel(text='Cz', row=7, col=0)
        self.chCz = self.addPlot(row=7, col=1)
        self.chCz.hideAxis('bottom')
        self.chCz.hideAxis('left')
        self.chCzL = pg.LabelItem('')
        self.addItem(self.chCzL, row=7, col=2)

        """
        self.addLabel(text='CM', row=8, col=0)
        self.chCM = self.addPlot(row=8, col=1)
        self.chCM.hideAxis('bottom')
        self.chCM.hideAxis('left')
        self.chCML = pg.LabelItem('')
        self.addItem(self.chCML, row=8, col=2)        
        """

        self.addLabel(text='A1', row=9, col=0)
        self.chA1 = self.addPlot(row=9, col=1)
        self.chA1.hideAxis('bottom')
        self.chA1.hideAxis('left')
        self.chA1L = pg.LabelItem('')
        self.addItem(self.chA1L, row=9, col=2)

        self.addLabel(text='Fp1', row=10, col=0)
        self.chFp1 = self.addPlot(row=10, col=1)
        self.chFp1.hideAxis('bottom')
        self.chFp1.hideAxis('left')
        self.chFp1L = pg.LabelItem('')
        self.addItem(self.chFp1L, row=10, col=2)

        self.addLabel(text='Fp2', row=11, col=0)
        self.chFp2 = self.addPlot(row=11, col=1)
        self.chFp2.hideAxis('bottom')
        self.chFp2.hideAxis('left')
        self.chFp2L = pg.LabelItem('')
        self.addItem(self.chFp2L, row=11, col=2)

        self.addLabel(text='T3', row=12, col=0)
        self.chT3 = self.addPlot(row=12, col=1)
        self.chT3.hideAxis('bottom')
        self.chT3.hideAxis('left')
        self.chT3L = pg.LabelItem('')
        self.addItem(self.chT3L, row=12, col=2)

        self.addLabel(text='T5', row=13, col=0)
        self.chT5 = self.addPlot(row=13, col=1)
        self.chT5.hideAxis('bottom')
        self.chT5.hideAxis('left')
        self.chT5L = pg.LabelItem('')
        self.addItem(self.chT5L, row=13, col=2)

        self.addLabel(text='O1', row=14, col=0)
        self.chO1 = self.addPlot(row=14, col=1)
        self.chO1.hideAxis('bottom')
        self.chO1.hideAxis('left')
        self.chO1L = pg.LabelItem('')
        self.addItem(self.chO1L, row=14, col=2)

        self.addLabel(text='O2', row=15, col=0)
        self.chO2 = self.addPlot(row=15, col=1)
        self.chO2.hideAxis('bottom')
        self.chO2.hideAxis('left')
        self.chO2L = pg.LabelItem('')
        self.addItem(self.chO2L, row=15, col=2)

        self.addLabel(text='X3', row=16, col=0)
        self.chX3 = self.addPlot(row=16, col=1)
        self.chX3.hideAxis('bottom')
        self.chX3.hideAxis('left')
        self.chX3L = pg.LabelItem('')
        self.addItem(self.chX3L, row=16, col=2)

        self.addLabel(text='X2', row=17, col=0)
        self.chX2 = self.addPlot(row=17, col=1)
        self.chX2.hideAxis('bottom')
        self.chX2.hideAxis('left')
        self.chX2L = pg.LabelItem('')
        self.addItem(self.chX2L, row=17, col=2)

        self.addLabel(text='F7', row=18, col=0)
        self.chF7 = self.addPlot(row=18, col=1)
        self.chF7.hideAxis('bottom')
        self.chF7.hideAxis('left')
        self.chF7L = pg.LabelItem('')
        self.addItem(self.chF7L, row=18, col=2)

        self.addLabel(text='F8', row=19, col=0)
        self.chF8 = self.addPlot(row=19, col=1)
        self.chF8.hideAxis('bottom')
        self.chF8.hideAxis('left')
        self.chF8L = pg.LabelItem('')
        self.addItem(self.chF8L, row=19, col=2)

        self.addLabel(text='X1', row=20, col=0)
        self.chX1 = self.addPlot(row=20, col=1)
        self.chX1.hideAxis('bottom')
        self.chX1.hideAxis('left')
        self.chX1L = pg.LabelItem('')
        self.addItem(self.chX1L, row=20, col=2)

        self.addLabel(text='A2', row=21, col=0)
        self.chA2 = self.addPlot(row=21, col=1)
        self.chA2.hideAxis('bottom')
        self.chA2.hideAxis('left')
        self.chA2L = pg.LabelItem('')
        self.addItem(self.chA2L, row=21, col=2)

        self.addLabel(text='T6', row=22, col=0)
        self.chT6 = self.addPlot(row=22, col=1)
        self.chT6.hideAxis('bottom')
        self.chT6.hideAxis('left')
        self.chT6L = pg.LabelItem('')
        self.addItem(self.chT6L, row=22, col=2)

        self.addLabel(text='T4', row=23, col=0)
        self.chT4 = self.addPlot(row=23, col=1)
        self.chT4.hideAxis('bottom')
        self.chT4.hideAxis('left')
        self.chT4L = pg.LabelItem('')
        self.addItem(self.chT4L, row=23, col=2)

        self.curveP3 = self.chP3.plot()
        self.curveC3 = self.chC3.plot()
        self.curveF3 = self.chF3.plot()
        self.curveFz = self.chFz.plot()
        self.curveF4 = self.chF4.plot()
        self.curveC4 = self.chC4.plot()
        self.curveP4 = self.chP4.plot()
        self.curveCz = self.chCz.plot()
        #self.curveCM = self.chCM.plot()
        self.curveA1 = self.chA1.plot()
        self.curveFp1 = self.chFp1.plot()
        self.curveFp2 = self.chFp2.plot()
        self.curveT3 = self.chT3.plot()
        self.curveT5 = self.chT5.plot()
        self.curveO1 = self.chO1.plot()
        self.curveO2 = self.chO2.plot()
        self.curveX3 = self.chX3.plot()
        self.curveX2 = self.chX2.plot()
        self.curveF7 = self.chF7.plot()
        self.curveF8 = self.chF8.plot()
        self.curveX1 = self.chX1.plot()
        self.curveA2 = self.chA2.plot()
        self.curveT6 = self.chT6.plot()
        self.curveT4 = self.chT4.plot()

        # Set timer
        self.timer = pg.QtCore.QTimer()
        # Timer signal binding update_data function
        self.timer.timeout.connect(self.update_data)
        # The timer interval is 3ms, which can be understood as refreshing data once in 3ms
        self.timer.start(3)


    def update_data(self):

        if self.conn.empty() is False:
            self.data = self.conn.get()

        # Data is filled into the drawing curve
        self.curveP3.setData(self.data.p3fil)
        self.curveC3.setData(self.data.c3fil)
        self.curveF3.setData(self.data.f3fil)
        self.curveFz.setData(self.data.fzfil)
        self.curveF4.setData(self.data.f4fil)
        self.curveC4.setData(self.data.c4fil)
        self.curveP4.setData(self.data.p4fil)
        self.curveCz.setData(self.data.czfil)
        #self.curveCM.setData(self.data.cmfil)
        self.curveA1.setData(self.data.a1fil)
        self.curveFp1.setData(self.data.fp1fil)
        self.curveFp2.setData(self.data.fp2fil)
        self.curveT3.setData(self.data.t3fil)
        self.curveT5.setData(self.data.t5fil)
        self.curveO1.setData(self.data.o1fil)
        self.curveO2.setData(self.data.o2fil)
        self.curveX3.setData(self.data.x3fil)
        self.curveX2.setData(self.data.x2fil)
        self.curveF7.setData(self.data.f7fil)
        self.curveF8.setData(self.data.f8fil)
        self.curveX1.setData(self.data.x1fil)
        self.curveA2.setData(self.data.a2fil)
        self.curveT6.setData(self.data.t6fil)
        self.curveT4.setData(self.data.t4fil)


        self.chP3L.setText("{:.1f}".format(amplitude(self.data.p3fil)))
        self.chC3L.setText("{:.1f}".format(amplitude(self.data.c3fil)))
        self.chF3L.setText("{:.1f}".format(amplitude(self.data.f3fil)))
        self.chFzL.setText("{:.1f}".format(amplitude(self.data.fzfil)))
        self.chF4L.setText("{:.1f}".format(amplitude(self.data.f4fil)))
        self.chC4L.setText("{:.1f}".format(amplitude(self.data.c4fil)))
        self.chP4L.setText("{:.1f}".format(amplitude(self.data.p4fil)))
        self.chCzL.setText("{:.1f}".format(amplitude(self.data.czfil)))
        #self.chCML.setText("{:.1f}".format(amplitude(self.data.cmfil)))
        self.chA1L.setText("{:.1f}".format(amplitude(self.data.a1fil)))
        self.chFp1L.setText("{:.1f}".format(amplitude(self.data.fp1fil)))
        self.chFp2L.setText("{:.1f}".format(amplitude(self.data.fp2fil)))
        self.chT3L.setText("{:.1f}".format(amplitude(self.data.t3fil)))
        self.chT5L.setText("{:.1f}".format(amplitude(self.data.t5fil)))
        self.chO1L.setText("{:.1f}".format(amplitude(self.data.o1fil)))
        self.chO2L.setText("{:.1f}".format(amplitude(self.data.o2fil)))
        self.chX3L.setText("{:.1f}".format(amplitude(self.data.x3fil)))
        self.chX2L.setText("{:.1f}".format(amplitude(self.data.x2fil)))
        self.chF7L.setText("{:.1f}".format(amplitude(self.data.f7fil)))
        self.chF8L.setText("{:.1f}".format(amplitude(self.data.f8fil)))
        self.chX1L.setText("{:.1f}".format(amplitude(self.data.x1fil)))
        self.chA2L.setText("{:.1f}".format(amplitude(self.data.a2fil)))
        self.chT6L.setText("{:.1f}".format(amplitude(self.data.t6fil)))
        self.chT4L.setText("{:.1f}".format(amplitude(self.data.t4fil)))




