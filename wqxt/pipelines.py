# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

import fitz
import img2pdf



class WqxtPipeline(object):
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        print('爬虫开始了...')

    def close_spider(self, spider):
        self.img_to_pdf(spider)

        print('爬虫结束了...')

    def img_to_pdf(self, spider):
        path = spider.path
        if path:
            book_name = spider.book_name
            pdf_path_ = "{}/{}_.pdf".format(path, book_name)
            pdf_path = "{}/{}.pdf".format(path, book_name)
            print(pdf_path_)
            with open(pdf_path_, "wb") as f:
                img_list = []
                for img_name in range(0, spider.pages):
                    img_name = "%s/%s.jpeg" % (path, img_name)
                    img_list.append(img_name)
                    print(img_name)
                pfn_bytes = img2pdf.convert(img_list)
                f.write(pfn_bytes)
            print("转换完成")

            doc = fitz.open(pdf_path_)
            toc = spider.toc
            doc.setToC(toc)
            doc.save(pdf_path)
            doc.close()
            print('添加目录完成')
            print(pdf_path_, pdf_path)

            if (os.path.exists(pdf_path_)):
                os.remove(pdf_path_)
            for img_name in range(0, spider.pages):
                img_name = "%s/%s.jpeg" % (path, img_name)
                if (os.path.exists(img_name)):
                    os.remove(img_name)
            print('已删除')
