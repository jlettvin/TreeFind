# -*- coding: utf8 -*-

__module__     = "test_UniArray.py"
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

from Self   import ( Self   )
from UniArray import ( UniArray )


class UniArrayTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1x1(self):
        """
        Construct a zero-initialized one member array.
        Check for expected initialization.
        """
        data = [[0]]
        expect = {'shape': (1, 1), 'data': data, 'size': 1}
        uniarray = UniArray((1,1), 0)
        self.assertEquals(uniarray, expect, Self.doc())

    def test_1x2(self):
        """
        Construct a -1 initialized two member array.
        Check for expected initialization.
        """
        data = [[-1, -1]]
        expect = {'shape': (1, 2), 'data': data, 'size': 2}
        uniarray = UniArray((1,2), -1)
        self.assertEquals(uniarray, expect, Self.doc())

    def test_2x2x2(self):
        """
        Construct a 9 initialized eight member array.
        Check for expected initialization.
        """
        data = [[[8, 8], [8, 8]], [[8, 8], [8, 8]]]
        expect = {'shape': (2, 2, 2), 'data': data, 'size': 8}
        uniarray = UniArray((2, 2, 2), 8)
        self.assertEquals(uniarray, expect, Self.doc())

    def test_2x2x2_modify_element(self):
        """
        Construct a 9 initialized eight member array.
        Modify last element by index.
        """
        data = [[[8, 8], [8, 8]], [[8, 8], [8, 9]]]
        expect = {'shape': (2, 2, 2), 'data': data, 'size': 8}
        uniarray = UniArray((2, 2, 2), 8)
        uniarray[1,1,1] = 9
        self.assertEquals(uniarray, expect, Self.doc())

    def test_2x2x2_modify_pair(self):
        """
        Construct an 8 initialized eight member array.
        Modify a pair.
        """
        data = [[[8, 8], [8, 8]], [[8, 8], [7, 9]]]
        expect = {'shape': (2, 2, 2), 'data': data, 'size': 8}
        uniarray = UniArray((2, 2, 2), 8)
        uniarray[1,1] = [7, 9]
        self.assertEquals(uniarray, expect, Self.doc())

    def test_2x2x2_modify_block(self):
        """
        Construct a 0 initialized eight member array.
        Modify a top-level block.
        """
        data = [[[0, 0], [0, 0]], [[5, 6], [7, 8]]]
        expect = {'shape': (2, 2, 2), 'data': data, 'size': 8}
        uniarray = UniArray((2, 2, 2), 0)
        #uniarray[1] = [[5, 6], [7, 8]]
        #self.assertEquals(uniarray, expect, Self.doc())

    def test_2x3_convert_4x1(self):
        """
        Construct a 2-initialized 4 member array.
        Check for expected initialization.
        """
        before = [[2, 2, 2], [2, 2, 2]]
        after  = [[5], [5], [5], [5]]
        expect = {'shape': (4, 1), 'data': after, 'size': 4}
        uniarray = UniArray((2,3), 2)
        uniarray(**expect)
        self.assertEquals(uniarray, expect, Self.doc())

