# -*- coding: utf-8 -*-
import scrapy
import logging

logger = logging.getLogger(__name__)


class HybkSpider(scrapy.Spider):
    name = "hyBk"
    allowed_domains = ["hengyan.com"]
    start_urls = (
        'http://top.hengyan.com/mianfei/',
    )

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:65.0) Gecko/20100101 Firefox/65.0"
    }

    def parse(self, response):
        ul_list = response.xpath("//div[@id='right']//ul[not(@class='title')]")
        # bookurl_list = response.xpath("//a[@class='bn']/@href")
        for li in ul_list[0:2]:
            book_info = {}
            # logger.warning(li.xpath("./li"))
            book_info["name"] = li.xpath("./li/a[@class='bn']/text()").extract_first()
            book_info["book_url"] = li.xpath("./li/a[@class='bn']/@href").extract_first()
            book_info["author"] = li.xpath("./li[@class='author']/text()").extract_first()
            yield scrapy.Request(
                book_info["book_url"],
                callback=self.book_desc,
                meta={"book": book_info},
            )

        # # get next page and parse
        # page_next = response.xpath("//p[@class='pager']//a")[-2]
        # if page_next.xpath("./text()").extract_first().encode("utf-8") == "下一页":
        #         # page_next = response.xpath("//p[@class='pager']//a[text()='下一页']")
        #         # if page_next is not NONE:
        #     next_url = "http://top.hengyan.com" + page_next.xpath("./@href").extract_first()
        #     print(next_url)
        #     yield scrapy.Request(
        #         next_url,
        #         callback=self.parse
        #     )

    def chapter_list(self, response):
        chapter_li = response.xpath("//div[@class='chapter']//li")
        book_info = response.meta["book"]
        book_info["chapter_info"] = {}
        for chapter in chapter_li:
            chapter_name = chapter.xpath("./a/text()").extract_first()
            book_info["chapter_info"][chapter_name] = chapter.xpath("./a/@href").extract_first()
            # print("chapter: %s, url: %s" % (book_info["chapter_info"]
            #                                 ["chapter_name"], book_info["chapter_info"]["chapter_url"]))
        print("***" * 20 + "chapter OK")
        yield book_info

    def book_desc(self, response):
        book_info = response.meta["book"]
        book_info["type"] = response.xpath("//p[@class='info']/span/a/text()").extract_first()
        yield scrapy.Request(
            book_info["book_url"].replace("book", "dir"),
            callback=self.chapter_list,
            meta={"book": book_info},
        )
