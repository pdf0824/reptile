# coding = utf-8
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from urllib import request
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from scrapyDemo.tutorial.tutorial.items import TutorialItem

base_url = 'https://yaohuo.me/'



class YaoHuoDemo(CrawlSpider):
    name = 'yaohuo'
    allowed_domains = ['yaohuo.me']
    start_urls = [
        'http://yaohuo.me/bbs/book_list.aspx?gettotal=2002&action=new',
    ]
    rules = (
        Rule(LinkExtractor(allow=('page',))),
        Rule(LinkExtractor(allow=('bbs-',), deny=('^/$', 'bbs.htm', '/Games/', '/adlink-24.html')),
             callback='parse_web'),
    )

    def start_requests(self):
        '''
        登陆
        :return:
        '''
        return [
            scrapy.FormRequest("https://yaohuo.me/waplogin.aspx",
                               method='post',
                               formdata={
                                   'logname': 'your name',
                                   'logpass': 'your password',
                                   'savesid': '1',
                                   'action': 'login',
                                   'classid': '0',
                                   'siteid': '0',
                                   'sid': '-3-0-0-0-0'

                               },
                               callback=self.logged)
        ]

    def logged(self, response):
        return [
            scrapy.Request(
                self.start_urls[0],
                callback=self.parse_web,
                errback=self.parse_err,
            )
        ]

    def parse_web(self, response):
        item = TutorialItem()
        urls = response.xpath('//div/a/@href').extract()
        item['title'] = response.xpath('//title/text()').extract()
        item['link'] = response.url
        print(item)
        for url in urls:
            if '/bbs-' in url:
                url = request.urljoin(base_url, url)
                yield scrapy.Request(url, self.parse_web)
        yield item

    def parse_err(self, response):
        self.logger.info('crawl {} failed'.format(response.url))
