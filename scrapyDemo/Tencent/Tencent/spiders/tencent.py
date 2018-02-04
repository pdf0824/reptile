# -*- coding: utf-8 -*-
from scrapyDemo.Tencent.Tencent.items import TencentItem
import scrapy


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even' or @class='odd']")
        for node in node_list:
            item = TencentItem()
            item["positionName"] = node.xpath("./td/a/text()").extract()[0]
            item["positionLink"] = node.xpath("./td/a/@href").extract()[0]
            if len(node.xpath("./td[2]/text()")):
                item["positionType"] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item["positionType"] = ""
            item["peopleNumber"] = node.xpath("./td[3]/text()").extract()[0]
            item["workLocation"] = node.xpath("./td[4]/text()").extract()[0]
            item["publishTime"] = node.xpath("./td[5]/text()").extract()[0]
            yield item
        if len(response.xpath("//a[@class='noactive' and @id='next']")) == 0:
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/" + url, callback=self.parse)
