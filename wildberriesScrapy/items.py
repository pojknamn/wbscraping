# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WildberriesscrapyItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field()
    brand = scrapy.Field()
    section = scrapy.Field()
    price_data = scrapy.Field()
    stock = scrapy.Field()
    assets = scrapy.Field()
    metadata = scrapy.Field()
    variants = scrapy.Field()

    # stock
    in_stock = scrapy.Field()
    count = scrapy.Field()

    # assets
    main_image = scrapy.Field()
    set_images = scrapy.Field()
    view360 = scrapy.Field()
    video = scrapy.Field()


class PriceItem(scrapy.Item):
    current = scrapy.Field()
    original = scrapy.Field()
    sale_tag = scrapy.Field()
