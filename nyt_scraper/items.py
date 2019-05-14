# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HeadlineItem(scrapy.Item):
    # define the fields for your item here like:
    headline = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    pass
