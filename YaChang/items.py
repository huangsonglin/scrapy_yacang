# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YachangItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    auction_time = scrapy.Field()
    auction_city = scrapy.Field()
    lot_num = scrapy.Field()
    aution_company = scrapy.Field()
    auction_classfy = scrapy.Field()
    auction_status = scrapy.Field()
    preview_auction_time = scrapy.Field()
    preview_auction_loction = scrapy.Field()
    official_auction_time = scrapy.Field()
    official_auction_loction = scrapy.Field()
    lotImformation = scrapy.Field()








