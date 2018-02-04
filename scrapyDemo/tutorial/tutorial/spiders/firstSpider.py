import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class DemoSpider(CrawlSpider):
    name = "demo"
    allowed_domains = ["morvanzhou.github.io"]
    start_urls = [
        'https://morvanzhou.github.io/',
        'http://www.baidu.com/',
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
