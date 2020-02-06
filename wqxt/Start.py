from scrapy import cmdline

# bid = BookId
# path = download path
# example : 'scrapy crawl main -a bid=8784
# or : 'scrapy crawl main -a bid=8784 -a path=/User/download

cmdline.execute('scrapy crawl main -a bid=8784'.split())
# cmdline.execute('scrapy crawl main -a bid=8784 -a path=/User/download'.split())
