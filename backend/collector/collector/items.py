# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CollectedProduct(scrapy.Item):
    # product item
    shop = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    volume = scrapy.Field()
    volume_unit = scrapy.Field()
    price_unit = scrapy.Field()
    description = scrapy.Field()
    img = scrapy.Field()
