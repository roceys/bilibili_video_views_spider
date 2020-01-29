import requests

proxies = {
            'http':  '123.149.141.158:9999',
            # 'https': '123.149.141.158:9999',
        }

res = requests.get('https://httpbin.org/get', proxies=proxies, timeout=8)
res.encoding = 'utf-8'

print( '>>>>>>>>>>>', res)
