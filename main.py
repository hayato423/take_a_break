import serial
from serial.tools import list_ports

def start_serial():
    ser = serial.Serial()
    ser.timeout = 0.1
    ports = list_ports.comports()
    devices = [info.device for info in ports]
    if len(devices) == 0:
        print("port not found")
        return None
    else:
        for i,device in enumerate(devices):
            print("{}:{} ".format(i,device),end="")
        print("")
        print("input device number")
        device_num = int(input())
        baudrates = [1200,2400,4800,9600,19200,38400,57600,115200]
        for i,baudrate in enumerate(baudrates):
            print("{}:{} ".format(i,baudrate),end="")
        print("")
        print("input baundrate")
        baudrate_num = int(input())
        ser.port = devices[device_num]
        ser.baudrate = baudrates[baudrate_num]
    try:
        ser.open()
        return ser
    except:
        print("error when opening serial")
        return None


ser = start_serial()
while ser.is_open:
    data = ser.read_all()
    if data != b'':
        print(data)
ser.close()


