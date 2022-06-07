import mne

#setting up the needed channels and positions with 'standard_alphabetic' montage
chnls = ['EEG P3-Pz', 'EEG C3-Pz', 'EEG F3-Pz', 'EEG Fz-Pz', 'EEG F4-Pz', 'EEG C4-Pz', 'EEG P4-Pz',
 'EEG Cz-Pz', 'EEG A1-Pz', 'EEG Fp1-Pz', 'EEG Fp2-Pz', 'EEG T3-Pz', 'EEG T5-Pz', 
 'EEG O1-Pz', 'EEG O2-Pz', 'EEG F7-Pz', 'EEG F8-Pz', 'EEG A2-Pz', 'EEG T6-Pz', 'EEG T4-Pz', 'Trigger']#


ch_pos = {
    'P3': [-0.05208847, -0.07742209, 0.05497033],
    'C3': [-0.06422518, -0.01143008, 0.06324241],
    'F3': [-0.04937287, 0.05219057, 0.04146064],
    'Fz': [0.00030679, 0.05749775, 0.06530994],
    'F4': [0.05093767, 0.05336348, 0.04010653],
    'C4': [0.06595447, -0.01071135, 0.0624779],
    'P4': [0.05470177, -0.07719843, 0.05558057],
    'Cz': [0.00039395, -0.0090081, 0.09850636],
    'A1': [-0.08458405, -0.02455653, -0.06680753],
    'Fp1': [-0.02892644, 0.08246248, -0.00686883],
    'Fp2': [0.02935449, 0.08342431, -0.00695727],
    'T3': [-0.08270225, -0.01574103, -0.009184],
    'T5': [-0.07117872, -0.07217947, -0.00244389],
    'O1': [-0.03, -0.12, 0.00868578],
    'O2': [0.03, -0.12, 0.00864746],
    'F7': [-0.06904496, 0.04173805, -0.01122204],
    'F8': [0.07177697, 0.04365169, -0.01179199],
    'A2': [0.08430674, -0.02457579, -0.06685175],
    'T6': [0.07178935, -0.07180173, -0.00249597],
    'T4': [0.08360512, -0.01475994, -0.0093255],
    'TRG': [0, 0, 0]
    }

    # 'Fp1': [-0.02892644, 0.08246248, -0.00686883],
    #       'Fp2': [0.02935449, 0.08342431, -0.00695727],
    #       'Fz': [0.00030679, 0.05749775, 0.06530994],
    #       'F3': [-0.04937287, 0.05219057, 0.04146064],
    #       'F4': [0.05093767, 0.05336348, 0.04010653],
    #       'F7': [-0.06904496, 0.04173805, -0.01122204],
    #       'F8': [0.07177697, 0.04365169, -0.01179199],
    #       'Cz': [0.00039395, -0.0090081, 0.09850636],
    #       'C3': [-0.06422518, -0.01143008, 0.06324241],
    #       'C4': [0.06595447, -0.01071135, 0.0624779],
    #       'T3': [-0.08270225, -0.01574103, -0.009184],
    #       'T4': [0.08360512, -0.01475994, -0.0093255],
    #       'T5': [-0.07117872, -0.07217947, -0.00244389],
    #       'T6': [0.07178935, -0.07180173, -0.00249597],
    #       'Pz': [0.00031907, -0.07970895, 0.08118295],
    #       'P3': [-0.05208847, -0.07742209, 0.05497033],
    #       'P4': [0.05470177, -0.07719843, 0.05558057],
    #       'O1': [-0.03, -0.12, 0.00868578],
    #       'O2': [0.03, -0.12, 0.00864746],
    #       'A1': [-0.08458405, -0.02455653, -0.06680753],
    #       'A2': [0.08430674, -0.02457579, -0.06685175],
    #       #'TRG': [0, 0, 0]

    #       }

coord_frame = 'unknown'
nasion = ([8.15612724e-06, 8.53062123e-02, -3.92899320e-02])
lpa = ([-0.08458405, -0.0196432, -0.04715421])
rpa = ([0.08430674, -0.01966246, -0.04719843])
hsp = None
hpi = None

dsi_24_montage = mne.channels.make_dig_montage(ch_pos=ch_pos, nasion=nasion, lpa=lpa, rpa=rpa, hsp=hsp, hpi=hpi)