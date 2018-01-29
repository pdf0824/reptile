# coding=utf-8
from bs4 import BeautifulSoup
import requests as req
import re
import os
import scrapy

URL = 'http://www.nationalgeographic.com.cn/animals/'

html = req.get(URL).text
soup = BeautifulSoup(html, 'lxml')
img_url = soup.find_all('img', {'src': re.compile('^http(.*)+\.jpg$')})
os.makedirs('./img/', exist_ok=True)
for img in img_url:
    url = img['src']
    r = req.get(url, stream=True)
    img_name = url.split('/')[-1]
    with open('./img/%s' % img_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)
        print('Save %s' % img_name)
