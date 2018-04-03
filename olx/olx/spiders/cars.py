# -*- coding: utf-8 -*-
import scrapy


class CarsSpider(scrapy.Spider):
    name = 'cars'
    allowed_domains = ['ce.olx.com.br/veiculos-e-pecas/carros']
    start_urls = ['http://ce.olx.com.br/veiculos-e-pecas/carros/']

    def parse(self, response):
        items = response.xpath('//ul[@id="main-ad-list"]/li')
        for item in items:
            self.log(item.xpath('./a/@href').extract_first())
