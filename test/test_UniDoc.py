# -*- coding: utf8 -*-

"""test_Self.py
"""

__module__     = "test_Self.py"
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

from Self   import ( Self   )


class SelfTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_selfdoc(self):
        """Check for __doc__ string access"""
        d="Check for __doc__ string access"
        self.assertEqual(d, Self.doc(), Self.doc())
