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
        ipstr = ''
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

CLI.join_into_wifi('Fiot_09', 'passnhucufsfsfs')
print CLI.get_ip()
