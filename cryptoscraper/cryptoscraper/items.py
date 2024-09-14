# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptoscraperItems(scrapy.Item):
    crypto_name = scrapy.Field()
    flagging_reason = scrapy.Field()
    crypto_address = scrapy.Field()
