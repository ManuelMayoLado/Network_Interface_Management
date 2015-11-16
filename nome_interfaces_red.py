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

x = ni.interfaces()
pprint(get_connection_name_from_guid(x))