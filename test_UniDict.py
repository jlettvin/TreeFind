# -*- coding: utf8 -*-

__module__     = "test_UniDict.py"
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

from UniDict import ( UniDict )

import inspect
class UniDictTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        unidict = UniDict()
        self.assertEqual(unidict, {})

    def test_simple(self):
        sample = {
            " Strip.This*Token": "But: Leave+This$Alone",
            "12BuckleMyShoe34TryItSomeMore": "Does'nt this work?"
        }
        unidict = UniDict(**sample)
        for k,w in unidict.iteritems():
            pass
