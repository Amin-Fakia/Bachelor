import struct

def decodeBytes_packetStart(ar, offset=0, len=5):
    result = ''

    for i in range(offset, len):
        result += chr(ar[i])

    return result


def decodeBytes_packetType(ar, offset=5):
    result = ar[offset]

    return result


def decodeBytes_packetLength(ar, offset=6):
    result = ar[offset] + ar[offset + 1]
    return result


def decodeBytes_packetNumber(ar, offset=8, len=4):
    result = 0

    for i in range(offset, len + offset):
        result += ar[i]

    return result

def printHeader(ar):

    header = ''

    packetStart = decodeBytes_packetStart(ar)
    packetType = decodeBytes_packetType(ar)
    packetLength = decodeBytes_packetLength(ar)
    packetNumber = decodeBytes_packetNumber(ar)

    header = str(packetStart) + ' Type: ' + str(packetType) + ' Length: ' + str(packetLength) \
             + ' Number: ' + str(packetNumber)

    print(header)


def decodeBytes_EventCode(ar, offset=12, len=4):
    result = 0

    for i in range(offset, len + offset):
        result += ar[i]

    return result


def decodeBytes_SendingNode(ar, offset=16, len=4):
    result = 0

    for i in range(offset, len + offset):
        result += ar[i]

    return result

def decodeBytes_LengthOfMessage(ar, offset=20, len=4):
    result = 0

    packetLength = decodeBytes_packetLength(ar)

    if packetLength+len >= offset:

        for i in range(offset, len + offset):
            result += ar[i]

    return result

def decodeBytes_Message(ar, offset=24):

    len = decodeBytes_LengthOfMessage(ar)
    result = ''

    for i in range(offset, len + offset):
        result += chr(ar[i])

    return result


def printEventPacket(ar):

    packet_type = decodeBytes_packetType(ar)

    if packet_type == 5:
        event_code = decodeBytes_EventCode(ar)
        sending_node = decodeBytes_SendingNode(ar)
        length_of_message = decodeBytes_LengthOfMessage(ar)
        message = decodeBytes_Message(ar)

        print('Event Code : '+ str(event_code) + ' Sending Node: '+str(sending_node)+' Length of Message: '+
              str(length_of_message)+' Message: '+str(message))


def decodeBytes_Timestamp(ar, offset=12, len=4):
    result = 0.0

    packetLength = decodeBytes_packetLength(ar)

    if packetLength + len >= offset:

        tpl = struct.unpack('>f', ar[12:16])
        result = tpl[0]

    return result


def decodeBytes_DataCounter(ar, offset=16, len=1):
    result = 0

    packetLength = decodeBytes_packetLength(ar)

    if packetLength + len >= offset:

        for i in range(offset, len + offset):
            result += ar[i]

    return result


def decodeBytes_ADCStatus(ar, offset=17, len=6):
    result = 0

    packetLength = decodeBytes_packetLength(ar)

    if packetLength + len >= offset:

        for i in range(offset, len + offset):
            result += ar[i]

    return result


def decodeBytes_ChData(ar, offset, len):
    result = 0.0

    packetLength = decodeBytes_packetLength(ar)

    if packetLength + len >= offset:

        tup = struct.unpack('>f', ar[offset:(offset+len)])
        result = tup[0]

    return result


def printsensorDataPacket(ar):

    packet_type = decodeBytes_packetType(ar)

    if packet_type == 1:

        timestamp = decodeBytes_Timestamp(ar)
        # dataCounter = decodeBytes_DataCounter(ar)
        # adcStatus = decodeBytes_ADCStatus(ar)

        # print('Timestamp: '+str(timestamp)+' Data Counter: '+str(dataCounter)+' ADC Status: '+
        #      str(adcStatus)+' Ch Data in uV: ')
        chnlsData = []
        for i in range(0, 25):
            if i not in [15,25,24,23,22,21]:
                chData = decodeBytes_ChData(ar, offset=23+i*4, len=4)
                chnlsData.append(chData)
            #print(chData)
        return chnlsData
            
