import json


class Parser:
    def __init__(self, callback_ap, callback_dhcp):
        self.callback_ap = callback_ap
        self.callback_dhcp = callback_dhcp
    
    def parse(self, data):
        try:
            d = json.loads(data)
            mode = d["mode"]
            
            if mode == "AP":
                self.callback_ap()
            
            elif mode == "DHCP":
                ssid_name = d["ssid_name"]
                ssid_password = d["ssid_password"]
                self.callback_dhcp(ssid_name, ssid_password)

        except Exception, e:
            print "Error: data format is incorrect"
            print str(e)




    




