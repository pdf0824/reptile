# coding = utf-8
from scrapy import cmdline

if "__main__" == __name__:
    name = input("请输入爬虫名字:")
    file_name = input("请输入保存的文件名字:")
    command = "scrapy crawl " + name + " -o " + file_name
    cmdline.execute(command.split())
