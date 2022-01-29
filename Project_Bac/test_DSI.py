import mne_test
import matplotlib.pyplot as plt



raw = mne_test.io.read_raw_edf("Data_01_filtered_01_30.edf",preload=True).drop_channels(['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'])
raw.filter(7,12,fir_design="firwin2")
raw.plot(duration=1000)
plt.show()