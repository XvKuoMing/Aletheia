import scrapy
from collector.items import CollectedProduct
import re


class CrosserSpider(scrapy.Spider):
    name = "crosser"
    original_name = 'Перекресток'
    allowed_domains = ["www.perekrestok.ru"]
    name_volume = re.compile(r"""
                            (.*)          # название товара
                            ,             # разграничитель между названием и его размером/объемом
                            \s*           # возможно пропущенные пробелы
                            (\d+)\s*(\w+)   # размер и единица измерения товара
                            \s*           # возможные лишние пробелы в конце
                            $             # на этом все заканчивается
                            """,
                        re.VERBOSE)
    products = []

    def start_requests(self):
        yield scrapy.Request("https://www.perekrestok.ru/cat", self.parse)
        for product in self.products:
            yield scrapy.Request(f"https://www.perekrestok.ru/cat/search?search={product}", self.parse)
        self.products = []

    def parse(self, response):

        if response.css('.product__title'):  # если это карточка продукта то собираем ее
            collected = CollectedProduct()
            collected['shop'] = self.original_name
            name = response.css('.product__title::text').extract()[0]
            name_volume = self.name_volume.search(name)
            if name_volume:
                name = name_volume.group(1)
                volume = float(name_volume.group(2))
                volume_unit = name_volume.group(3)
            else:
                name = name
                volume = None
                volume_unit = None
            collected['name'] = name
            collected['volume'] = volume
            collected['volume_unit'] = volume_unit

            price_per_unit = response.css('.product-price-wrapper .price-card-unit-value::text').extract()
            price, unit = int(price_per_unit[0].split(',')[0]), price_per_unit[-1]
            collected['price'] = price  # оставляем только целое число
            collected['price_unit'] = unit
            desc = response.css('h2.product-composition-title + p::text').extract()
            collected['description'] = desc[0] if desc else None
            collected['img'] = response.css('div.product__gallery img::attr(src)').extract()[0]  # храним только ссылку
            yield collected

        products = response.css('.product-card__link')  # собираем все ссылки
        for product in products:
            # вытаскиваем ссылку каждого продукта и парсим его
            product_page_url = 'https://' + self.allowed_domains[0] + product.css('a').attrib['href']
            yield response.follow(product_page_url,
                                  callback=self.parse)

