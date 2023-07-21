import requests
import json
import time
import yaml
from logging import (getLogger, basicConfig)
import logging
from datetime import datetime
from pytz import timezone
logger = getLogger()
def file__(x):
        return x

class LogSenDnsMaster(object):
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).timetuple()
    logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename='log/log_dns_to_server.log',
                    level=logging.INFO, filemode='a+')
    def __init__(self) :
        basicConfig(level="INFO")
        with open(f"config/config.yml", 'r') as stream:
            yml_data = yaml.load(stream, Loader=yaml.FullLoader)
            self.ip_address = yml_data['IP_address']
            self.authorization = yml_data['authorization']
            self.ssl = yml_data['ssl']
        read_id_dns_server= open(f"config/id_dns_node.txt",'r',encoding = 'utf-8')
        self.dns_center_id = str(read_id_dns_server.readline ())


    def main(self):
        log_file = "/var/log/pihole.log"
        open_log=open(log_file, "r")
        headers = {
        'accept': 'application/json',
        'authorization': self.authorization,
        'X-CSRFToken': 'MVTXORjHng10PLJX7w5i3Jj3agnDCdDdl7MtQLYy6CBdYXNfc5m5gn5RCTydT3ZZ',
        }
        ############################################################################    
        split_log = open_log.read()
        # print(split_log)
        if len(split_log)!=0:
            json_data = {
                'dns_center_id': self.dns_center_id,
                'log_line': str(split_log)
            }

            check=0
            while check ==0:
                try:
                    response = requests.post(f'{self.ssl}://{self.ip_address}/api/LogToFilelList/', headers=headers, json=json_data)
                    print(response.status_code)
                    # print(f'{self.ssl}://{self.ip_address}/api/LogToFilelList/')
                    logging.info(f'{response.status_code}')
                    check =1
                    with open(log_file,'w',encoding = 'utf-8') as f:
                        f.write("")
                except:
                    logging.warning(f'Server timeout error!!!')
                    print(f'Server timeout error!!!')
                    time.sleep(5)
        ################################################################# 
            

if __name__ == '__main__':
    while True:
        try:
            Sl=LogSenDnsMaster()    
            Sl.main()
            time.sleep(5)
        except:
            pass
