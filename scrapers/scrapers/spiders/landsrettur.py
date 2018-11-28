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
from scrapers.utils import parse_icelandic_date, split_on_uppercase
import requests


class LandsretturSpider(scrapy.Spider):
    name = 'landsrettur'
    allowed_domains = ['landsrettur.is']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.SaveNewItemPipeline': 300}
                    }

    def _get_keywords(self, url):
        r = requests.get(url)
        root = lxml.html.fromstring(r.text)
        keywords_script = root.xpath("//script[contains(text(),'KeywordsList')]")[0].text
        keywords_script = keywords_script.replace('window.KeywordsList = [', '').replace('];', '').replace('\n','')
        keywords = keywords_script.split(',')
        keywords = set([keyword.replace('"','').strip() for keyword in keywords])


    def __init__(self, offset=0, count=10, margin=30):
        # first run - today is the day
        self.latest_date = datetime.date.today()
        self.domstoll = Domstoll.objects.filter(name='Landsréttur').first()
        self.base_url = 'https://www.landsrettur.is'
        self.offset = offset
        self.count = count
        self.margin = int(margin)
        self.end = self.latest_date - datetime.timedelta(days=self.margin)
        self.overview_url = 'https://landsrettur.is/default.aspx?pageitemid=4468cca6-a82f-11e5-9402-005056bc2afe&offset={}&count={}'
        self.base_url = 'https://www.landsrettur.is'


    def start_requests(self):
        # first request
        yield Request(self.overview_url.format(self.offset, self.count),
                      meta={'offset': self.offset, 'count': self.count},
                      callback=self.parse_overview)


    def parse_overview(self, response):
        offset = int(response.meta['offset'])
        count = int(response.meta['count'])
        root = lxml.html.fromstring(response.text)
        rows = root.xpath('//div[@class="row"]/div[@class="col-md-6 col-xs-12"]')
        for row in rows:
            item_date = row.xpath('div[@class="sentence"]/time')[0].attrib['datetime']
            item_date_object = datetime.datetime.strptime(item_date, '%d.%m.%Y %H:%M:%S').date()
            if self.end <= item_date_object <= self.latest_date:
                # we have not reached our margin so we shall just continue
                pass
            else:
                # too far, let's get out of here
                raise CloseSpider('Reached date range: {} days'.format(self.margin))
            item = DomurItem()
            item['date'] = item_date_object
            item['domstoll'] = self.domstoll
            url = row.xpath('div[@class="sentence"]/a[@class="casenumber"]')[0]
            item['url'] = self.base_url + url.attrib['href']
            identifier_tag = url.xpath('h2')[0]
            item['identifier'] = identifier_tag.text

            try:
                parties_tag = url.xpath('p')[0]
                # remove the \n linebreaks
                item['parties'] = " ".join(parties_tag.text.split())
            except AttributeError:
                # No text for parties
                pass
            try:
                abstract_tag = row.xpath('.//div[@class="case-abstract"]')[0]
                item['abstract'] = abstract_tag.text_content()
            except IndexError:
                pass

            try:
                tags_tag = row.xpath('div[@class="sentence"]/small')[0]
                tags_text = tags_tag.text
                #pos = [i for i, e in enumerate(tags_text + 'A') if e.isupper()]
                #tags = [tags_text[pos[j]:pos[j + 1]].strip().rstrip('.') for j in range(len(pos) - 1)]
                tags = split_on_uppercase(tags_text, True)
                #tags = [tag.strip().rstrip('.') for tag in tags]
                item['tags'] = tags
            except AttributeError:
                # no tags
                pass
            print(item)
        #     yield Request(item['url'], callback=self.parse_judgement,
        #                   meta={'item': item})
        # # are there rows?
        # if len(rows) > 0:
        #     offset = offset + 10
        #     print(self.base_url.format(offset, count))
        #     yield Request(self.overview_url.format(offset, count),
        #               meta={'offset': offset, 'count': count},
        #               callback=self.parse_overview)

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

