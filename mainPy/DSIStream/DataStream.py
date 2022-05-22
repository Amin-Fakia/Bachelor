import socket
import os
import sys
import inspect
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# print(currentdir)
# sys.path.insert(0, parentdir) 

import DSI24_ByteStream_Decoder as dc
from DSI import filter
import Ch_Data as ch

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

def clearall(data):
    data.p3.clear()#0
    data.c3.clear()#1
    data.f3.clear()#2
    data.fz.clear()#3
    data.f4.clear()#4
    data.c4.clear()#5
    data.p4.clear()#6
    data.cz.clear()#7
    data.cm.clear()#8
    data.a1.clear()#9
    data.fp1.clear()# 10
    data.fp2.clear() # 11
    data.t3.clear()# 12
    data.t5.clear()# 13
    data.o1.clear()# 14
    data.o2.clear() # 15
    data.x3.clear()# 16
    data.x2.clear()#17
    data.f7.clear()#18
    data.f8.clear()#19
    data.x1.clear()#20
    data.a2.clear()#21
    data.t6.clear()#22
    data.t4.clear()#23
    data.trg.clear()#24


def streamData(conn, connRec, isRec):
    BUFFER_SIZE = 5
    TCP_IP = "127.0.1.0"
    TCP_PORT = 8844

    data = ch.data()

    start = False

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("connected: ", s)
    checkconn = True
    rec = False

    while checkconn is True:

        recvData = s.recv(BUFFER_SIZE)
        if recvData is None:
            break

        if recvData == "@ABCD".encode():
            recvData += s.recv(7)
            recvData += s.recv(dc.decodeBytes_packetLength(recvData))

            if dc.decodeBytes_packetType(recvData) == 5:
                dc.printEventPacket(recvData)

            elif dc.decodeBytes_packetType(recvData) == 1:

                vref = (dc.decodeBytes_ChData(recvData, 107, 4) + dc.decodeBytes_ChData(recvData, 59, 4)) / 2

                data.p3.append(dc.decodeBytes_ChData(recvData, 23, 4))#- vref)
                data.c3.append(dc.decodeBytes_ChData(recvData, 27, 4))#- vref)
                data.f3.append(dc.decodeBytes_ChData(recvData, 31, 4))#- vref)
                data.fz.append(dc.decodeBytes_ChData(recvData, 35, 4))#- vref)
                data.f4.append(dc.decodeBytes_ChData(recvData, 39, 4))#- vref)
                data.c4.append(dc.decodeBytes_ChData(recvData, 43, 4))#- vref)
                data.p4.append(dc.decodeBytes_ChData(recvData, 47, 4))#- vref)
                data.cz.append(dc.decodeBytes_ChData(recvData, 51, 4))#- vref)
                data.cm.append(dc.decodeBytes_ChData(recvData, 55, 4))#- vref)
                data.a1.append(dc.decodeBytes_ChData(recvData, 59, 4))#- vref)
                data.fp1.append(dc.decodeBytes_ChData(recvData, 63, 4))# - vref)
                data.fp2.append(dc.decodeBytes_ChData(recvData, 67, 4))# - vref)
                data.t3.append(dc.decodeBytes_ChData(recvData, 71, 4))#- vref)
                data.t5.append(dc.decodeBytes_ChData(recvData, 75, 4))#- vref)
                data.o1.append(dc.decodeBytes_ChData(recvData, 79, 4))#- vref)
                data.o2.append(dc.decodeBytes_ChData(recvData, 83, 4))#- vref)
                data.x3.append(dc.decodeBytes_ChData(recvData, 87, 4))#- vref)
                data.x2.append(dc.decodeBytes_ChData(recvData, 91, 4))#- vref)
                data.f7.append(dc.decodeBytes_ChData(recvData, 95, 4))#- vref)
                data.f8.append(dc.decodeBytes_ChData(recvData, 99, 4))#- vref)
                data.x1.append(dc.decodeBytes_ChData(recvData, 103, 4))#- vref)
                data.a2.append(dc.decodeBytes_ChData(recvData, 107, 4))#- vref)
                data.t6.append(dc.decodeBytes_ChData(recvData, 111, 4))#- vref)
                data.t4.append(dc.decodeBytes_ChData(recvData, 115, 4))#- vref)
                data.trg.append(dc.decodeBytes_ChData(recvData, 119, 4))# - vref)

                if isRec.empty() is False:
                    start = isRec.get()

                if start is True:


                    recData = ({'Time': 0, 'Fp1 - Vref': dc.decodeBytes_ChData(recvData, 63, 4), 'Fp2 - Vref': dc.decodeBytes_ChData(recvData, 67, 4), 'Fz - Vref': dc.decodeBytes_ChData(recvData, 35, 4),
                                'F3 - Vref': dc.decodeBytes_ChData(recvData, 31, 4), 'F4 - Vref': dc.decodeBytes_ChData(recvData, 39, 4), 'F7 - Vref': dc.decodeBytes_ChData(recvData, 95, 4),
                                'F8 - Vref': dc.decodeBytes_ChData(recvData, 99, 4), 'Cz - Vref': dc.decodeBytes_ChData(recvData, 51, 4), 'C3 - Vref': dc.decodeBytes_ChData(recvData, 27, 4),
                                'C4 - Vref': dc.decodeBytes_ChData(recvData, 43, 4), 'T3 - Vref': dc.decodeBytes_ChData(recvData, 71, 4), 'T4 - Vref': dc.decodeBytes_ChData(recvData, 115, 4),
                                'T5 - Vref': dc.decodeBytes_ChData(recvData, 75, 4), 'T6 - Vref': dc.decodeBytes_ChData(recvData, 111, 4), 'Pz - Vref': dc.decodeBytes_ChData(recvData, 55, 4),
                                'P3 - Vref': dc.decodeBytes_ChData(recvData, 23, 4), 'P4 - Vref': dc.decodeBytes_ChData(recvData, 47, 4), 'O1 - Vref': dc.decodeBytes_ChData(recvData, 79, 4),
                                'O2 - Vref': dc.decodeBytes_ChData(recvData, 83, 4), 'A1 - Vref': dc.decodeBytes_ChData(recvData, 59, 4), 'A2 - Vref': dc.decodeBytes_ChData(recvData, 107, 4),
                                'Trigger': dc.decodeBytes_ChData(recvData, 119, 4)})

                    connRec.put(recData)

                if len(data.p3) == 150:
                    data.p3fil = filter.butter_bandpass_filter(data.p3, 10, 30, 300)
                    data.c3fil = filter.butter_bandpass_filter(data.c3, 10, 30, 300)
                    data.f3fil = filter.butter_bandpass_filter(data.f3, 10, 30, 300)
                    data.fzfil = filter.butter_bandpass_filter(data.fz, 10, 30, 300)
                    data.f4fil = filter.butter_bandpass_filter(data.f4, 10, 30, 300)
                    data.c4fil = filter.butter_bandpass_filter(data.c4, 10, 30, 300)
                    data.p4fil = filter.butter_bandpass_filter(data.p4, 10, 30, 300)
                    data.czfil = filter.butter_bandpass_filter(data.cz, 10, 30, 300)
                    #data.cmfil = filter.butter_bandpass_filter(data.cm, 10, 30, 300)
                    data.a1fil = filter.butter_bandpass_filter(data.a1, 10, 30, 300)
                    data.fp1fil = filter.butter_bandpass_filter(data.fp1, 10, 30, 300)
                    data.fp2fil = filter.butter_bandpass_filter(data.fp2, 10, 30, 300)
                    data.t3fil = filter.butter_bandpass_filter(data.t3, 10, 30, 300)
                    data.t5fil = filter.butter_bandpass_filter(data.t5, 10, 30, 300)
                    data.o1fil = filter.butter_bandpass_filter(data.o1, 10, 30, 300)
                    data.o2fil = filter.butter_bandpass_filter(data.o2, 10, 30, 300)
                    data.x3fil = filter.butter_bandpass_filter(data.x3, 10, 30, 300)
                    data.x2fil = filter.butter_bandpass_filter(data.x2, 10, 30, 300)
                    data.f7fil = filter.butter_bandpass_filter(data.f7, 10, 30, 300)
                    data.f8fil = filter.butter_bandpass_filter(data.f8, 10, 30, 300)
                    data.x1fil = filter.butter_bandpass_filter(data.x1, 10, 30, 300)
                    data.a2fil = filter.butter_bandpass_filter(data.a2, 10, 30, 300)
                    data.t6fil = filter.butter_bandpass_filter(data.t6, 10, 30, 300)
                    data.t4fil = filter.butter_bandpass_filter(data.t4, 10, 30, 300)
                    data.trgfil = filter.butter_bandpass_filter(data.trg, 10, 30, 300)

                    #print(data.p3fil)

                    conn.put(data)
                    clearall(data)
    s.close()
