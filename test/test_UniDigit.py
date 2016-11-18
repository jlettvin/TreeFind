# -*- coding: utf8 -*-

"""test_UniDigit.py
"""

__module__     = "test_UniDigit.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = [ "Jonathan D. Lettvin" ]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161107"

import unittest2

import sys
sys.path.append('.')
sys.path.append('..')

from UniDigit import ( UniDigit )
from Self   import ( Self   )


class UniDigitTestCase(unittest2.TestCase):

    def setUp(self):
        self.unidigit = UniDigit(ingest=True, unique=False)

    def tearDown(self):
        pass

    def test_comprehensive(self):
        failpass = ['[FAIL] %d u%06x %s', '[PASS] %d u%06x %s']
        total = 0
        okay = 0
        languages = sorted(self.unidigit.languageToDigits.keys())
        for language in languages:
            digits = self.unidigit.languageToDigits[language]
            for digit, char in enumerate(digits):
                total = total + 1
                codepoint = ord(char)
                self.assertEqual(self.unidigit(codepoint), digit)
                result = int(self.unidigit(codepoint) == digit)
                okay = okay + result
        fail = total - okay
