import matplotlib.pyplot as plt
import numpy as np


class Cursor:
    """
    A cross hair cursor.
    """
    def __init__(self, ax):
        self.ax = ax
        self.vertical_line = ax.axvline(color='k', lw=1)
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)

    def set_cross_hair_visible(self, visible):
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)


    def on_mouse_move(self, event):
        print("mouse move")
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        else:
            self.set_cross_hair_visible(True)
            x= event.xdata
            # update the line positions
            self.vertical_line.set_xdata(x)
            self.ax.figure.canvas.draw()
    def on_mouse_click(self,event):
        if event.inaxes:
            return event.xdata