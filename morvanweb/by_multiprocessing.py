# coding = utf-8

import multiprocessing as mp
from urllib.request import urlopen, urljoin
from bs4 import BeautifulSoup
import re
import time

base_url = 'https://morvanzhou.github.io/'


def crawl(url):
    return urlopen(url).read().decode('utf-8')


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {'href': re.compile('^/.+?/$')})
    title = soup.find('h1').get_text().strip()
    page_urls = set([urljoin(base_url, url['href']) for url in urls])
    url = soup.find('meta', {'property': "og:url"})['content']
    return title, page_urls, url




if __name__ == '__main__':
    unseen = set([base_url, ])
    seen = set()
    count, t1 = 1, time.time()
    pool = mp.Pool(4)
    while len(unseen) != 0:
        print('\nDistributed Crawling...')
        crawl_jobs = [pool.apply_async(crawl, args=(url, )) for url in unseen]
        htmls = [i.get() for i in crawl_jobs]

        print('\nDistributed Parsing...')
        parse_jobs = [pool.apply_async(parse, args=(html, )) for html in htmls]
        results = [j.get() for j in parse_jobs]

        print('\nAnalysing...')
        seen.update(unseen)
        unseen.clear()

        for title, page_urls, url in results:
            print(count, title, url)
            count += 1
            unseen.update(page_urls - seen)
    print('Total time: %.1f s' % (time.time() - t1,))
