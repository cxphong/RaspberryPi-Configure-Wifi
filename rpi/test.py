
class CLI(object):
	
	@staticmethod
	def modify_network_interface_no_password(ssid_name):
		return "auto lo\niface lo inet loopback\niface eth0 inet dhcp\nallow-hotplug wlan0\nauto wlan0\niface wlan0 inet dhcp\nwpa-ssid " + ssid_name + "\nwpa-key_mgmt NONE\nwpa-scan_ssid 1";
	
	@staticmethod
    	def modify_network_interface(ssid_name,ssid_password):
    		return "auto lo\niface lo inet loopback\niface eth0 inet dhcp\nallow-hotplug wlan0\nauto wlan0\niface wlan0 inet dhcp\nwpa-ssid " + ssid_name + "\nwpa-psk " + ssid_password + "\nwpa-scan_ssid 1";

print CLI.modify_network_interface_no_password('Fiot_09')
print CLI.modify_network_interface('Fiot_09', 'passnhucu')

