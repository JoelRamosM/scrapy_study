# -*- coding: utf-8 -*-
import scrapy


class UdacitySpider(scrapy.Spider):
    name = 'udacity'
    start_urls = ['https://br.udacity.com/courses/all/']

    def parse(self, response):
        divs = response.xpath(
            '/html/body/ir-root/ir-content/ir-course-catalog/section/div/div/div/div/div'
        )
        for div in divs:
            link = div.xpath('.//h3/a')
            title = link.xpath('./text()').extract_first()
            href = link.xpath('./@href').extract_first()
            img = div.xpath('.//img[contains(@class, "course-thumb")]/@src'
                            ).extract_first()
            descriprion = div.xpath('.//div[2]/span/text()').extract_first()
            yield {
                'title': title,
                'url': href,
                'img': img,
                'description': descriprion,
            }