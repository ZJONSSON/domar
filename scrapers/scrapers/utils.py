from dateutil import parser
from reynir import Reynir
import os
from pathlib import Path
import lxml.html
import html2text
import lxml.html.clean


SCRAPERS_ROOT = os.environ['SCRAPERS_ROOT']

PDF_ROOT = Path(SCRAPERS_ROOT).parent / "pdf"

r = Reynir()


class IcelandicDateParserInfo(parser.parserinfo):
    def __init__(self):
        self.WEEKDAYS = [(u"Mán", u"Mánudagur"),
                         (u"Þri", u"Þriðjudagur"),
                         (u"Mið", u"Miðvikudagur"),
                         (u"Fim", u"Fimmtudagur"),
                         (u"Fös", u"Föstudagur"),
                         (u"Lau", u"Laugardagur"),
                         (u"Sun", u"Sunnudagur")]
        self.MONTHS = [(u"Jan", u"janúar"),
                       (u"Feb", u"febrúar"),
                       (u"Mar", u"mars"),
                       (u"Apr", u"apríl"),
                       (u"May", u"maí"),
                       (u"jún", u"júní"),
                       (u"júl", u"júlí"),
                       (u"ágú", u"ágúst"),
                       (u"sep", u"september"),
                       (u"okt", u"október"),
                       # (u"nov", u"nóvember"),
                       (u"nóv", u"nóvember"),
                       (u"des", u"desember")]
        parser.parserinfo.__init__(self)

    def __call__(self):
        """ dateutil calls the parserinfo to instantiate it"""
        return self


def parse_icelandic_date(text):
    return parser.parse(text, parserinfo=IcelandicDateParserInfo())


def parse_sentences(text):
    #r = Reynir()
    parsed = r.parse(text)
    sentences = [sentence.tidy_text for sentence in parsed['sentences']]
    return(sentences)


def save_judgement_pdf_file(response, court):
    filename_id = os.path.basename(response.url)
    year = filename_id[:4]
    folder = PDF_ROOT / court / year
    folder.mkdir(parents=True, exist_ok=True)
    filename = folder / filename_id
    filename.write_bytes(response.body)


def remove_element(el):
    # see: https://stackoverflow.com/a/53572856
    parent = el.getparent()
    if el.tail is not None:
        if el.tail.strip():
            prev = el.getprevious()
            if prev:
                prev.tail = (prev.tail or '') + el.tail
            else:
                parent.text = (parent.text or '') + el.tail
    parent.remove(el)


def clean_domur_response(response_text):
    text = response_text.replace('<o:p>', '')
    text = text.replace('</o:p>', '')
    text = text.replace('&nbsp;', ' ')
    text = text.replace('<hr>', '<hr />')
    text = text.replace('<br>', '<br />')
    # Hello non-breaking space
    text = text.replace('\xa0', ' ')
    root = lxml.html.fromstring(text)
    cleaner = lxml.html.clean.Cleaner(style=True)
    root = cleaner.clean_html(root)
    # remove empty tags
    for el in root.xpath("//*[not(normalize-space())]"):
        remove_element(el)
    # if we have tables, then remove paragraph tags from them
    # (but keep their content)
    for table in root.xpath('//table'):
        ps = table.findall('.//p')
        for p in ps:
            p.drop_tag()
    return root


def get_markdown(text_tag):
    text_maker = html2text.HTML2Text()
    text_maker.unicode_snob = True
    text_maker.body_width = 0
    text_maker.ignore_anchors = True
    text = text_maker.handle(lxml.html.tostring(text_tag, method='html', encoding='unicode'))
    # it so happens that the emphasis has a trailing (or leading) space
    # See line 155: https://www.haestirettur.is/default.aspx?\
    # pageid=347c3bb1-8926-11e5-80c6-005056bc6a40&id=c406c42d-8170-41db-9f05-bd4f8c75fc5e
    text = text.replace(' _', '_')
    text = text.replace('_ ', '_')
    return text
