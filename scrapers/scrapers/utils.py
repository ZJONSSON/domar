from dateutil import parser


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


def split_on_uppercase(s, keep_contiguous=False):
    """
    See: https://stackoverflow.com/questions/2277352/split-a-string-at-uppercase-letters

    Args:
        s (str): string
        keep_contiguous (bool): flag to indicate we want to
                                keep contiguous uppercase chars together

    Returns:

    """
    string_length = len(s)
    is_lower_around = (lambda: s[i-1].islower() or
                       string_length > (i + 1) and s[i + 1].islower())

    start = 0
    parts = []
    for i in range(1, string_length):
        if s[i].isupper() and (not keep_contiguous or is_lower_around()):
            parts.append(s[start: i])
            start = i
    parts.append(s[start:])

    return parts
