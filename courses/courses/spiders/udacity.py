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
            href = link.xpath('./@href').extract_first()
            yield scrapy.Request(
                url='https://br.udacity.com%s' % href,
                callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.xpath('//title/text()').extract_first()
        headline = response.xpath(
            '//h6[contains(@class, "big hidden-sm-down")]/text()'
        ).extract_first()
        instructors = []
        for div in response.xpath(
                '/html/body/ir-root/ir-content/ir-ndop-b/section[7]/ir-nd-instructors//div[contains(@class,"card")]'
        ):
            instructors.append({
                'name':
                div.xpath('./*[contains(@class,"name")]/text()')
                .extract_first(),
                ## aguardando SPA
                #'image':div.xpath('./img/@src').extract_first(),
            })

        yield {
            'title': title,
            'headline': headline,
            'instructors': instructors,
        }