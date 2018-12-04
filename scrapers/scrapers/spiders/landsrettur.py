# -*- coding: utf-8 -*-
import scrapy
from scrapers.items import DomurItem
from domar.models import Domstoll, Domur
from scrapy.http.request import Request
import datetime
from scrapy.exceptions import CloseSpider
import lxml.html
from scrapers.utils import parse_sentences, save_judgement_pdf_file
import requests
import io
from wand.image import Image
from google.cloud import vision
from google.cloud.vision import types


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
        keywords_script = keywords_script.replace('window.KeywordsList = [', '').replace('];', '').replace('\n', '')
        keywords = keywords_script.split(',')
        keywords = set([keyword.replace('"', '').strip() for keyword in keywords])

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

        self.client = vision.ImageAnnotatorClient()

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
            url = row.xpath('div[@class="sentence"]/a[@class="casenumber"]')[0]
            item = DomurItem()
            item['url'] = self.base_url + url.attrib['href']
            identifier_tag = url.xpath('h2')[0]
            item['identifier'] = identifier_tag.text
            if Domur.objects.filter(identifier=item['identifier']).exists():
                # Already seen this and saved. Nothing more to do.to
                self.logger.info('Already seen: {}'.format(item['identifier']))
                continue

            item_date = row.xpath('div[@class="sentence"]/time')[0].attrib['datetime']
            item_date_object = datetime.datetime.strptime(item_date, '%d.%m.%Y %H:%M:%S').date()
            if self.end <= item_date_object <= self.latest_date:
                # we have not reached our margin so we shall just continue
                pass
            else:
                # too far, let's get out of here
                raise CloseSpider('Reached date range: {} days'.format(self.margin))
            item['date'] = item_date_object
            item['domstoll'] = self.domstoll
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
                tags = parse_sentences(tags_text)
                # remove the end sentence punctuation
                tags = [tag.strip().rstrip('.') for tag in tags]
                item['tags'] = tags
            except AttributeError:
                # no tags
                pass
            yield Request(item['url'], callback=self.find_pdf_link,
                           meta={'item': item})
        # do we have a continue button? If so, let's scrape further
        more_button = root.find_class('moreVer')
        if more_button:
            offset = offset + count
            yield Request(self.overview_url.format(offset, count),
                      meta={'offset': offset, 'count': count},
                      callback=self.parse_overview)

    def find_pdf_link(self, response):
        item = response.meta['item']
        root = lxml.html.fromstring(response.text)
        pdf_link = root.xpath('//a[contains(@class, "pdflink")]')[0]
        pdf_url = self.base_url + pdf_link.attrib['href']
        yield Request(pdf_url, callback=self.parse_pdf,
                           meta={'item': item})

    def parse_pdf(self, response):
        item = response.meta['item']
        save_judgement_pdf_file(response, str(self.domstoll))
        f = io.BytesIO(response.body)
        with Image(blob=f, resolution=150) as all_pages:
            f.close()
            text = ""
            for img in all_pages.sequence:
                with Image(image=img) as img_page:
                    img_page.format = 'png'
                    output = io.BytesIO()
                    img_page.save(file=output)
                    image = types.Image(content=output.getvalue())
                    output.close()
                    response = self.client.document_text_detection(image=image)
                    text = text + response.text_annotations[0].description
        item['text'] = text
        yield item
