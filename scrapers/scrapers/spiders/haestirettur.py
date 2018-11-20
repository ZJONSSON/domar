# -*- coding: utf-8 -*-
import scrapy


class HaestiretturSpider(scrapy.Spider):
    name = 'haestirettur'
    allowed_domains = ['haestirettur.is']
    start_urls = ['http://haestirettur.is/']

    def parse(self, response):
        pass
