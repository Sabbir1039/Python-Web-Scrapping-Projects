import scrapy

class QuotesItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    author_details_link = scrapy.Field()
    tags = scrapy.Field()
    author_details = scrapy.Field()