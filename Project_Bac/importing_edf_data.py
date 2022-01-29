#%%
import mne
import matplotlib.pyplot as plt
#get the needed montage for DSI 24
from dsi_24_montage import dsi_24_montage

#load the edf file
raw = mne.io.read_raw_edf('Eyes_Open_Closed_raw.edf', preload=True).drop_channels(['EEG X3-Pz','EEG X2-Pz','EEG X1-Pz','EEG CM-Pz']) # bug recording
raw.filter(1,30)
raw.plot(duration=50)

#changeing the raw channel_names to the channel_names of the dsi montage
i = 0
tmax = raw.times[-1]
# setting the dsi montage to the file
print(raw.ch_names)

for x in raw.ch_names:
    raw.rename_channels({x: dsi_24_montage.ch_names[i]})
    i += 1
raw.set_montage(dsi_24_montage)
raw.set_eeg_reference(projection=True).apply_proj()
raw.plot_sensors(show_names=True)
events = mne.make_fixed_length_events(raw,start=0,stop=tmax)
print(events)
event_dict = {'auditory/left': 1}
epochs = mne.Epochs(raw, events, tmin=-0.2, tmax=0.5, event_id=event_dict,
                    preload=True)
epochs.plot_
#plot power spectrum //fft
#raw.plot_psd()

plt.show()

# %%


#, 'EEG C3-Pz', 'EEG Fz-Pz', 'EEG C4-Pz',
#  'EEG Cz-Pz', 'EEG A1-Pz', 'EEG Fp1-Pz', 'EEG Fp2-Pz', 'EEG T3-Pz', 'EEG T5-Pz', 
#  'EEG O1-Pz', 'EEG O2-Pz', 'EEG F7-Pz', 'EEG F8-Pz', 'EEG A2-Pz', 'EEG T6-Pz', 'EEG T4-Pz', 'Trigger'