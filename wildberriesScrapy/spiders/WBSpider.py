import json

import scrapy
from ..items import WildberriesscrapyItem, PriceItem
import time
import re

class WbspiderSpider(scrapy.Spider):
    name = 'WBSpider'
    page_number = 1
    allowed_domains = ['wildberries.ru']
    start_urls = ["https://www.wildberries.ru/promotions/crocs-i-den-shopinga"]  # ['https://www.wildberries.ru/catalog/dom/dachniy-sezon/basseyny/naduvnye-basseyny']

    def parse(self, response):
        item_limit = 7
        next_page_url = response.css("a.pagination__next::attr(href)").extract_first()
        hrefs = response.css("a.product-card__main::attr(href)").extract()
        for n, link in enumerate(hrefs):
            if n < item_limit:  # Временный лимит количества предметов на страницу
                item_link = response.urljoin(link)
                yield scrapy.Request(url=item_link, callback=self.parse_detail)

        if next_page_url:
            a = response.urljoin(next_page_url)
            yield scrapy.Request(url=a, callback=self.parse)

    def parse_detail(self, response):
        item = WildberriesscrapyItem()
        prices = PriceItem()
        script_text = response.css("script::text")
        original_price = script_text.re_first(r'"price":[^{][0-9]*')
        current_price = script_text.re_first(r'"salePrice":[0-9]*')
        sale = script_text.re_first(r'"sale":[0-9]*').split(":")[-1]
        item["timestamp"] = time.time()
        item["RPC"] = script_text.re_first(r'"imtId":[0-9]*').split(":")[-1]
        item["url"] = response.urljoin(response.css("meta[itemprop='url']::attr(content)")[0].extract())
        item["title"] = response.css('meta[itemprop="name"]::attr(content)').extract_first()
        item["marketing_tags"] = [i for i in response.css("a.spec-action__link::text").extract()]
        item["brand"] = response.css('meta[itemprop="brand"]::attr(content)')[0].extract()
        item["section"] = list(set([i for i in response.css("span[itemprop='title']::text").extract()]))
        prices["current"] = float(current_price.split(":")[-1])
        prices["original"] = float(original_price.split(":")[-1])
        prices["sale_tag"] = "" if not sale else f"Скидка {sale}%"
        color = response.xpath('//*[@id="infoBlockProductCard"]/p[2]/span/text()').extract_first()
        item["title"] = f"{item['title']}{f', {color}' if color else ''}"

        item["stock"] = {"in_stock": True if not response.css("span.sold-out-product__text::text").extract() else False,
                         "count": 0}
        item["assets"] = {"main_image": response.css("meta[itemprop='image']::attr(content)")[0].extract(),
                          "set_images": response.css(".slide__content source::attr(srcset)").extract(),
                          }
        meta = {"__description": response.css("meta[itemprop='description']::attr(content)")[0].extract(),
                "АРТИКУЛ": response.css("#productNmId::text")[0].extract()
                }
        for td in response.css("tr.product-params__row"):
            col_key = td.css("span.product-params__cell-decor span::text")[0].extract()
            col_value = td.css("td.product-params__cell::text")[0].extract()
            self.log(f"key - {col_key} :: val - {col_value}")
            meta[col_key] = col_value
        item["metadata"] = meta
        item["price_data"] = prices
        yield item
