from ConfigParser import SafeConfigParser
import sys
import logging
import multiprocessing
import socket
import fcntl
import struct
import time
import os
import subprocess
from PhFile import PhFile
import netifaces

global nw_config
global server
global parser

class CLI(object):
    
    def modify_network_interface_no_password(ssid_name):
        return "auto lo\niface lo inet loopback\niface eth0 inet dhcp\nallow-hotplug wlan0\nauto wlan0\niface wlan0 inet dhcp\nwpa-ssid " + ssid_name + "\nwpa-key_mgmt NONE\nwpa-scan_ssid 1";

    @staticmethod
    def modify_network_interface(ssid_name,ssid_password):
        return "auto lo\niface lo inet loopback\niface eth0 inet dhcp\nallow-hotplug wlan0\nauto wlan0\niface wlan0 inet dhcp\nwpa-ssid " + ssid_name + "\nwpa-psk " + ssid_password + "\nwpa-scan_ssid 1";

    @staticmethod
    def write_configuration_interface(data):
	PhFile().saveText("/etc/network/interfaces", data)

    @staticmethod
    def join_into_wifi(ssid_name, ssid_password):
        data = CLI.modify_network_interface(ssid_name, ssid_password)
        CLI.write_configuration_interface(data)
        
    	subprocess.call("sudo service hostapd stop", shell=True);
    	subprocess.call("sudo service dnsmasq stop", shell=True);
    	subprocess.call("sudo update-rc.d hostapd disable", shell=True);
    	subprocess.call("sudo update-rc.d dnsmasq disable", shell=True);
    	subprocess.call("sudo ifdown wlan0", shell=True);
    	subprocess.call("sudo ifup wlan0", shell=True);
        subprocess.call("sudo dhclient -i wlan", shell=True)

    @staticmethod
    def start_accesspoint_mode():
        subprocess.call("sudo cp /home/pi/nhvcam_raspberry/interfaces /etc/network/", shell=True);
        subprocess.call("sudo ifdown wlan0", shell=True);
        subprocess.call("sudo ifup wlan0", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo service hostapd stop", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo service dnsmasq stop", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo service hostapd start", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo service dnsmasq start", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo update-rc.d hostapd enable", shell=True);
        time.sleep(1.5);
        subprocess.call("sudo update-rc.d dnsmasq enable", shell=True);

    @staticmethod
    def get_ip():
        try:
            ipstr = subprocess.check_output('ifconfig wlan0 | grep \'inet addr:\'', shell=True)
        except subprocess.CalledProcessError:
            print >> sys.stderr, "No IP address found. Device not connected?"
            return "none"
        except Exception as inst:
            print >> sys.stderr, type(inst)
            print >> sys.stderr, inst
            return "none"

        startIdx = ipstr.find('inet addr:')
        if (startIdx == -1):
             return "none"
        ipstr = ipstr[ipstr.find('inet addr:')+10:].split()[0]
        return ipstr

    @staticmethod
    def get_wifi_mode():
        try:
            modestr = subprocess.check_output('iwconfig wlan0 | grep Mode:', shell=True)
        except subprocess.CalledProcessError:
            print >> sys.stderr, "No interface found."
            return None
        except Exception as inst:
            print >> sys.stderr, type(inst)
            print >> sys.stderr, inst
            return None

        startIdx = modestr.find('Mode:')
        if (startIdx == -1):
            return None

        modestr = modestr[modestr.find('Mode:') + 5:].split()[0]
        return modestr

    @staticmethod
    def get_gateway(interface_name):
        gw = netifaces.gateways()

        try:
            if gw['default'][netifaces.AF_INET][1] == interface_name:
                gw['default'][netifaces.AF_INET][0]
            else:
                return None
        except:
            return None

    @staticmethod
    def get_connected_ssid_name():
        return os.popen("iwgetid -r").read().rstrip()

    @staticmethod
    def get_netmask():
        return os.popen("ifconfig wlan0 | grep 'inet addr:' | awk '{print $4}' | awk -F':' '{print $2}'").read().rstrip()

    @staticmethod
    def get_mac_address():
        return os.popen("ifconfig wlan0 | awk 'FNR==1 {print $5}'").read().rstrip()

    @staticmethod
    def get_ap_name():
        return os.popen("grep '^ssid=' /etc/hostapd/hostapd.conf | awk -F'=' '{ print $2 }'").read().rstrip()