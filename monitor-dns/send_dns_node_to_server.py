import requests
import psutil
import platform
import json
import time
import yaml
from logging import (getLogger, basicConfig)
import logging
from datetime import datetime
from pytz import timezone
import os
import sqlite3
logger = getLogger()


class Send_DNS_node(object):
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).timetuple()
    logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename='log/dns_node.log',
                    level=logging.INFO, filemode='a+')
    def __init__(self) :
        basicConfig(level="INFO")
        with open(f"config/config.yml", 'r') as f:
            yml_data = yaml.load(f, Loader=yaml.FullLoader)
        self.ip_address = yml_data['IP_address']
        self.authorization = yml_data['authorization']
        self.ssl = yml_data['ssl']
    
    def monitor(self):
        global id_dnsnode
        uname = platform.uname()
        Host_name= uname.node
        OS= f"{uname.system}, {uname.release}, {uname.version}, {uname.machine}"
        if_addrs = psutil.net_if_addrs()
        for interface_name,interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    if ('127.0.0.1' not in address.address):
                        IP_Address= f"{address.address}"
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    if ('00:00:00:00:00:00' not in address.address):
                        MAC_Address= f"{address.address}"
        headers = {
        'accept': 'application/json',
        'authorization': self.authorization,
        'X-CSRFToken': 'Zwh07hsHKtxmFMoEdweN6jcsETgYJykzyIaw9b7ytP7zOYsWi5vAjXYg6wry0oGl',
        }
        json_data = {
            'hostname': Host_name,
            'ip_address': IP_Address,
            'mac_address': MAC_Address,
            'os': OS,
        }
        check=0
        while check ==0:
            try:
                response = requests.post(f'{self.ssl}://{self.ip_address}/api/Dns_Node_List/', headers=headers, json=json_data)
                logging.info(f'Check response status code:\t{response.status_code}')
                check =1
            except:
                logging.warning(f'Server timeout error!!!')
                time.sleep(5)
        response_json=json.loads(response.text)
        with open(f"config/id_dns_node.txt",'w',encoding = 'utf-8') as f:
            try:
                id_dnsnode = str(response_json["id"])
                f.write(str(response_json["id"]))
            except:
                logging.warning(f'{response_json}')
        f.close()
    def put_link_adlist(self):
        conn = sqlite3.connect('/etc/pihole/gravity.db')
        cur = conn.cursor()
        sqlite_insert_query=f"""
                        insert into adlist (address,comment)
                        values ('{self.ssl}://{self.ip_address}/rawblacklist/{id_dnsnode}',
                                'DNS NODE') 
                        """
        cur.execute(sqlite_insert_query)
        conn.commit()
    def external_ip(self):
        with open("/etc/dnsmasq.d/01-pihole.conf",'a+',encoding = 'utf-8') as f:
            f.write("except-interface=nonexisting\n")
            f.close()
        os.system("pihole restartdns")

if __name__ == '__main__':
    DNS=Send_DNS_node()
    DNS.external_ip()
    DNS.monitor()     
    DNS.put_link_adlist()