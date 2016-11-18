#!/usr/bin/env python
# -*- coding: utf8 -*-

"""test_Self.py
This module tests test_Codepoint grammar which imports "classify16" grammar.
"""

__module__     = "test_Codepoint.py"
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
__date__       = "20161111"

import unittest2

from Self   import ( Self   )

from antlr4                             import *
from test_CodepointLexer                import (    test_CodepointLexer     )
from test_CodepointListener             import (    test_CodepointListener  )
from test_CodepointParser               import (    test_CodepointParser    )

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

class test_CodepointPrintListener(test_CodepointListener):

    def enterHello(self, ctx):
        #if not self.result:
        self.result = "[PASS] classify: %s" % (ctx.ID())

    def enterCodepoint(self, ctx):
        #if not self.result:
        self.result = "[FAIL] classify: %s" % (ctx.ID())

    def __str__(self):
        return unicode(self.result)

class SelfTestCase(unittest2.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_English(self):
        """
        Does "hello unittest" get identified?
        """
        lexer = test_CodepointLexer(InputStream("hello unittest"))
        stream = CommonTokenStream(lexer)
        parser = test_CodepointParser(stream)
        tree = parser.prog()
        printer = test_CodepointPrintListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        self.assertEquals(u"[PASS] classify: unittest",
                str(printer),
                Self.doc())

    def test_Chinese(self):
        """
        Does "hello 愚公移山" get identified?
        """
        expect = u"[PASS] classify: 愚公移山"
        lexer = test_CodepointLexer(InputStream(u"hello 愚公移山"))
        stream = CommonTokenStream(lexer)
        parser = test_CodepointParser(stream)
        tree = parser.prog()
        printer = test_CodepointPrintListener()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)

        self.assertEquals(expect,
                str(printer),
                Self.doc())
