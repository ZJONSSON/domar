# -*- coding: utf-8 -*-
import scrapy
from scrapers.items import DomurItem
from domar.models import Domstoll
from scrapy.http.request import Request
import datetime
from scrapy.exceptions import CloseSpider
import lxml.html
from lxml.html.clean import Cleaner
import html2text


class HeradsdomstolarSpider(scrapy.Spider):
    name = 'heradsdomstolar'
    allowed_domains = ['heradsdomstolar.is']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.SaveNewItemPipeline': 300}
                      }

    def __init__(self, offset=0, count=20, margin=30):
        # first run - today is the day
        self.latest_date = datetime.date.today()
        self.base_url = 'https://www.heradsdomstolar.is'
        self.offset = offset
        self.count = count
        self.margin = int(margin)
        self.end = self.latest_date - datetime.timedelta(days=self.margin)
        self.overview_url = 'https://heradsdomstolar.is/default.aspx?pageitemid=e7fc58af-8d46-11e5-80c6-005056bc6a40&offset={}&count={}'
        self.base_url = 'https://www.heradsdomstolar.is'

    def start_requests(self):
        # first request
        yield Request(self.overview_url.format(self.offset, self.count),
                      meta={'offset': self.offset, 'count': self.count},
                      callback=self.parse_overview)


    def parse_overview(self, response):
        offset = int(response.meta['offset'])
        count = int(response.meta['count'])
        root = lxml.html.fromstring(response.text)
        rows = root.xpath('//div[@class="row"]/div[@class="col-sm-6 col-xs-12 verdict-box"]')
        for row in rows:
            item_date = row.xpath('div[@class="sentence"]/a/time')[0].attrib['datetime']
            item_date_object = datetime.datetime.strptime(item_date, '%Y-%m-%dT%H:%M:%S').date()
            if self.end <= item_date_object <= self.latest_date:
                # we have not reached our margin so we shall just continue
                pass
            else:
                # too far, let's get out of here
                raise CloseSpider('Reached date range: {} days'.format(self.margin))
            item = DomurItem()

            url = row.xpath('div[@class="sentence"]/a[@class="sentence"]')[0]
            item['url'] = self.base_url + url.attrib['href']
            item['date'] = item_date_object
            domstoll_tag = row.xpath('div[@class="sentence"]/a/h3')[0]
            domstoll_text = domstoll_tag.text
            domstoll = Domstoll.objects.filter(name=domstoll_text).first()
            item['domstoll'] = domstoll
            identifier_tag = row.xpath('div[@class="sentence"]/a/h2')[0]
            item['identifier'] = identifier_tag.text
            judge_tag = row.xpath('div[@class="sentence"]/a/span[@class="person"]')[0]
            item['judge'] = judge_tag.text
            try:
                abstract_tag = row.xpath('.//div[@class="case-abstract"]')[0]
                item['abstract'] = abstract_tag.text_content()
            except IndexError:
                pass
            yield Request(item['url'], callback=self.parse_judgement,
                          meta={'item': item})
        # are there rows?
        if len(rows) > 0:
            offset = offset + 10
            print(self.base_url.format(offset, count))
            yield Request(self.overview_url.format(offset, count),
                      meta={'offset': offset, 'count': count},
                      callback=self.parse_overview)

    def parse_judgement(self, response):
        item = response.meta['item']
        root = lxml.html.fromstring(response.text)

        tags_tag = root.xpath('//div[@class="verdict-keywords"]/ul/li[@class="keyword"]')
        tags = [tag.text for tag in tags_tag]
        item['tags'] = tags
        cleaner = Cleaner()
        cleaner.kill_tags = ['title']
        text_maker = html2text.HTML2Text()
        text_maker.unicode_snob = True
        text_maker.body_width = 0
        text_maker.ignore_anchors = True
        text_maker.ignore_emphasis = True
        text_tag = root.xpath('//div[@id="main"]/div[@class="subpagewrapper padding20"]/div[@class="no-anchors"]')[0]
        text_tag = cleaner.clean_html(text_tag)
        item['text'] = text_maker.handle(lxml.html.tostring(text_tag).decode("utf-8"))
        yield item

