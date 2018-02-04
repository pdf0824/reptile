# 腾讯招聘信息爬取:
1、爬虫从main函数开始，直接运行[main.py](https://github.com/pdf0824/reptile/blob/master/scrapyDemo/Tencent/Tencent/main.py)即可\
2、[items.py](https://github.com/pdf0824/reptile/blob/master/scrapyDemo/Tencent/Tencent/items.py)定义了爬取的属性\
3、[settings.py](https://github.com/pdf0824/reptile/blob/master/scrapyDemo/Tencent/Tencent/settings.py)增加了对于 - o 输出时正确显示中文\
4、[pipelines.py](https://github.com/pdf0824/reptile/blob/master/scrapyDemo/Tencent/Tencent/pipelines.py)定义输出以及转码，结果存于data.json中\
5、[tencent.py](https://github.com/pdf0824/reptile/blob/master/scrapyDemo/Tencent/Tencent/spiders/tencent.py)是具体的爬虫\

## 爬了什么？
- 对腾讯社招所有的招聘信息进行爬取
- 内容有：职位名称、详情链接、职位类别、招聘人数、工作地点、发布时间、工作职责、工作要求
- 哈哈  ，没了

### 腾讯招聘爬虫  完结