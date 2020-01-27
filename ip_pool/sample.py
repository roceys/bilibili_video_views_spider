import requests

from ip_pool import api_settings

addr = '123.52.97.130:9999'
ip = 'http://' + addr
ips = 'https://' + addr
proxies = {
    'http': '60.167.112.222:9999'
}

res = requests.get(
    api_settings.URL_TEST,
    timeout=10,
    proxies=proxies
)

b = 1
