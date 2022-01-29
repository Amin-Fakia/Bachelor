import matplotlib.pyplot as plt
import numpy as np
from Cursor import Cursor


x = np.arange(0, 1, 0.01)
y = np.sin(2 * 2 * np.pi * x)

fig, ax = plt.subplots()
ax.set_title('Simple cursor')
ax.plot(x, y, 'o')
cursor = Cursor(ax)
fig.canvas.mpl_connect('motion_notify_event', cursor.on_mouse_move)
cid = fig.canvas.mpl_connect('button_press_event', cursor.on_mouse_click)
plt.show()