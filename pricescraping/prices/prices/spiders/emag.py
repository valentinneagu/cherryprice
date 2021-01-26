import scrapy
import re
import logging


class EmagSpider(scrapy.Spider):
    name = 'emag'
    allowed_domains = ['www.emag.ro']

    def __init__(self, url_to_parse='https://www.emag.ro/', **kwargs):
        self.start_urls = [url_to_parse]
        super().__init__(**kwargs)


    def parse(self, response):
        xpath_discount = "// *[ @ id = \"main-container\"] / section[1] / div / div[2] / div[2] / div / div / div[2] " \
                         "/ form / div[1] / div[1] / div / div[1] / p[2] "
        xpath_full_price = "//*[@id=\"main-container\"]/section[1]/div/div[2]/div[2]/div/div/div[2]/form/div[" \
                           "1]/div/div/div[1]/p "
        paragraph = response.xpath(xpath_discount)
        if not paragraph.get():
            paragraph = response.xpath(xpath_full_price)
        price_fragments = re.findall(r'\d+', paragraph.get())
        final_price = ''.join(price_fragments[:-1]) + ',' + price_fragments[-1]
        logging.info('Price: {}'.format(final_price))
        yield {
            'price': final_price
        }
