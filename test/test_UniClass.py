# -*- coding: utf8 -*-

"""test_UniClass.py
"""

__module__     = "test_UniClass.py"
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
__date__       = "20161110"

import unittest2

import sys
sys.path.append('.')
sys.path.append('..')

from Self   import ( Self   )
from UniClass import ( UniClass )


class SelfTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_selfUniClass(self):
        """Check for good conversions"""

        testData = u"""\
A	000041	Lu
B	000042	Lu
C	000043	Lu
a	000061	Ll
b	000062	Ll
c	000063	Ll
0	000030	Nd
1	000031	Nd
2	000032	Nd
$	000024	Sc
=	00003d	Sm
*	00002a	Po
愚	00611a	Lo
公	00516c	Lo
移	0079fb	Lo
山	005c71	Lo
"""

        for line in testData.split('\n'):
            line = line.strip()
            if not line:
                break
            A, B, C = line.split()
            if A and B and C:
                codepoint = ord(A)
                self.assertEqual(codepoint, int(B, 0x10), Self.doc())
                self.assertEqual(UniClass.classify(codepoint), C, Self.doc())
