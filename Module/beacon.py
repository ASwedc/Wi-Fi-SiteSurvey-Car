import os, time, csv, threading

from scapy.all import *

class Beacon():
    def __init__(self, iface = "wlan0", path = 'Beacon_info.csv'):
        self.iface = iface
        self.file_path = path
        self.ssid = ""
        self.bssid = ""
        self.hssid = ""
        self.dBm = ""
        self.ntp = ""
        self.channel = 0

    # change channel
    def Hopper(self):
        self.channel= (self.channel % 11) + 1 
        os.system('iwconfig %s channel %d' % (self.iface, self.channel))
        time.sleep(0.1)
    
    # beacon information will be collect
    def Info(self, pkt):
        if pkt.haslayer(Dot11Beacon):
                self.ssid = str(pkt.getlayer(Dot11Elt).info)
                self.bssid = str(pkt.getlayer(Dot11FCS).addr2)
                self.hssid = pkt.getlayer(Dot11Elt).info
                self.dBm = str(pkt.getlayer(RadioTap).dBm_AntSignal)
                self.ntp = str("%.3f" %(time.time()))
                
                if self.hssid == '' or pkt.getlayer(Dot11Elt).ID != 0:
                    print ("Hidden Network Detected")
                   
                with open(self.file_path, 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([self.ssid, self.bssid, self.dBm, self.ntp, self.channel])
    
    # get beacon information what "Info" function want
    def Sniff(self):
        sniff(iface = self.iface ,prn=self.Info, timeout = 4.4)
        data = [self.ssid, self.bssid, self.dBm, self.ntp, self.channel]
        
        return data