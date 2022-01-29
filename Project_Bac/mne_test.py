
import matplotlib.pyplot as plt
import mne
import numpy as np

from matplotlib.animation import FuncAnimation
from vedo import show, interactive



raw = mne.io.read_raw_edf("Eyes_Open_Eyes_Closed_filtered.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])

new_events = mne.make_fixed_length_events(raw, start=5, stop=50, duration=2.)


print(new_events)
raw.plot(duration=100)

plt.show()