# -*- coding: utf-8 -*-
import os
import time

import scrapy
from wqxt import Info


def mkdir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, 0o777)


class MainSpider(scrapy.Spider):
    name = 'main'
    allowed_domains = []

    def __init__(self, bid=None, path='', *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        info = Info.BookInfo(bid)
        scrapy.Spider.bid = bid
        scrapy.Spider.book_name = info.book_name
        scrapy.Spider.path = ('' if path == '' else path + '/') + scrapy.Spider.book_name
        scrapy.Spider.pages = info.book_pages
        scrapy.Spider.toc = info.chapter()
        self.path = scrapy.Spider.path
        self.headers = info.headers
        self.imgSrcList = info.imgSrcList()

    def start_requests(self):
        if self.path:
            mkdir(self.path)
        for index, url in enumerate(self.imgSrcList):
            path = self.path + '/%s.jpeg' % index
            if not (os.path.exists(path)):
                yield scrapy.Request(url=url,
                                     callback=self.parse,
                                     dont_filter=True,
                                     headers=self.headers,
                                     meta=dict(path=path))
        # for i in range(20):
        #     yield scrapy.Request(url='http://httpbin.org/get',
        #                                  callback=self.proxy_test,
        #                                  dont_filter=True,
        #                                  headers=self.headers,
        #                                  )

    def proxy_test(self, response):
        print(response.url)
        print(response.text)

    def parse(self, response):
        if len(response.body) == 10400 or len(response.body) == 5:
            print('Error:', len(response.body), '空页重试',response.url)
            print(response.meta)
            yield scrapy.Request(url=response.url,
                                 callback=self.parse,
                                 dont_filter=True,
                                 headers=self.headers,
                                 meta=response.meta)
        else:
            with open(response.meta['path'], 'wb') as file:
                file.write(response.body)
                print(response.meta['path'], "finish in ", time.asctime())
