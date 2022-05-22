import socket
import numpy as np
from DSIStream import filter, DSI24_ByteStream_Decoder as dc
import matplotlib.pyplot as plt

TCP_IP = "127.0.0.1"
TCP_PORT = 8844
BUFFER_SIZE = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
print("connected: ", s)

#pw = pg.plot()
x=np.linspace(0, 100, 300)
y = np.cos(x)
n=0


plt.ion()

figure, ax = plt.subplots(figsize=(8,6))

line1, = ax.plot(x, y)


y=np.array([])

plt.title("Dynamic Plot",fontsize=25)

plt.xlabel("X",fontsize=18)
plt.ylabel("uV",fontsize=18)
plt.ylim([-10000,10000])

while True:


    data = s.recv(BUFFER_SIZE)
    if data == None:
        break


    if data == "@ABCD".encode():
        data += s.recv(7)
        data += s.recv(dc.decodeBytes_packetLength(data))

        if dc.decodeBytes_packetType(data) == 5:
            dc.printEventPacket(data)

        elif dc.decodeBytes_packetType(data) == 1:
            #print(dc.decodeBytes_packetNumber(data))
            y=np.append(y, dc.decodeBytes_ChData(data, 23, 4))
            if len(y) == 300:
                yFilterd = filter.butter_bandpass_filter(y, 0.1, 20, 300)

                line1.set_xdata(x)
                line1.set_ydata(yFilterd)
                figure.canvas.draw()


                figure.canvas.flush_events()

                y=np.array([])
                n=0

        n+=1



s.close()