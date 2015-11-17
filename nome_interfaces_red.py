import netifaces as ni
import _winreg as wr
from pprint import pprint

def get_connection_name_from_guid(iface_guids):
    iface_names = []
    reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
    reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    for i in range(len(iface_guids)):
        try:
            reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
            iface_names.append(wr.QueryValueEx(reg_subkey, 'Name')[0].encode())
        except:
            pass
    return iface_names

interfaces = ni.interfaces()

for i in interfaces:
	if get_connection_name_from_guid([i]):
		try:
			if ni.ifaddresses(i)[2][0]['netmask']:
				print get_connection_name_from_guid([i]), ni.ifaddresses(i)[2][0]
		except:
			try: 
				if ni.ifaddresses(i)[2]:
					print get_connection_name_from_guid([i])
			except:
				pass
				
				
#### DNS

nslookup_info = os.popen("nslookup").read()
dns = re.findall('Address:(.+)',nslookup_info)