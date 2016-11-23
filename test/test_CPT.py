# -*- coding: utf8 -*-

__module__     = "test_CPT.py"
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
__date__       = "20161123"

import unittest2
import inspect

import sys
sys.path.append('.')
sys.path.append('..')

from CPT        import (CPT      )
from Self       import (Self     )
from datetime   import (datetime, timedelta)


class CPTTestCase(unittest2.TestCase):

    def setUp(self):
        self.cpt = CPT()

    def tearDown(self):
        pass

    def test_empty_length(self):
        "Check length of empty CPT"
        self.assertEqual(len(self.cpt), 0, Self.doc())

    def test_empty_get_fail(self):
        "Check return 0 for getitem on CPT"
        self.assertEqual(self.cpt[97], 0, Self.doc())

    def test_insert(self):
        "Check return pass/fail for good/bad getitem on one-entry CPT"
        codepoint = ord(u'a')
        other = ord(u'b')
        self.cpt[codepoint] = codepoint
        self.assertEqual(self.cpt[codepoint], codepoint, Self.doc())
        self.assertEqual(self.cpt[codepoint], codepoint, Self.doc())
        self.assertEqual(self.cpt[other], 0, Self.doc())

    def test_multiple_insert(self):
        "Check that lowercase exclusive use works"
        codepoints = [ord(c) for c in u"abcdefghijklmnopqrstuvwxyz"]
        others     = [ord(c) for c in u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        cpt        = self.cpt
        for codepoint in codepoints:
            cpt[codepoint] = codepoint
            self.assertEqual(cpt[codepoint], codepoint, Self.doc())
        for other in others:
            self.assertEqual(cpt[other], 0, Self.doc())
        self.assertEqual(len(cpt), 26)

    def test_delete(self):
        "Check that both case use works"
        codepoints = [ord(c) for c in u"abcdefghijklmnopqrstuvwxyz"]
        others     = [ord(c) for c in u"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        both       = codepoints + others
        cpt        = self.cpt
        for codepoint in both:
            cpt[codepoint] = codepoint
        self.assertEqual(len(cpt), 52)
        for codepoint in both:
            self.assertEqual(cpt[codepoint], codepoint, Self.doc())
        for codepoint in others:
            del cpt[codepoint]
        self.assertEqual(len(cpt), 26)
        for other in others:
            self.assertEqual(cpt[other], 0, Self.doc())
        for codepoint in codepoints:
            self.assertEqual(cpt[codepoint], codepoint, Self.doc())

    def test_setitem_timing(self):
        "Calculate the cost of inserts"
        N = 10
        I = 10000
        operations = N * I

        cpt_microseconds = 0.0
        dct_microseconds = 0.0
        d = {}

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                self.cpt[codepoint] = codepoint
            cpt_microseconds += (datetime.now() - t0).total_seconds()

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                d[codepoint] = codepoint
            dct_microseconds += (datetime.now() - t0).total_seconds()

        with open('../artifacts/CPT.setitem.timing.txt', 'w') as target:
            cpt_peroperation = 1e6 * cpt_microseconds / (N * I)
            dct_peroperation = 1e6 * dct_microseconds / (N * I)
            ratio = cpt_peroperation / dct_peroperation
            print>>target, "\tSETITEM"
            print>>target, "%f microseconds/cpt setitem" % (cpt_peroperation)
            print>>target, "%f microseconds/dct setitem" % (dct_peroperation)
            print>>target, "%f performance ratio" % (ratio)
            print>>target, "70 ~times difference.  TODO reimplement in C"

    def test_getitem_timing(self):
        "Calculate the cost of lookups"
        N = 10
        I = 10000
        operations = N * I

        cpt_microseconds = 0.0
        dct_microseconds = 0.0
        d = {}

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                self.cpt[codepoint] = codepoint
            cpt_microseconds += (datetime.now() - t0).total_seconds()

        for codepoint in xrange(I):
            d[codepoint] = codepoint
            self.cpt[codepoint] = codepoint

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                result = self.cpt[codepoint]
            cpt_microseconds += (datetime.now() - t0).total_seconds()

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                result = d[codepoint]
            dct_microseconds += (datetime.now() - t0).total_seconds()

        with open('../artifacts/CPT.getitem.timing.txt', 'w') as target:
            cpt_peroperation = 1e6 * cpt_microseconds / (N * I)
            dct_peroperation = 1e6 * dct_microseconds / (N * I)
            ratio = cpt_peroperation / dct_peroperation
            print>>target, "\tGETITEM"
            print>>target, "%f microseconds/cpt getitem" % (cpt_peroperation)
            print>>target, "%f microseconds/dct getitem" % (dct_peroperation)
            print>>target, "%f performance ratio" % (ratio)
            print>>target, "150 ~times difference.  TODO reimplement in C"

    def test_delitem_timing(self):
        "Calculate the cost of lookups"
        N = 10
        I = 100
        operations = N * I

        cpt_microseconds = 0.0
        dct_microseconds = 0.0
        d = {}

        for _ in xrange(N):
            t0 = datetime.now()
            for codepoint in xrange(I):
                self.cpt[codepoint] = codepoint
            cpt_microseconds += (datetime.now() - t0).total_seconds()

        for codepoint in xrange(I):
            d[codepoint] = codepoint
            self.cpt[codepoint] = codepoint

        for _ in xrange(N):
            for codepoint in xrange(I):
                self.cpt[codepoint] = codepoint
            t0 = datetime.now()
            for codepoint in xrange(I):
                del self.cpt[codepoint]
            cpt_microseconds += (datetime.now() - t0).total_seconds()

        for _ in xrange(N):
            for codepoint in xrange(I):
                d[codepoint] = codepoint
            t0 = datetime.now()
            for codepoint in xrange(I):
                del d[codepoint]
            dct_microseconds += (datetime.now() - t0).total_seconds()

        with open('../artifacts/CPT.delitem.timing.txt', 'w') as target:
            cpt_peroperation = 1e6 * cpt_microseconds / (N * I)
            dct_peroperation = 1e6 * dct_microseconds / (N * I)
            ratio = cpt_peroperation / dct_peroperation
            print>>target, "\tDELITEM"
            print>>target, "%f microseconds/cpt getitem" % (cpt_peroperation)
            print>>target, "%f microseconds/dct getitem" % (dct_peroperation)
            print>>target, "%f performance ratio" % (ratio)
            print>>target, "5000 ~times difference.  TODO reimplement in C"
