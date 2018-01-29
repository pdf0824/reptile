# coding = utf-8
import scrapy
from scrapyDemo.tutorial.tutorial.items import TutorialItem


class YaoHuoDemo(scrapy.Spider):
    name = 'yaohuo'
    allowed_domains = ['http://yaohuo.me']
    start_urls = [
        'http://yaohuo.me/bbs/book_list.aspx?gettotal=2002&action=new',
    ]

    def parse(self, response):
        item = TutorialItem()
        item['title'] = response.xpath('//title/text()').extract()
        item['link'] = response.url
        # urls = response.xpath('//div/a/@href').extract
        # print(urls)
        for url in response.xpath('//div/a/@href').extract:
            yield scrapy.Request(url, self.parse)
        return item
