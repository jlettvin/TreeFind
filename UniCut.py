#!/usr/bin/env python
# -*- coding: utf8 -*-

"""UniCut.py

Usage:
    UniCut.py [-v] [INTEGER...]
    UniCut.py -j
    UniCut.py -t
    UniCut.py (-h)
    UniCut.py (--version)

Options:
    -t --test                       Run some tests
    -j --javascript                 Produce javascript
    -v --verbose                    Show details of operation
    -h --help                       Show this Usage message
    --version                       Show version

Concepts:
    This module generates efficient lookup trees for converting
    digits in 37 lnguages supported by Unicode to internal digits
    for multi-language math.

STRING
STRING... can be strings with mixed language characters
They will be read, cut, and shown as trees.

Author  : Jonathan D. Lettvin (jlettvin@gmail.com)
Date    : 20161113
Legal   : Copyright(c)2016 Jonathan D. Lettvin, All Rights Reserved
License : GPL 3.0
"""

__module__     = "UniCut.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = ["Jonathan D. Lettvin"]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161106"

from UniDict import UniDict

class UniCut(list):

    default = UniDict(bits = 3, base = 10, codepointBits = 21, reverse=True)
    default(
        enum = 1 << default.bits,
        need = (
            (default.codepointBits / default.bits) +
            int((default.codepointBits % default.bits) != 0)))
    default(mask = default.enum - 1, poss = default.need * default.bits)

    def __init__(self, **kw):
        self.the = UniDict(**UniCut.default)
        self.the.update(**kw)
        if self.the.bits != UniCut.default['bits']:
            self.the(
                enum = 1 << self.bits,
                need = (
                    (self.the.codepointBits / self.the.bits) +
                    int((self.the.codepointBits % self.the.bits) != 0)))
            self.the(mask = enum - 1, poss = self.the.need * self.the.bits)
        # Initialize the list of lists
        self.append([-1] * self.the.enum)

    #def __call(self, codepoint, digit=-1):
        #cuts = self.cut(codepoint):
            #N = len(self)
            #if self[this][segment] == -1:
                #pass

    def cut(self, c):
        cuts = [
            (c >> (shft * self.the.bits)) & self.the.mask
            for shft in range(self.the.need)]
        if self.the.reverse:
            cuts.reverse()
        return cuts

    def insert(self, c):
        pass


if __name__ == "__main__":

    def main():
        pass

    main()
