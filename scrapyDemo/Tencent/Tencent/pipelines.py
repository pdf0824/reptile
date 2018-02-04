# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TencentPipeline(object):
    def __init__(self):
        self.f = open("../data.json", 'wb')
        self.f.write("[\n".encode("utf-8"))

    def process_item(self, item, spider):
        result = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(result.encode('utf-8'))
        return item

    def close_spider(self, spider):
        self.f.write("]".encode("utf-8"))
        self.f.close()
