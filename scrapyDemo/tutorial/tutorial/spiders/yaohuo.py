# coding = utf-8
import scrapy
import redis

from scrapyDemo.tutorial.tutorial.items import TutorialItem

base_url = 'https://yaohuo.me'
page_count = 0
r = redis.Redis(host='localhost', port='6379', db=0)


class YaoHuoDemo(scrapy.Spider):
    name = 'yaohuo'
    allowed_domains = ['yaohuo.me']
    start_urls = [
        'https://yaohuo.me/bbs/book_list.aspx?action=new&siteid=1000&classid=0&getTotal=2002&page=1',
    ]

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
        node_list = response.xpath("//div[@class='line1' or @class='line2']/a[1]")
        for node in node_list:
            item = TutorialItem()
            item["title"] = node.xpath("./text()").extract()[0]
            item['link'] = base_url + node.xpath("./@href").extract()[0]
            item["author"] = (node.xpath("../text()[2]").extract()[0])[:-1]
            if r.get(item['link']) is None:
                r.set(item['link'], item['title'])
                yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.parse_detail)
            else:
                print("已经处理过")

        next_page = base_url + response.xpath("//div[@class='bt2']/a[1]/@href").extract()[0]
        global page_count
        if page_count < 2:
            yield scrapy.Request(next_page, callback=self.parse_web)
            page_count += 1
        else:
            page_count = 0
            print("重新爬取")
            yield scrapy.Request(url="https://yaohuo.me/bbs/book_list.aspx?gettotal=2002&action=new",
                                 callback=self.parse_web)

    def parse_err(self, response):
        self.logger.info('crawl {} failed'.format(response.url))

    def parse_detail(self, response):
        item = response.meta['item']
        item['body'] = \
            response.xpath("//div[@class='bbscontent']/text() | //div[@class='bbscontent']/a/text()").extract()[0]
        item['isRou'] = response.xpath("//div[@class='content']/text()[1]").extract()[0]
        if item["isRou"][0] == "礼":
            var1, var2 = item["isRou"].split()
            total = int(var1[3:])
            surplus = int(var2.split('(')[0][3:])
            once = int(response.xpath("//div[@class='content']/text()[2]").extract()[0].split("：")[1])
            re_url = response.xpath("//form/@action").extract()[0]
            form_data = {
                'face': "",
                'sendmsg': "0",
                'action': 'add',
                'id': str(response.xpath("//form/input[@name='id']/@value").extract()[0]),
                'siteid': str(response.xpath("//form/input[@name='siteid']/@value").extract()[0]),
                'lpage': str(response.xpath("//form/input[@name='lpage']/@value").extract()[0]),
                'classid': str(response.xpath("//form/input[@name='classid']/@value").extract()[0]),
                'sid': str(response.xpath("//form/input[@name='sid']/@value").extract()[0]),
                'g': str(response.xpath("//form/input[@name='g']/@value").extract()[0]),
                'content': ""
            }
            if total - surplus > once:
                msg = "吃肉，已吃:" + str(once) + ",还剩:" + str(surplus - once) + ",谢谢老板"
                form_data['content'] = msg
            elif total - surplus == once:
                msg = "吃肉，下个人没有了," + str(once) + "是最后的了"
                form_data['content'] = msg
            else:
                msg = "吃" + str(surplus)
                form_data['content'] = msg
            yield scrapy.FormRequest(url=base_url + re_url, method='post', formdata=form_data, callback=self.chi)
        # return item

    def chi(self, response):
        print(response.body)
