import requests

ip = '223.199.26.142:9999'
proxies = {
    'http': 'http://' + ip,
    'https': 'https://' + ip,
}

res = requests.get('https://httpbin.org/get',
                   proxies=proxies,
                   timeout=8)
res.encoding = 'utf-8'

print('>>>>>>>>>>>', res.content.decode())
