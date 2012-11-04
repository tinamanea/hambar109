# encoding: utf-8
import unittest
from datetime import date
from path import path
from mof_parser import parse


DATA = path(__file__).abspath().parent / 'data'


class MofParserTest(unittest.TestCase):

    def setUp(self):
        self.html = (DATA / 'mof1_2009_0174.html').text('windows-1252')

    def test_phrase_found_in_text(self):
        self.assertIn("utilizeze eficient spectrul radio", self.html)

    def test_parser_returns_section_meta(self):
        out = parse(self.html)
        self.assertDictContainsSubset({
            'heading': "PARTEA I",
            'title': u"LEGI, DECRETE, HOTĂRÂRI SI ALTE ACTE",
            'date': date(2009, 3, 19),
            'mof_number': 174,
        }, out['meta'])

    def test_parser_extracts_main_sections(self):
        out = parse(self.html)
        self.assertEqual(len(out['sections']), 4)
        self.assertEqual([s['title'] for s in out['sections']], [
            u"DECIZII ALE CURTII CONSTITUTIONALE",
            u"ORDONANTE SI HOTĂRÂRI ALE GUVERNULUI ROMÂNIEI",
            (u"ACTE ALE ORGANELOR DE SPECIALITATE ALE "
                 u"ADMINISTRATIEI PUBLICE CENTRALE"),
            u"ACTE ALE BĂNCII NATIONALE A ROMÂNIEI",
        ])

    def test_parser_extracts_articles(self):
        out = parse(self.html)
        section_gov = out['sections'][1]
        self.assertEqual([a['title'][:62] for a in section_gov['articles']], [
            u"22. - Ordonantă de urgentă privind înfiintarea Autoritătii Nat",
            u"290. - Hotărâre privind încetarea exercitării functiei publice",
            u"291. - Hotărâre privind exercitarea, cu caracter temporar, a f",
            u"294. - Hotărâre privind modificarea raportului de serviciu al ",
            u"295. - Hotărâre privind exercitarea, cu caracter temporar, a f",
            u"296. - Hotărâre privind încetarea exercitării de către domnul ",
            u"297. - Hotărâre privind dispunerea reluării activitătii de căt",
            u"304. - Hotărâre privind exercitarea, cu caracter temporar, a f",
        ])
