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
import inspect

import sys
sys.path.append('.')
sys.path.append('..')

from UniDict  import ( UniDict  )
from Self   import ( Self   )

class UniDictTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_empty(self):
        unidict = UniDict()
        self.assertEqual(unidict, {})

    def test_simple(self):
        """
        Check for proper conversions of member names and data fields.
        """
        before = {
            " Strip.This*Token": "But: Leave+This$Alone",
            "12BuckleMyShoe34TryItSomeMore": "Does'nt this work?"
        }
        after = {
            "StripThisToken": "But: Leave+This$Alone",
            "BuckleMyShoeTryItSomeMore": "Does\\'nt this work?"
        }
        unidict = UniDict(**before)
        self.assertEqual(unidict, after, Self.doc())
