# coding=utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random

base_url = 'https://baike.baidu.com'
his = ['/item/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0']

url = base_url + his[-1]
html = urlopen(url).read().decode("utf-8")
soup = BeautifulSoup(html, features='lxml')
print(soup.find('h1').get_text(), ' url:', his[-1])
i = 0

for i in range(20):
    url = base_url + his[-1]

    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    print(i, soup.find('h1').get_text(), '    url: ', his[-1])

    # find valid urls
    sub_urls = soup.find_all("a", {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})

    if len(sub_urls) != 0:
        his.append(random.sample(sub_urls, 1)[0]['href'])
    else:
        # no valid sub link found
        his.pop()
