# -*- coding: utf-8 -*-
import scrapy
from courses.items import CourseItem, VeducaItemLoader
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class VeducaSpider(scrapy.Spider):
    name = 'veduca'
    allowed_domains = ['veduca.org']
    start_urls = ['http://veduca.org/courses']

    def parse(self, response):
        couser_list = response.xpath(
            "//div[contains(@class,'course-listing')]//a")
        for course_item in couser_list:
            url = course_item.xpath(".//@href").extract_first()
            url = 'https://veduca.org%s' % url
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            "//span[contains(@class, 'next')]/a/@href").extract_first()
        if next_page:
            self.log("============= PAGE: %s ===============" % next_page)
            yield scrapy.Request(
                url='https://veduca.org%s' % next_page, callback=self.parse)

    def parse_detail(self, response):
        loader = VeducaItemLoader(CourseItem(), response=response)
        loader.add_value("url", response.url)
        loader.add_xpath("title",
                         "//*[contains(@class,'course-title')]/text()")
        loader.add_xpath("headline",
                         "//*[contains(@class,'course-subtitle')]/text()")
        loader.add_xpath("instructors",
                         "//*[contains(@class,'author-name')]/text()")
        loader.add_xpath("lectures", "//a[contains(@class,'item')]/@href")
        loader.add_xpath(
            "instructors_description",
            "//div[contains(@class,'bio')]/div/div/div/div/div[2]")
        yield loader.load_item()
