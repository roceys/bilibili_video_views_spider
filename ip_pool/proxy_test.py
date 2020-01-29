import requests
from ip_pool import api_settings

with open(api_settings.FILE_NAME,'r') as f:
    # ip_list = [item.split(',')[0] for item in f.readlines()]
    ip_list = ['111.72.25.96:9999']

    for ip in ip_list:
        try:
            proxies = {
                'http': 'http://' + ip,
                'https': 'https://' + ip,
            }

            res = requests.get('https://httpbin.org/get',
                               proxies=proxies,
                               timeout=10)
            res.encoding = 'utf-8'
            print('>>>>>>>>>>>', res.content.decode())
        except Exception as e:
            print(e)

