
import matplotlib.pyplot as plt
import mne
import numpy as np
raw = mne.io.read_raw_edf("./mainPy/edf_data/Data_03_raw.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz', 'Trigger'])

data = raw.get_data()
print(data[0])

ft = np.abs(np.fft.rfft([12,10]))
ps = np.square(ft)
print(sum(ft))
frequency = np.linspace(0, 300/2, len(ps))
plt.plot(frequency, ps,color='red')

plt.show()