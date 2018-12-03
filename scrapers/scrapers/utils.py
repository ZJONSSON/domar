from dateutil import parser
from reynir import Reynir


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
