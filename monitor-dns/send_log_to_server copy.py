import requests
import time
from datetime import date,datetime
import yaml
from logging import (getLogger, basicConfig)
import logging
from pytz import timezone
logger = getLogger()
class Send_log(object):
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

        

    def main(self):
        log_name = "/var/log/pihole.log"
        headers = {
        'accept': 'application/json',
        'authorization': self.authorization,
        'X-CSRFToken': 'MVTXORjHng10PLJX7w5i3Jj3agnDCdDdl7MtQLYy6CBdYXNfc5m5gn5RCTydT3ZZ',
        }
        while True:
            todays_date = date.today()
            log = open(log_name, "r")
            open_log=log.readlines()
            read_line = open(f"config/check_log.txt",'r',encoding = 'utf-8')
            a = int(read_line.readline ())
            if (a > len(open_log)):
                with open(f"config/check_log.txt",'w',encoding = 'utf-8') as f:
                    f.write("0")
                f.close()
                logging.info(f'Sang ngày mới!!!')

            read_line = open(f"config/check_log.txt",'r',encoding = 'utf-8')
            a = int(read_line.readline ())
            for line in open_log[a:]:
                arr_log = line.split(' ')
                try:
                    access_time = datetime.strptime(f'{todays_date.year} {arr_log[0]} {arr_log[1]} {arr_log[2]}', '%Y %b %d %H:%M:%S')
                except:
                    access_time = datetime.strptime(f'{todays_date.year} {arr_log[0]} {arr_log[2]} {arr_log[3]}', '%Y %b %d %H:%M:%S')
                read_id_dns_server= open(f"config/id_dns_node.txt",'r',encoding = 'utf-8')
                dns_center_id= str(read_id_dns_server.readline ())

                ip_client=arr_log[-1]
                domain=arr_log[-3]
                #########################################################################
                if (("gravity blocked" or "regex blacklisted" or "exactly blacklisted" )in line):
                    status=f"{arr_log[-5]} {arr_log[-4]}"
                elif (("NODATA-IPv6" or "<CNAME>" or "NXDOMAIN" or "<PTR>")in line):
                    status=arr_log[-4]
                else:
                    status=arr_log[-4]

                #############################################################################
                json_data = {
                    'dns_center_id': dns_center_id,
                    'ip_client': ip_client,
                    'domain': domain,
                    'access_time': str(access_time),
                    'status': status,
                }
                check=0
                while check ==0:
                    try:
                        response = requests.post(f'{self.ssl}://{self.ip_address}/api/Log_Detail_List/', headers=headers, json=json_data)
                        logging.info(f'Check response status code: {response.status_code}\n{line}')

                        check =1
                    except:
                        logging.warning(f'Server timeout error!!!')
                        time.sleep(5)
            ################################################################# 
            len_open_log=len(open_log)
            with open(f"config/check_log.txt",'w',encoding = 'utf-8') as f:
                f.write(str(len_open_log))
            read_line.close()
            f.close()
            time.sleep(1)
            

if __name__ == '__main__':
    Sl=Send_log()    
    Sl.main()
