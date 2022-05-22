import threading
import socket
import DSI24_ByteStream_Decoder as dc
import filter
import Ch_Data as ch





class streamThread(threading.Thread):
    def __init__(self, TCP_IP="127.0.1.0", TCP_PORT=8844):
        threading.Thread.__init__(self)
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.BUFFER_SIZE = 5

        self.data = ch.data()

        self.checkconn = False

    def clearall(self):
        self.data.p3.clear()
        self.data.c3.clear()
        self.data.f3.clear()
        self.data.fz.clear()
        self.data.f4.clear()
        self.data.c4.clear()
        self.data.p4.clear()
        self.data.cz.clear()
        self.data.cm.clear()
        self.data.a1.clear()
        self.data.fp1.clear()
        self.data.fp2.clear()
        self.data.t3.clear()
        self.data.t5.clear()
        self.data.o1.clear()
        self.data.o2.clear()
        self.data.x3.clear()
        self.data.x2.clear()
        self.data.f7.clear()
        self.data.f8.clear()
        self.data.x1.clear()
        self.data.a2.clear()
        self.data.t6.clear()
        self.data.t4.clear()
        self.data.trg.clear()

    def run(self):
        global dataFilt
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        print("connected: ", s)
        self.checkconn = True

        while True:

            recvData = s.recv(self.BUFFER_SIZE)
            if recvData is None:
                break

            if recvData == "@ABCD".encode():
                recvData += s.recv(7)
                recvData += s.recv(dc.decodeBytes_packetLength(recvData))

                if dc.decodeBytes_packetType(recvData) == 5:
                    dc.printEventPacket(recvData)

                elif dc.decodeBytes_packetType(recvData) == 1:
                    self.data.p3.append(dc.decodeBytes_ChData(recvData, 23, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.c3.append(dc.decodeBytes_ChData(recvData, 27, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.f3.append(dc.decodeBytes_ChData(recvData, 31, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.fz.append(dc.decodeBytes_ChData(recvData, 35, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.f4.append(dc.decodeBytes_ChData(recvData, 39, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.c4.append(dc.decodeBytes_ChData(recvData, 43, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.p4.append(dc.decodeBytes_ChData(recvData, 47, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.cz.append(dc.decodeBytes_ChData(recvData, 51, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.cm.append(dc.decodeBytes_ChData(recvData, 55, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.a1.append(dc.decodeBytes_ChData(recvData, 59, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.fp1.append(dc.decodeBytes_ChData(recvData, 63, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.fp2.append(dc.decodeBytes_ChData(recvData, 67, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.t3.append(dc.decodeBytes_ChData(recvData, 71, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.t5.append(dc.decodeBytes_ChData(recvData, 75, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.o1.append(dc.decodeBytes_ChData(recvData, 79, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.o2.append(dc.decodeBytes_ChData(recvData, 83, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.x3.append(dc.decodeBytes_ChData(recvData, 87, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.x2.append(dc.decodeBytes_ChData(recvData, 91, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.f7.append(dc.decodeBytes_ChData(recvData, 95, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.f8.append(dc.decodeBytes_ChData(recvData, 99, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.x1.append(dc.decodeBytes_ChData(recvData, 103, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.a2.append(dc.decodeBytes_ChData(recvData, 111, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.t6.append(dc.decodeBytes_ChData(recvData, 115, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.t4.append(dc.decodeBytes_ChData(recvData, 119, 4) - dc.decodeBytes_ChData(recvData, 107, 4))
                    self.data.trg.append(dc.decodeBytes_ChData(recvData, 123, 4) - dc.decodeBytes_ChData(recvData, 107, 4))

                    if len(self.data.p3) is 200:



                        self.data.p3fil = filter.butter_bandpass_filter(self.data.p3, 10, 30, 300)
                        self.data.c3fil = filter.butter_bandpass_filter(self.data.c3, 10, 30, 300)
                        self.data.f3fil = filter.butter_bandpass_filter(self.data.f3, 10, 30, 300)
                        self.data.fzfil = filter.butter_bandpass_filter(self.data.fz, 10, 30, 300)
                        self.data.f4fil = filter.butter_bandpass_filter(self.data.f4, 10, 30, 300)
                        self.data.c4fil = filter.butter_bandpass_filter(self.data.c4, 10, 30, 300)
                        self.data.p4fil = filter.butter_bandpass_filter(self.data.p4, 10, 30, 300)
                        self.data.czfil = filter.butter_bandpass_filter(self.data.cz, 10, 30, 300)
                        self.data.cmfil = filter.butter_bandpass_filter(self.data.cm, 10, 30, 300)
                        self.data.a1fil = filter.butter_bandpass_filter(self.data.a1, 10, 30, 300)
                        self.data.fp1fil = filter.butter_bandpass_filter(self.data.fp1, 10, 30, 300)
                        self.data.fp2fil = filter.butter_bandpass_filter(self.data.fp2, 10, 30, 300)
                        self.data.t3fil = filter.butter_bandpass_filter(self.data.t3, 10, 30, 300)
                        self.data.t5fil = filter.butter_bandpass_filter(self.data.t5, 10, 30, 300)
                        self.data.o1fil = filter.butter_bandpass_filter(self.data.o1, 10, 30, 300)
                        self.data.o2fil = filter.butter_bandpass_filter(self.data.o2, 10, 30, 300)
                        self.data.x3fil = filter.butter_bandpass_filter(self.data.x3, 10, 30, 300)
                        self.data.x2fil = filter.butter_bandpass_filter(self.data.x2, 10, 30, 300)
                        self.data.f7fil = filter.butter_bandpass_filter(self.data.f7, 10, 30, 300)
                        self.data.f8fil = filter.butter_bandpass_filter(self.data.f8, 10, 30, 300)
                        self.data.x1fil = filter.butter_bandpass_filter(self.data.x1, 10, 30, 300)
                        self.data.a2fil = filter.butter_bandpass_filter(self.data.a2, 10, 30, 300)
                        self.data.t6fil = filter.butter_bandpass_filter(self.data.t6, 10, 30, 300)
                        self.data.t4fil = filter.butter_bandpass_filter(self.data.t4, 10, 30, 300)
                        self.data.trgfil = filter.butter_bandpass_filter(self.data.trg, 10, 30, 300)

                        self.clearall()
        s.close()