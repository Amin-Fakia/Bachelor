import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import mne


raw = mne.io.read_raw_edf("Data_01_filtered_01_30.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])

data = raw.get_data()
data = data[13]
sampling_rate = 30.0

time = np.arange(0, 10, 1/sampling_rate)


fourier_transform = np.fft.rfft(data)

abs_fourier_transform = np.abs(fourier_transform)

power_spectrum = np.square(abs_fourier_transform)

frequency = np.linspace(0, sampling_rate/2, len(power_spectrum))
plt.plot(frequency, power_spectrum)

plt.show()