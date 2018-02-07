# coding = utf-8
from scrapy import cmdline
import redis
import time
import threading
r = redis.Redis(host='localhost', port='6379', db=0)
if "__main__" == __name__:
    # name = input("请输入爬虫名字:")
    # file_name = input("请输入保存的文件名字:")
    # command = "scrapy crawl " + name + " -o " + file_name
    # cmdline.execute(command.split())
    while True:
        command = "scrapy crawl " + 'yaohuo'
        cmdline.execute(command.split())
        print()
        time.sleep(10)
