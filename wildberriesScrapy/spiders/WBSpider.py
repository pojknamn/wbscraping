import scrapy
from ..items import WildberriesscrapyItem, PriceItem
import time


class WbspiderSpider(scrapy.Spider):
    name = 'WBSpider'
    page_number = 1
    allowed_domains = ['wildberries.ru']
    start_urls = ['https://www.wildberries.ru/catalog/dom/dachniy-sezon/basseyny/naduvnye-basseyny'] #  ["https://www.wildberries.ru/brands/crocs/all"]

    def parse(self, response):
        item_limit = 100
        next_page_url = response.css("a.pagination__next::attr(href)").extract_first()
        hrefs = response.css("a.product-card__main::attr(href)").extract()
        for link in hrefs:
            time.sleep(1)
            item_link = response.urljoin(link)
            yield scrapy.Request(url=item_link, callback=self.parse_detail)

        if next_page_url:
            a = response.urljoin(next_page_url)
            yield scrapy.Request(url=a, callback=self.parse)
    # TODO: Add proxies and try/except blocks
    def parse_detail(self, response):
        item = WildberriesscrapyItem()
        prices = PriceItem()
        article = response.css("#productNmId::text")[0].extract()
        script_text = response.css("script::text")
        original_price = script_text.re_first(r'"price":[^{][0-9]*')
        current_price = script_text.re_first(r'"salePrice":[0-9]*')
        sale = script_text.re_first(r'"sale":[0-9]*').split(":")[-1]
        color = response.xpath('//*[@id="infoBlockProductCard"]/p[2]/span/text()').extract_first()
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
        item["title"] = f"{item['title']}{f', {color}' if color else ''}"
        item["stock"] = {"in_stock": True if not response.css("span.sold-out-product__text::text").extract() else False,
                         "count": 0}
        list360 = []
        try:
            description = response.css("meta[itemprop='description']::attr(content)")[0].extract()
        except IndexError:
            description = ""
        if response.css(".thumb_3d span::text").extract():
            for pic in range(12):
                base3d_link = f"https://images.wbstatic.net/3d/{article}/{pic}.jpg"
                list360.append(base3d_link)

        item["assets"] = {"main_image": response.css("meta[itemprop='image']::attr(content)")[0].extract(),
                          "set_images": response.css(".slide__content source::attr(srcset)").extract(),
                          "view360": list360,
                          "video": [response.css("meta[property='og:video']::attr(content)").extract_first(),]
                          }

        meta = {"__description": description,
                "АРТИКУЛ": article
                }

        for td in response.css("tr.product-params__row"):
            try:
                col_key = td.css("span.product-params__cell-decor span::text")[0].extract()
            except IndexError:
                col_key = False
            try:
                col_value = td.css("td.product-params__cell::text")[0].extract()
            except IndexError:
                col_value = ""
            if col_key:
                meta[col_key] = col_value
        item["metadata"] = meta
        item["price_data"] = prices
        item["variants"] = len(response.css("li.j-color img::attr(src)").extract())
        yield item
