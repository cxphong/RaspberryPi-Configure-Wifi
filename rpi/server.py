import multiprocessing
import socket
from cli import CLI

class Server(object):
    def __init__(self, hostname, port, callback):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.callback = callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def stop(self):
        print "stop"
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def start(self):
        self.logger.debug("listening")
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=self.__handle, args=(conn, address))
            process.daemon = True
            process.start()
            self.logger.debug("Started process %r", process)
    
    def __handle(self, connection, address):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger("process-%r" % (address,))
        try:
            logger.debug("Connected %r at %r", connection, address)
            while True:
                if CLI.get_wifi_mode() == "Master":
                    ssid = CLI.get_ap_name()
                    mac = CLI.get_mac_address()
                    str = "{mode:\"AP\", ssid=\"" + ssid + "\", mac: \"" + mac + "\"}"
                    connection.sendall(str)
                elif CLI.get_wifi_mode() == "Managed":
                    ip = CLI.get_ip()
                    netmask = CLI.get_netmask()
                    gateway = CLI.get_gateway('wlan0')
                    ssid = CLI.get_connected_ssid_name()

                    if ip is None:
                        ip = ""

                    if netmask is None:
                        netmask = ""

                    if gateway is None:
                        gateway = ""

                    if ssid is None:
                        ssid = ""

                    str = "{mode: \"CLIENT\", ip: \"" + ip + "\", netmask: \"" + netmask + "\", gateway: \"" + gateway +"\", ssid: \"" + ssid + "\"}"
                    connection.sendall(str)
                
                data = connection.recv(1024)
                if data == "":
                    logger.debug("Socket closed remotely")
                    break
                self.callback(data)
                    
            logger.debug("Sent data")
        except:
            logger.exception("Problem handling request")
        finally:
            logger.debug("Closing socket")
            connection.close()
