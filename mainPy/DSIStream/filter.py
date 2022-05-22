from scipy.signal import butter, filtfilt

def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def filterAllCh(data):
    data.p3fil = butter_bandpass_filter(data.p3, 10, 30, 300)
    data.c3fil = butter_bandpass_filter(data.c3, 10, 30, 300)
    data.f3fil = butter_bandpass_filter(data.f3, 10, 30, 300)
    data.fzfil = butter_bandpass_filter(data.fz, 10, 30, 300)
    data.f4fil = butter_bandpass_filter(data.f4, 10, 30, 300)
    data.c4fil = butter_bandpass_filter(data.c4, 10, 30, 300)
    data.p4fil = butter_bandpass_filter(data.p4, 10, 30, 300)
    data.czfil = butter_bandpass_filter(data.cz, 10, 30, 300)
    #data.cmfil = butter_bandpass_filter(data.cm, 10, 30, 300)
    data.a1fil = butter_bandpass_filter(data.a1, 10, 30, 300)
    data.fp1fil = butter_bandpass_filter(data.fp1, 10, 30, 300)
    data.fp2fil = butter_bandpass_filter(data.fp2, 10, 30, 300)
    data.t3fil = butter_bandpass_filter(data.t3, 10, 30, 300)
    data.t5fil = butter_bandpass_filter(data.t5, 10, 30, 300)
    data.o1fil = butter_bandpass_filter(data.o1, 10, 30, 300)
    data.o2fil = butter_bandpass_filter(data.o2, 10, 30, 300)
    data.x3fil = butter_bandpass_filter(data.x3, 10, 30, 300)
    data.x2fil = butter_bandpass_filter(data.x2, 10, 30, 300)
    data.f7fil = butter_bandpass_filter(data.f7, 10, 30, 300)
    data.f8fil = butter_bandpass_filter(data.f8, 10, 30, 300)
    data.x1fil = butter_bandpass_filter(data.x1, 10, 30, 300)
    data.a2fil = butter_bandpass_filter(data.a2, 10, 30, 300)
    data.t6fil = butter_bandpass_filter(data.t6, 10, 30, 300)
    data.t4fil = butter_bandpass_filter(data.t4, 10, 30, 300)
    data.trgfil = data.trg #butter_bandpass_filter(data.trg, 10, 30, 300)


'''''
from numpy import genfromtxt
my_data = genfromtxt('rawDat.csv', delimiter=',')

y=butter_bandpass_filter(my_data,10,30,300)

import numpy
numpy.savetxt("doo.csv", y, delimiter=",") '''