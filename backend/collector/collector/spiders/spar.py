import scrapy


class SparSpider(scrapy.Spider):
    name = "spar"
    original_name = 'SPAR'
    allowed_domains = ["myspar.ru"]
    start_urls = ["https://myspar.ru/"]

    def parse(self, response):
        pass
