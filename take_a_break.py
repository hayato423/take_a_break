import serial
from serial.tools import list_ports
import numpy as np
from datetime import datetime
from time import sleep
import pyautogui


bpm = 0
ibi = 0
bpm_prev = 0
ibi_prev = 0
pNN_data = np.zeros(30)
pNN_count = 0
checker = 1
datalist = 0
first_pNN = 0
pNN_ave = 0

def start_serial():
    ser = serial.Serial()
    ser.timeout = 0.1
    ports = list_ports.comports()
    devices = [info.device for info in ports]
    if len(devices) == 0:
        print("port not found")
        return None
    else:
        #ポート一覧表示
        for i,device in enumerate(devices):
            print("{}:{} ".format(i,device),end="")
        print("")
        device_num = int(input("Input device number:"))
        baudrates = [1200,2400,4800,9600,19200,38400,57600,115200]
        #ボードレート一覧表示
        for i,baudrate in enumerate(baudrates):
            print("{}:{} ".format(i,baudrate),end="")
        print("")
        baudrate_num = int(input("Input baundrate:"))
        #入力された設定を反映
        ser.port = devices[device_num]
        ser.baudrate = baudrates[baudrate_num]
        percentage = float(input('Input percentage:'))
    try:
        #接続テスト
        ser.open()
        return ser, percentage
    except:
        print("error when opening serial")
        return None


def get_data(ser):
    bin_data = ser.readline()
    if bin_data != b'':
        data = bin_data.decode()
        data = data.strip()
        return data
    else:
        return None



ser, percentage = start_serial()
print("start")
print('Please wait')
print(percentage)
while ser.is_open:
    data = get_data(ser)
    if data != None:
        if data[0] == "B":
            bpm = int(data[1:])
        elif data[0] == "Q":
            ibi = int(data[1:])
    if bpm != 0 and ibi != 0:
        if bpm == bpm_prev and ibi == ibi_prev:
            checker = 1
        if checker != 1:
            print(datetime.now().strftime('%H:%M:%S'))
            if ibi_prev != 0 and bpm_prev != 0:
                pNN_n = ibi - ibi_prev
                if pNN_n*pNN_n >= 2500:
                    pNN_data[pNN_count] = 1
                else:
                    pNN_data[pNN_count] = 0
                pNN_count += 1
                if pNN_count == 30:
                    datalist = 1
                    pNN_count = 0

                if datalist == 1:
                    pNN_sum = np.sum(pNN_data)
                    pNN_ave = pNN_sum / 30
                    if first_pNN == 0:
                        first_pNN = pNN_ave
                        print("\nfirst pNN is {}".format(first_pNN))
                    print("BPM:{}  pNN:{}".format(bpm,pNN_ave))
                    if pNN_ave < first_pNN * (percentage/100):
                        pyautogui.keyDown('win')
                        pyautogui.press('x')
                        pyautogui.keyUp('win')
                        pyautogui.press(['u','s'])
                        exit()
            ibi_prev = ibi
            bpm_prev = bpm
        checker = 0
ser.close()


