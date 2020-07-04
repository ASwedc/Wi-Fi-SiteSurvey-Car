import os
import csv
import time
import serial

# write GY-955 module data to csv
def GY955(ser, file_path):
#----------------------------------------------Accelerometer
    ser.write(serial.to_bytes([0xA5, 0x15, 0xBA]))

    data = ser.read(12)
    str = "".join("{:02X}".format(c) for c in data)
    
    a = int(str[8:12], 16)
    if (str[8] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Acc_X = a

    a = int(str[12:16], 16)
    if (str[12] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Acc_Y = a
    
    a = int(str[16:20], 16)
    if (str[16] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Acc_Z = a

#----------------------------------------------Gyroscope
    ser.write(serial.to_bytes([0xA5, 0x25, 0xCA]))

    data = ser.read(12)
    str = "".join("{:02X}".format(c) for c in data)
    
    a = int(str[8:12], 16)
    if (str[8] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Gyro_X = a
    
    a = int(str[12:16], 16)
    if (str[12] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Gyro_Y = a
    
    a = int(str[16:20], 16)
    if (str[16] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Gyro_Z = a

#----------------------------------------------Magnetometer
    ser.write(serial.to_bytes([0xA5, 0x35, 0xDA]))

    data = ser.read(12)
    str = "".join("{:02X}".format(c) for c in data)
    
    a = int(str[8:12], 16)
    if (str[8] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Magnet_X = a
    
    a = int(str[12:16], 16)
    if (str[12] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Magnet_Y = a
    
    a = int(str[16:20], 16)
    if (str[16] != 'F'):
        a = a / 16
    else:
        a = (65535 - a + 1) /-16
    Magnet_Z = a

#----------------------------------------------Euler
    ser.write(serial.to_bytes([0xA5, 0x45, 0xEA]))

    data = ser.read(12)
    str = "".join("{:02X}".format(c) for c in data)
    
    a = int(str[8:12], 16)
    if (str[8] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Yaw = a
    
    a = int(str[12:16], 16)
    if (str[12] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Roll = a
    
    a = int(str[16:20], 16)
    if (str[16] != 'F'):
        a = a / 100
    else:
        a = (65535 - a + 1) /-100
    Pitch = a

#----------------------------------------------Timestamp
    now = int(time.time())
    timeArray = time.localtime(now)
    timeNow = time.strftime("%H:%M:%S", timeArray)
    
#----------------------------------------------CSV
    with open(file_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timeNow, Acc_X, Acc_Y, Acc_Z, Gyro_X, Gyro_Y, Gyro_Z, Magnet_X, Magnet_Y, Magnet_Z, Yaw, Roll, Pitch])
        
    return Yaw
    
if __name__ == '__main__':
    # initial GY-955 module
    ser = serial.Serial('/dev/serial0', 9600)
    ser.write(serial.to_bytes([0xAA, 0x00, 0xAA]))
    
    # the file path to save GY-955 data
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = absolute_path + '/output.csv'
    
    # write caption
    with open(file_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['TimeNow', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z', 'Magnet_X', 'Magnet_Y', 'Magnet_Z', 'Yaw', 'Roll', 'Pitch'])
    
    for i in range(0, 100):
        GY955(ser, file_path)