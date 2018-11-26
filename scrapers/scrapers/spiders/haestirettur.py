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


class HaestiretturSpider(scrapy.Spider):
    name = 'haestirettur'
    allowed_domains = ['haestirettur.is']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapers.pipelines.HaestiretturPipeline': 300}
                      }

    def __init__(self, offset=0, count=10, margin=30):
        # first run - today is the day
        self.latest_date = datetime.date.today()
        # we only deal with the supreme court here
        self.domstoll = Domstoll.objects.filter(name='Hæstiréttur').first()
        self.base_url = 'https://www.haestirettur.is'
        self.offset = offset
        # the highest number of judgements on one page that we can get - we can
        # get fewer, but not more - kept here if it would so happen that the
        # court would change their default value which is 10
        # you can set this on the command line with -a NAME=VALUE
        self.count = count
        # How far do we want to go? 30 days from today is the default. To do
        # a full run, set it 7000 or so.
        self.margin = int(margin)
        # go back margin days
        self.end = self.latest_date - datetime.timedelta(days=self.margin)
        self.overview_url = 'https://www.haestirettur.is/default.aspx?pageitemid=4468cca6-a82f-11e5-9402-005056bc2afe&offset={}&count={}'
        self.base_url = 'https://www.haestirettur.is'

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
                tags_tag = row.xpath('div[@class="sentence"]/small')[0]
                tags = [tag.strip() for tag in tags_tag.text.split('.')]
                item['tags'] = tags
            except AttributeError:
                # no tags
                pass

            # it happens that no abstract is provided (in the olden days, kids)
            try:
                abstract_tag = row.xpath('.//div[@class="case-abstract"]')[0]
                item['abstract'] = abstract_tag.text_content()
            except IndexError:
                pass
            # parse the text from the individual verdict page
            yield Request(item['url'], callback=self.parse_judgement,
                          meta={'item': item})
        # do we have a continue button? If so, let's scrape further
        more_button = root.find_class('moreVer')
        if more_button:
            offset = offset + 10
            print(self.base_url.format(offset, count))
            yield Request(self.overview_url.format(offset, count),
                      meta={'offset': offset, 'count': count},
                      callback=self.parse_overview)

    def parse_judgement(self, response):
        item = response.meta['item']
        root = lxml.html.fromstring(response.text)
        # old judgements do not have the apellants or plaintiffs tags
        try:
            appellants_tag = root.xpath('//div[@class="appelants"]')[0]
            plaintiffs_tag = root.xpath('//div[@class="plaintiffs"]')[0]
            item['appellants'] = appellants_tag.text_content()
            item['plaintiffs'] = plaintiffs_tag.text_content()
        except IndexError:
            pass

        # lets get the text

        # cleaner options for the main text
        cleaner = Cleaner()
        # old verdicts have a lot of Microsoft Word elements - one of them is title
        cleaner.kill_tags = ['title']

        # set up the html2text options
        text_maker = html2text.HTML2Text()
        text_maker.unicode_snob = True
        text_maker.body_width = 0
        text_maker.ignore_anchors = True
        text_maker.ignore_emphasis = True

        # get the verdict
        text_tag = root.xpath('//div[@class="verdict"]')[0]
        # clean it
        text_tag = cleaner.clean_html(text_tag)

        # remove the pdf links
        for r in text_tag.xpath('.//a[@class="pdflink pull-right"]'):
            r.getparent().remove(r)

        item['text'] = text_maker.handle(lxml.html.tostring(text_tag).decode("utf-8"))
        yield item

