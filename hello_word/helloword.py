import scrapy


class GilenoFilhoSpider(scrapy.Spider):
    name = "GilenoFilho"
    start_urls = ["http://www.gilenofilho.com.br"]

    def parse(self, response):
        self.log("Hello Word")
        self.log(response.body)