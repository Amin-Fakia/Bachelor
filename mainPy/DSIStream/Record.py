import csv
import math


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier


def start_recording(conn):
    with open('mycsv.csv', 'w', newline='') as csvfile:
        fieldnames = ['Time', 'Fp1', 'Fp2', 'Fz',
                      'F3', 'F4', 'F7',
                      'F8', 'Cz', 'C3',
                      'C4', 'T3', 'T4',
                      'T5', 'T6', 'Pz',
                      'P3', 'P4', 'O1',
                      'O2', 'A1', 'A2',
                      'Trigger']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        s = 1 / 300
        n = 0

        while True:
            if conn.empty() is False:
                recData = conn.get()
                # print(data['Fp1 - Vref'])

                n += s
                # n = round_half_up(n, 4)

                writer.writerow({'Time': round_half_up(n, 4), 'Fp1': recData['Fp1'], 'Fp2': recData['Fp2'],
                                 'Fz': recData['Fz'],
                                 'F3': recData['F3'], 'F4': recData['F4'],
                                 'F7': recData['F7'],
                                 'F8': recData['F8'], 'Cz': recData['Cz'],
                                 'C3': recData['C3'],
                                 'C4': recData['C4'], 'T3': recData['T3'],
                                 'T4': recData['T4'],
                                 'T5': recData['T5'], 'T6': recData['T6'],
                                 'Pz': recData['Pz'],
                                 'P3': recData['P3'], 'P4': recData['P4'],
                                 'O1': recData['O1'],
                                 'O2': recData['O2'], 'A1': recData['A1'],
                                 'A2': recData['A2'],
                                 'Trigger': recData['Trigger']})


def start_recording_study(conn):
    with open('mycsv.csv', 'w',
              newline='') as csvfile:
        fieldnames = ['Time', 'Fp1', 'Fp2', 'Fz',
                      'F3', 'F4', 'F7',
                      'F8', 'Cz', 'C3',
                      'C4', 'T3', 'T4',
                      'T5', 'T6', 'Pz',
                      'P3', 'P4', 'O1',
                      'O2', 'A1', 'A2',
                      'Trigger']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        s = 1 / 300
        n = 0

        while True:
            if conn.empty() is False:
                recData = conn.get()
                # print(data['Fp1 - Vref'])

                n += s
                # n = round_half_up(n, 4)

                writer.writerow({'Time': recData['Time'], 'Fp1': recData['Fp1'], 'Fp2': recData['Fp2'],
                                 'Fz': recData['Fz'],
                                 'F3': recData['F3'], 'F4': recData['F4'],
                                 'F7': recData['F7'],
                                 'F8': recData['F8'], 'Cz': recData['Cz'],
                                 'C3': recData['C3'],
                                 'C4': recData['C4'], 'T3': recData['T3'],
                                 'T4': recData['T4'],
                                 'T5': recData['T5'], 'T6': recData['T6'],
                                 'Pz': recData['Pz'],
                                 'P3': recData['P3'], 'P4': recData['P4'],
                                 'O1': recData['O1'],
                                 'O2': recData['O2'], 'A1': recData['A1'],
                                 'A2': recData['A2'],
                                 'Trigger': recData['Trigger']})


import numpy as np
from pyedflib import highlevel
import pandas


def csv_to_edf(patientID, patientName, gender, birthdate, filepath):
    signals = []

    fieldnames = ['Time', 'Fp1', 'Fp2', 'Fz',
                  'F3', 'F4', 'F7',
                  'F8', 'Cz', 'C3',
                  'C4', 'T3', 'T4',
                  'T5', 'T6', 'Pz',
                  'P3', 'P4', 'O1',
                  'O2', 'A1', 'A2',
                  'Trigger']
    data = pandas.read_csv('mycsv.csv', delimiter=',',
                           names=fieldnames)

    signals.append(data.P3[1:].to_list())
    signals.append(data.C3[1:].to_list())
    signals.append(data.F3[1:].to_list())
    signals.append(data.Fz[1:].to_list())
    signals.append(data.F4[1:].to_list())
    signals.append(data.C4[1:].to_list())
    signals.append(data.P4[1:].to_list())
    signals.append(data.Cz[1:].to_list())
    signals.append(data.Pz[1:].to_list())
    signals.append(data.Fp1[1:].to_list())
    signals.append(data.Fp2[1:].to_list())
    signals.append(data.T3[1:].to_list())
    signals.append(data.T5[1:].to_list())
    signals.append(data.O1[1:].to_list())
    signals.append(data.O2[1:].to_list())
    # signals.append(data.X3[1:].to_list())
    # signals.append(data.X2[1:].to_list())
    signals.append(data.F7[1:].to_list())
    signals.append(data.F8[1:].to_list())
    # signals.append(data.X1[1:].to_list())
    signals.append(data.A1[1:].to_list())
    signals.append(data.A2[1:].to_list())
    signals.append(data.T6[1:].to_list())
    signals.append(data.T4[1:].to_list())
    signals.append(data.Trigger[1:].to_list())
    #signals.append(data.annotations[1:].to_list())

    x = np.array(signals)

    signals = x.astype(np.float_)
    annotations = []

    i = 1
    firstTRG = True
    for d in data.Trigger[1:]:
        if int(d) != 0 and firstTRG == True:
            annotations.append([float(data.Time[i]),0, str(data.Trigger[i])])
            firstTRG = False
        elif int(d) == 0:
            firstTRG = True
        i += 1

    channel_names = ['P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'Pz', 'Fp1', 'Fp2', 'T3', 'T5', 'O1', 'O2', 'F7',
                     'F8', 'A1', 'A2', 'T6', 'T4', 'Trigger']

    signal_headers = highlevel.make_signal_headers(channel_names, sample_rate=300, physical_min=signals.min(),
                                                   physical_max=signals.max())
    header = highlevel.make_header(patientname=patientName, gender=gender, birthdate=birthdate, patientcode=patientID)
    header['annotations'] = annotations
    highlevel.write_edf(filepath, signals, signal_headers, header)


#csv_to_edf('Alex', 'Alexander Stanchula', 'Male', '07.05.1998', 'test.edf')


