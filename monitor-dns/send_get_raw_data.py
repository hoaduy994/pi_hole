from pickle import TRUE
import requests
import time
from logging import (getLogger, basicConfig)
import yaml
import logging
import re
import sqlite3
import os
from datetime import datetime
from pytz import timezone
class RealRegexWhite:
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Ho_Chi_Minh')).timetuple()
    logging.basicConfig(format='%(asctime)s \t %(levelname)s \t %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename='log/black_white_to_server.log',
                    level=logging.INFO, filemode='a+')
    def __init__(self) :
        basicConfig(level="INFO")
        with open(f"config/config.yml", 'r') as f:
            yml_data = yaml.load(f, Loader=yaml.FullLoader)
            self.IP_address = yml_data['IP_address']
            self.authorization = yml_data['authorization']
            self.ssl = yml_data['ssl']
        read_id_dns_server= open(f"config/id_dns_node.txt",'r',encoding = 'utf-8')
        self.dns_center_id= str(read_id_dns_server.readline ())
        
    def PATCH_api(self,json_data,id_patch,url):
        headers = {
                    'accept': 'application/json',
                    'authorization': self.authorization,
                    'X-CSRFToken': 'U85MCfkXxeAJTr4HHzeXJOPZaPRNJ6EwUQcc2Hgl8idBPfxfWDWTLS79PjwcedmI',
                }
        return requests.patch(f'{self.ssl}://{self.IP_address}/api/{url}/{id_patch}/', headers=headers, json=json_data)
    
    def rawregexwhite(self):
        url = f"{self.ssl}://{self.IP_address}/rawregexwhite/{self.dns_center_id}"
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        conn = sqlite3.connect('/etc/pihole/gravity.db')
        cur = conn.cursor()
        sqlite_insert_query=f"""
                        DELETE FROM domainlist 
                        WHERE type = "2"
                        """
        
        cur.execute(sqlite_insert_query)
        conn.commit()
        for row in add_regexwhite: 
            sqlite_insert_query=f"""
                            insert into domainlist (type,domain,comment)
                            values ('2','{row}','RegexWhite') 
                            """
            cur.execute(sqlite_insert_query)
            conn.commit() 
        
    def rawwhitelist(self):
        url = f"{self.ssl}://{self.IP_address}/rawwhitelist/{self.dns_center_id}"
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        conn = sqlite3.connect('/etc/pihole/gravity.db')
        cur = conn.cursor()
        sqlite_insert_query=f"""
                        DELETE FROM domainlist 
                        WHERE type = "0"
                        """
        cur.execute(sqlite_insert_query)
        conn.commit()
        for row in add_regexwhite: 
            sqlite_insert_query=f"""
                            insert into domainlist (type,domain,comment)
                            values ('0',"{row}",'White') 
                            """
            cur.execute(sqlite_insert_query)
            conn.commit() 

            
    def rawblacklist(self):
        url = f"{self.ssl}://{self.IP_address}/rawblacklist/{self.dns_center_id}"
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        conn = sqlite3.connect('/etc/pihole/gravity.db')
        cur = conn.cursor()
        sqlite_insert_query=f"""
                        DELETE FROM domainlist 
                        WHERE type = "1"
                        """
        cur.execute(sqlite_insert_query)
        conn.commit()
        for row in add_regexwhite: 
            sqlite_insert_query=f"""
                            insert into domainlist (type,domain,comment)
                            values ('1',"{row}",'Black') 
                            """
            cur.execute(sqlite_insert_query)
            conn.commit() 
    
    def rawregexblack(self):
        url = f"{self.ssl}://{self.IP_address}/rawregexblack/{self.dns_center_id}"
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        conn = sqlite3.connect('/etc/pihole/gravity.db')
        cur = conn.cursor()
        sqlite_insert_query=f"""
                        DELETE FROM domainlist 
                        WHERE type = "3"
                        """
        cur.execute(sqlite_insert_query)
        conn.commit()
        for row in add_regexwhite: 
            sqlite_insert_query=f"""
                            insert into domainlist (type,domain,comment)
                            values ('3',"{row}",'White') 
                            """
            cur.execute(sqlite_insert_query)
            conn.commit() 
    
    def rawdnsrecords(self):
        url = f"{self.ssl}://{self.IP_address}/rawdnsrecords/{self.dns_center_id}"  
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        for row in add_regexwhite:
            with open("/etc/pihole/custom.list", mode ="a",encoding = 'utf-8') as f:
                f.write(f"{row}\n")
            f.close()
        os.system("pihole restartdns")
        
    def rawdnsforwarder(self):
        url = f"{self.ssl}://{self.IP_address}/rawdnsforwarder/{self.dns_center_id}"  
        x = requests.get(url)
        data_dns=str(x.text).split("\n")
        add_regexwhite=[]
        for row in data_dns:
            if (("<" not in row) and("        "not in row)):
                add_regexwhite.append(row)
        file = open("/etc/dnsmasq.d/01-pihole.conf", "r").read()
        dnsmasq_pihole= file.split("\n")
        for row in dnsmasq_pihole:     
            if "server" in row:
                file=file.replace(row,'')
        for row in add_regexwhite:
            file+=f"{row}\n"
        with open("/etc/dnsmasq.d/01-pihole.conf",'w',encoding = 'utf-8') as f:
            f.write(file)
    def main(self):
        headers = {
            'accept': 'application/json',
            'authorization': self.authorization,
            'X-CSRFToken': 'U85MCfkXxeAJTr4HHzeXJOPZaPRNJ6EwUQcc2Hgl8idBPfxfWDWTLS79PjwcedmI',
        }
        check = True
        while check:
            try:
                response = requests.get(f'{self.ssl}://{self.IP_address}/api/Dns_Node_List/{self.dns_center_id}/', headers=headers)
                data=response.json()
                check = False
            except:
                check = True
                logging.warning(f'Server disconnect!!!')
                time.sleep(30)
        # Nếu is_close == None : Có lệnh thêm doman vào Domain Pihole
        # Nếu is_close == True : Domain đã tồn tại trong DB của Pihole 
        # Nếu is_close == False : Có lệnh xoá từ Server node
        # Nếu type == 0 : Đây là white
        # Nếu type == 1 : Đây là black
        # Nếu type == 2 : Đây là regex_white
        # Nếu type == 3 : Đây là regex_black
        
        if not data['is_raw_black_list']:
            RealRegexWhite.rawblacklist(self)
            json_data={
                        "is_raw_black_list":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            os.system("pihole -g")
            logging.info(f'Raw Black List\tStatus Code::{s.status_code}')
        
        if not data['is_raw_regex_black']:
            json_data={
                        "is_raw_regex_black":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            logging.info(f'Raw Regex Black\tStatus Code::{s.status_code}')
        
        if not data['is_raw_white_list']:
            RealRegexWhite.rawwhitelist(self)
            json_data={
                        "is_raw_white_list":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            logging.info(f'Raw White List\tStatus Code::{s.status_code}')
        
        if not data['is_raw_regex_white_list']:
            RealRegexWhite.rawregexwhite(self)
            json_data={
                        "is_raw_regex_white_list":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            logging.info(f'Raw Regex White\tStatus Code::{s.status_code}')
            
        if not data['is_dns_dnsrecord']:
            RealRegexWhite.rawdnsrecords(self)
            json_data={
                        "is_dns_dnsrecord":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            logging.info(f'Raw Dns Records\tStatus Code:{s.status_code}')

        if not data['is_dns_forwarder']:
            RealRegexWhite.rawdnsforwarder(self)
            json_data={
                        "is_dns_forwarder":True
                        }
            s=RealRegexWhite.PATCH_api(self,json_data=json_data,id_patch=self.dns_center_id,url='Dns_Node_List')
            os.system("pihole restartdns")
            logging.info(f'Raw DNS Rorwarder\tStatus Code::{s.status_code}')
if __name__ == '__main__':
    Sl=RealRegexWhite()
    while True:
        try:
            Sl.main()
            time.sleep(5)
        except:
            pass
    # Sl.rawdnsrecords()