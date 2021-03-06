import mne

#setting up the needed channels and positions with 'standard_alphabetic' montage
filepath = "mainPy/edf_data/EEG_Eyes_Open_Closed_0001_raw.edf"  # relative file path
exclud_channels = ['EEG CM-Pz','EEG X1-Pz','EEG X2-Pz','EEG X3-Pz'] # Exclude Channels

# signal_processing.py
raw = mne.io.read_raw_edf(filepath,preload=True,exclude=exclud_channels)
montage = mne.channels.make_standard_montage("standard_1020",.56).get_positions()['ch_pos']
chnls = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'C3', 'Cz', 'C4', 'P3', 'Pz', 'P4', 'O1', 'O2', 'T3', 'T5', 'T4', 'T6', 'A1', 'A2']
ch_pos= {}


for k in montage:
    for j in raw.info['ch_names']:
        if(k in j):
            ch_pos[k] = montage[k]

print(ch_pos)
# ch_pos = {'EEG Fp1-Pz': [-0.02892644, 0.08246248, -0.00686883],
#           'EEG Fp2-Pz': [0.02935449, 0.08342431, -0.00695727],
#           'EEG Fz-Pz': [0.00030679, 0.05749775, 0.06530994],
#           'EEG F3-Pz': [-0.04937287, 0.05219057, 0.04146064],
#           'EEG F4-Pz': [0.05093767, 0.05336348, 0.04010653],
#           'EEG F7-Pz': [-0.06904496, 0.04173805, -0.01122204],
#           'EEG F8-Pz': [0.07177697, 0.04365169, -0.01179199],
#           'EEG Cz-Pz': [0.00039395, -0.0090081, 0.09850636],
#           'EEG C3-Pz': [-0.06422518, -0.01143008, 0.06324241],
#           'EEG C4-Pz': [0.06595447, -0.01071135, 0.0624779],
#           'EEG T3-Pz': [-0.08270225, -0.01574103, -0.009184],
#           'EEG T4-Pz': [0.08360512, -0.01475994, -0.0093255],
#           'EEG T5-Pz': [-0.07117872, -0.07217947, -0.00244389],
#           'EEG T6-Pz': [0.07178935, -0.07180173, -0.00249597],
#           'EEG Pz-Pz': [0.00031907, -0.07970895, 0.08118295],
#           'EEG P3-Pz': [-0.05208847, -0.07742209, 0.05497033],
#           'EEG P4-Pz': [0.05470177, -0.07719843, 0.05558057],
#           'EEG O1-Pz': [-0.02890355, -0.1104998, 0.00868578],
#           'EEG O2-Pz': [0.02932531, -0.11021188, 0.00864746],
#           'EEG A1-Pz': [-0.08458405, -0.02455653, -0.06680753],
#           'EEG A2-Pz': [0.08430674, -0.02457579, -0.06685175],
#           #   'EEG None': [0, 0, 0],
#           'Trigger': [0, 0, 0]

#           }

# coord_frame = 'unknown'
# nasion = ([8.15612724e-06, 8.53062123e-02, -3.92899320e-02])
# lpa = ([-0.08458405, -0.0196432, -0.04715421])
# rpa = ([0.08430674, -0.01966246, -0.04719843])
# hsp = None
# hpi = None

# dsi_24_montage = mne.channels.make_dig_montage(ch_pos=ch_pos, nasion=nasion, lpa=lpa, rpa=rpa, hsp=hsp, hpi=hpi)
