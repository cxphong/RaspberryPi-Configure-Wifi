from ConfigParser import SafeConfigParser
from server import Server
import logging
from parser import Parser
import multiprocessing
import time
import constant
from cli import CLI
import sys
import os

global parser

def check_network_status():
    print ('check_network_status')

    ip = CLI.get_ip()
    if ip is None:
        CLI.start_accesspoint_mode()
        time.sleep(60)


# Receive request start access point
def on_receive_ap_command():
    close_tcp_server()
    CLI.start_accesspoint_mode()

    time.sleep(60)

    sys.exit()

# Receive request connect to SSID
def on_receive_connect_to_ssid(ssid_name, ssid_password):
    close_tcp_server()
    CLI.join_into_wifi(ssid_name, ssid_password)

    print 'Wait 90s'
    time.sleep(90)

    sys.exit()

def on_receive_data(data):
    print "data " + data
    global parser
    
    parser.parse(data)


def close_tcp_server():
    print "close socket"
    global server
    
    server.stop()

def startServer():
    global server
    
    check_network_status()
    
    # start tcp server
    logging.basicConfig(level=logging.DEBUG)
    p = SafeConfigParser()
    p.read(constant.HOME + '/config.ini')
    
    ip = CLI.get_ip()

    port = p.getint('TCP', 'port')
    cmd = "sudo fuser -k " + str(port) + "/tcp"
    print (cmd)
    os.popen(cmd)
    server = Server(ip, port, on_receive_data)
    
    try:
        print "Listening"
        server.start()
    except Exception, e:
        print str(e)
    finally:
        print "..."


def main():
    global parser
    global server

    parser = Parser(on_receive_ap_command, on_receive_connect_to_ssid)
    startServer()
    
    while (1):
        pass

    print 'Exit program'


if __name__ == "__main__":
    main()
