import requests
import math,random
from lxml import etree
import os,time,json

class Proxy():
    
    def __init__(self) -> None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
        self.headers = headers
        self.key = 'proxy'
        self.urls = [url for url in ['http://www.66ip.cn/{}.html'.format(i+1) for i in range(5)]  if requests.get(url=url,headers=headers).status_code == 200]
        self.proxies = []


    def get_content(self) -> None:
        for url in self.urls:
            res = requests.get(url=url,headers=self.headers,timeout=3)
            # print(requests.utils.get_encodings_from_content(res.text))
            content = res.content.decode(requests.utils.get_encodings_from_content(res.text)[0])
            self.parse(content)
        with open('./proxies.json','w+') as f:
            json.dump({'proxy':self.proxies},fp=f,ensure_ascii=False,indent=4)

    def parse(self,content) -> None:
        html = etree.HTML(content)
        result = html.xpath("//div[@align='center']/table/tr")[1:]
        for re in result:
            proxy_ip = re.xpath("./td/text()")[0]
            proxy_port = re.xpath("./td/text()")[1]
            proxy_address = re.xpath("./td/text()")[2]
            # proxy_style = re.xpath("./td/text()")[3]
            proxy_check_time = re.xpath("./td/text()")[4].split(' ')[0]
            # 将获取的代理存放至列表中
            self.proxies.append({
                'ip':proxy_ip,
                'port':proxy_port,
                'address':proxy_address,
                'check_time':proxy_check_time})

    def random(self) -> dict:
        self.get_content()
        rd = math.floor(random.random()*len(self.proxies))
        # print(rd)
        # print(self.proxies[rd])
        proxies = {
            'http': 'http://'+self.proxies[rd]['ip']+':'+self.proxies[rd]['port']
            # 'https': 'https://'+self.proxies[rd]['ip']+':'+self.proxies[rd]['port']
        }
        res = requests.get(url='https://www.baidu.com',headers=self.headers,proxies=proxies)
        if res.status_code != 200:
            self.random()
        else:
            return proxies

def get_proxies():
    proxies={}
    if os.path.exists('./proxies.json') and math.ceil(time.time())-os.stat('./proxies.json').st_mtime<=12*60*60:
        with open('./proxies.json','r+') as f:
            contents = f.readlines()
            proxy_list = json.loads(''.join(contents))['proxy']
            rd = math.floor(random.random()*len(proxy_list))
            proxies = {
                'http': 'http://'+proxy_list[rd]['ip']+':'+proxy_list[rd]['port'],
                # 'https': 'http://'+proxy_list[rd]['ip']+':'+proxy_list[rd]['port']
            }     
    else:
        proxy = Proxy()
        proxies = proxy.random()
    return proxies  

proxies=get_proxies()
res = requests.get(url='https://www.baidu.com',headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        },proxies=proxies)
print(proxies)

print(res)
