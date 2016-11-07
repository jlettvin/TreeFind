# -*- coding: utf8 -*-
import unittest2

from UniDigit import ( UniDigit )

import inspect
class UniDigitTestCase(unittest2.TestCase):

    def setUp(self):
        self.unidigit = UniDigit(ingest=True, unique=False)

    def tearDown(self):
        pass

    def doc(self, msg = ""):
        more = " (%s)" % (msg) if msg else ""
        frame = inspect.currentframe().f_back
        for objref in frame.f_globals.values():
            if inspect.isfunction(objref):
                if objref.func_code == frame.f_code:
                    return objref.__doc__ + more
            elif inspect.isclass(objref):
                for name, member in inspect.getmembers(objref):
                    if inspect.ismethod(member):
                        if member.im_func.func_code == frame.f_code:
                            return member.__doc__ + more

    def test_selfdoc(self):
        """Check for __doc__ string access"""
        d="Check for __doc__ string access"
        self.assertEqual(d, self.doc(), self.doc())

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
