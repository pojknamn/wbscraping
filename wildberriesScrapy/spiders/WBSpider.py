import scrapy
from ..items import WildberriesscrapyItem
import time

class WbspiderSpider(scrapy.Spider):
    name = 'WBSpider'
    page_number = 1
    allowed_domains = ['wildberries.ru']
    start_urls = ['https://www.wildberries.ru/catalog/dom/dachniy-sezon/basseyny/naduvnye-basseyny']

    def parse(self, response):
        next_page_url = response.css("a.pagination__next::attr(href)").extract_first()
        hrefs = response.css("a.product-card__main::attr(href)").extract()
        # self.log(len(hrefs))
        for n, link in enumerate(hrefs):
            if n < 1:
                item_link = response.urljoin(link)
                # self.log(item_link)
                yield scrapy.Request(url=item_link, callback=self.parse_detail)


        self.log("card_list:")
        self.log(f"{next_page_url}")
        if next_page_url:
            a = response.urljoin(next_page_url)
            yield scrapy.Request(url=a, callback=self.parse)


    def parse_detail(self, response):
        # self.log(response.url)
        original = 100
        sale = 51
        item = WildberriesscrapyItem()
        item["timestamp"] = time.time()
        item["url"] = response.urljoin(response.css("meta[itemprop='url']::attr(content)")[0].extract())
        item["title"] = response.css('meta[itemprop="name"]::attr(content)').extract_first()
        # item["marketing_tags"] = []
        item["brand"] = response.css('meta[itemprop="brand"]::attr(content)')[0].extract()
        # item["section"] = [i for i in response.css("a.breadcrumbs__link a span[itemprop='title']::text").extract()]
        # item["pricedata"] = {"current": response.css("meta[itemprop='price']::attr(content)").extract(),
        #                      "original": 0.0,
        #                      "sale_tag": f"Скидка: {100 - (original / 100 * sale) }%"}
        # item["stock"] = {"in_stock": True,
        #                  "count": 0}
        # item["assets"] = {"main_image": response.css("meta[itemprop='image']::content").extract(),
        #                   "set_images": response.css(".slide__content img::attr(src)").extract()}
        # item["metadata"] = {"__description": response.css("meta[itemprop='description']::attr(content)").extract(),
        #                     "АРТИКУЛ": response.css("#productNmId::text").extract()
        #                     }
        # for td in response.css("tr.product-params__row"):
        #     col_key = td.css("span.product-params__cell-decor span::text").extract()
        #     col_value = td.css("td.product-params__cell::text").extract()
        #     item['metadata'][col_key] = col_value

        yield item
