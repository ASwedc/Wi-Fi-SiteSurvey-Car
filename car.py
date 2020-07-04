import os, csv, serial, time, threading
from flask import (Flask, Blueprint, request)
from scapy.all import *

from . import db
from .Sensor.GY955 import GY955
from .Module import motor
from .Module import beacon

# directory to save data
data_path = os.path.dirname(os.path.abspath(__file__)) + '/Data'

if not os.path.isdir(data_path):
    os.mkdir(data_path)

GY_path = data_path + '/GY-955'
if not os.path.isdir(GY_path):
    os.mkdir(GY_path)
    
beacon_path = data_path + '/Beacon_info'
if not os.path.isdir(beacon_path):
    os.mkdir(beacon_path)

# time now
now = int(time.time())
timeArray = time.localtime(now)
timeNow = time.strftime("%Y-%m-%d-%H:%M:%S", timeArray)

# file path to save GY-955 data
GY_path = GY_path + '/GY955-' + timeNow + '.csv'

# file path to save beacon information
beacon_path = beacon_path + '/BeaconInfo-' + timeNow + '.csv'

# caption of GY-955 data
with open(GY_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['TimeNow',
                     'Acc_X',    'Acc_Y',    'Acc_Z',
                     'Gyro_X',   'Gyro_Y',   'Gyro_Z',
                     'Magnet_X', 'Magnet_Y', 'Magnet_Z',
                     'Yaw',      'Roll',     'Pitch'])

# caption of beacon information
with open(beacon_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ssid","bssid","dBm","ntp"])

# monitor interface
iface = ''

# object of current app
app = Flask

# object of beacon information class
beacon = beacon

# object of car direction class
motor = motor.Direction()

# initial GY-955 module
'''ser = serial.Serial('/dev/serial0', 9600)
ser.write(serial.to_bytes([0xAA, 0x00, 0xAA]))'''

# the beginning Yaw data of GY-955
'''yaw = GY955(ser, GY_path)'''

# control thread work
adjust_run = False
hopper_run = False
beacon_run = False

def Current_app(current_app):
    global app
    app = current_app

def Adjust():
    global adjust_run
    global motor
    global yaw
    
    adjust_run = True
    print("start adjusting direction")
    while adjust_run:
        new_yaw = GY955(ser, GY_path)
        dif = new_yaw - yaw
        dc = motor.Update_dc(dif)
        time.sleep(0.5)
        
    print("stop adjusting direction")

def Hopper():
    global hopper_run
    global beacon
    global iface
    
    hopper_run = True
    print("start hoppering channel")
    while hopper_run:
        beacon.Hopper()

    print("stop hoppering channel")

def Beacon():
    global beacon_run
    global beacon
    global app
    
    with app.app_context():
        database = db.get_db()
        beacon_run = True
        print("start collecting beacon information")    
        while beacon_run:
            data = beacon.Sniff()
            database.execute('INSERT INTO Beacon (ssid, bssid, dBm, ntp, channel) VALUES (?, ?, ?, ?, ?)',
            (data[0], data[1], data[2], data[3], data[4]))
            database.commit()
            
        print("stop collecting beacon information")

bp = Blueprint('car', __name__)

# set interface to monitor mode
@bp.route('/iface', methods = ('GET', 'POST'))
def Iface():
    global beacon
    global iface
    global beacon_path
    
    if request.method == 'POST':
        iface = request.form['iface']
        
    os.system('ifconfig %s down' %iface)
    os.system('iwconfig %s mode monitor' %iface)
    os.system('ifconfig %s up' %iface)
    beacon = beacon.Beacon(iface, beacon_path)
    
    return '', 204
    
# control car direction
@bp.route('/forward')
def Forward():
    global motor
    motor.Dir('F')
    
    '''t1 = threading.Thread(target = Adjust)
    t1.start()'''
    
    t2 = threading.Thread(target = Hopper)
    t2.start()

    t3 = threading.Thread(target = Beacon)
    t3.start()
    
    return 'forward'

@bp.route('/back')
def Back():
    global motor
    motor.Dir('B')
    
    return 'back'

@bp.route('/left')
def Left():
    global motor
    motor.Dir('L')
    
    return 'left'

@bp.route('/right')
def Right():
    global motor
    motor.Dir('R')
    
    return 'right'

@bp.route('/stop')
def Stop():
    global motor
    global adjust_run
    global hopper_run
    global beacon_run
    
    motor.Dir('S')
    adjust_run = False
    hopper_run = False
    beacon_run = False
    
    return 'stop'