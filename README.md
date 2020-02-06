# wenquan_scrapy

文泉学堂爬虫  scrapy框架

支持断点续传

默认8线程工作
线程数量对程序影响不大，详情在settings.py中调整

入口：
## Start.py

    bid = BookId
    path = download path
    example : 'scrapy crawl main -a bid=8784'
    or : 'scrapy crawl main -a bid=8784 -a path=/User/download'

## settings.py
    线程数
    Threads = 8;


    CONCURRENT_REQUESTS_PER_DOMAIN = Threads;
    CONCURRENT_REQUESTS_PER_IP = Threads;
    CONCURRENT_REQUESTS = Threads;
    DOWNLOAD_TIMEOUT = 30;
    主要速度影响为DOWNLOAD_DELAY，服务器会封ip，推荐默认。
    DOWNLOAD_DELAY = 60 / 30;
    RETRY_ENABLED = True;
    RETRY_TIMES = 5;


挂代理直接64线程0延迟跑就可以


破解登陆验证：
(超简单)破解文泉学堂的登陆验证
https://blog.csdn.net/m0_46261074/article/details/104187104

jwt加密详解：
文泉学堂爬虫：Jwt-HS256加解密详解
https://blog.csdn.net/m0_46261074/article/details/104162067

jwt依赖可能会出现解密密钥不正确的问题，配置方法见博客：
解决Python修改pyjwt模块默认header无效的问题
https://blog.csdn.net/m0_46261074/article/details/104165261

项目中的json是已经分类好的id文件,可以直接取用下载全部（推荐挂代理）。

编辑于：Thu Feb 6 23:20:21 2020

左素
