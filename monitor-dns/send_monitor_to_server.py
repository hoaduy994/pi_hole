import psutil
import requests
import time
import yaml
from logging import (getLogger, basicConfig)
from datetime import date,datetime
import pytz
import logging
from pytz import timezone
logger = getLogger()
class Send_monitor(object):
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).timetuple()
    logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename='log/monitor_dns_to_server.log',
                    level=logging.INFO, filemode='a+')
    def __init__(self) :
        basicConfig(level="INFO")
        with open(f"config/config.yml", 'r') as f:
            yml_data = yaml.load(f, Loader=yaml.FullLoader)
        self.ip_address = yml_data['IP_address']
        self.authorization = yml_data['authorization']
        self.ssl = yml_data['ssl']

    def main(self):
        headers = {
            'accept': 'application/json',
            'authorization': self.authorization,
            'X-CSRFToken': 'yeqgE9DsK0jIFSacX6H8EoR8L67T7VcqRdijuPgaqf61qNeNQTWbPO8F2OljmmX3',
        }


        read_id_dns_server= open(f"config/id_dns_node.txt",'r',encoding = 'utf-8')
        dns_center_id= str(read_id_dns_server.readline ())
        #################################################
        cpufreq = psutil.cpu_freq()
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            percentage
        cpu=f"{psutil.cpu_percent()}"
        svmem = psutil.virtual_memory()
        ram=f"{svmem.percent}"


        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if ("ext4" in f'{partition.fstype}'):
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    continue
                disk=f"{partition_usage.percent}"
        # get IO statistics since boot
        response = requests.get('http://192.168.72.131/admin/api.php?status&auth=998ed4d621742d0c2d85ed84173db569afa194d4597686cae947324aa58ab4bb')
        data = response.json()
        # print(response.text)
        if "status" in data and data["status"] == "enabled":
            status = "Enable"
        else:
            status = "Disable"

        json_data = {
        'dns_center_id': dns_center_id,
        'ram': ram,
        'cpu': cpu,
        'disk': disk,
        'status': status,
        }
        # print(json_data)
        check=0
        while check ==0:
            try:
                response = requests.post(f'{self.ssl}://{self.ip_address}/api/Monitor_DNS_List/', headers=headers, json=json_data)

                logging.info(f'Check response status code: {response.status_code} \t{json_data}')
                check =1
            except:
                logging.warning(f'Server timeout error!!!')
                time.sleep(60)
        time.sleep(60)

if __name__ == '__main__':
    while True:
        try:
            Sm=Send_monitor()  
            Sm.main()
        except:
            pass