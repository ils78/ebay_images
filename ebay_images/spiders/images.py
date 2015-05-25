# -*- coding: utf-8 -*-
import scrapy
import re
import rson
from ebay_images.items import EbayImagesItem

class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["ebay.com","ebayimg.com"]
    start_urls = (
        'http://www.ebay.com/sch/Accessory-Bundles-/176971/i.html',
    )

    def __init__(self, url=None, *a, **kw):
        super(ImagesSpider, self).__init__(*a, **kw)
        if url:
            self.start_urls = (url,)

    def parse(self, response):
        if response.url == 'http://www.ebay.com/sch/Accessory-Bundles-/176971/i.html':
            for url in response.xpath('//h3[@class="lvtitle"]//a/@href').extract():
                yield scrapy.Request(url)
        else:
            for script in response.xpath('//script/text()').extract():
                script = re.sub(r'\s+', ' ', script)
                match = re.match(r'^.+"imgArr" : (.+\]), "islarge".+$', script)
                item = EbayImagesItem()
                images = []
                if match:
                    for img in rson.loads(match.group(1)):
                        images.append(img['maxImageUrl'])
                item['image_urls'] = images
                yield item


