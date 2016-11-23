#!/usr/bin/env python
# -*- coding: utf8 -*-

"""CPT.py: an O(1) table lookup for codepoint:table pairs."""

__module__     = "CPT.py"
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
__date__       = "20161121"

from UniCut import UniCut


class CPT(object):
    "Code Point Table."

    def _preinit(self):
        "Internal function for initializing the lookup table"
        self.base, self.data = [1, [[0] * self.size, [0] * self.size]]

    def __init__(self):
        "Setup sizing, lookup table, and redo dictionary"
        self.snip = UniCut()
        self.size = self.snip.the.enum
        self._preinit()
        self.redo = {}

    def __setitem__(self, glyph, table):
        "Set the table number for the glyph.  TODO develop __delitem__  method"
        codepoint = glyph if isinstance(glyph, int) else ord(glyph)
        this, cuts = [1, self.snip.cut(codepoint)]
        self.redo[codepoint] = table
        for segment in cuts[:-1]:
            N = len(self.data)
            if self.data[this][segment] == 0:
                if this < self.base:
                    self.data[this][segment] = table
                else:
                    self.data[this][segment] = N
                    self.data.append([0] * self.size)
                    this = N
            else:
                this = self.data[this][segment]
        self.data[this][cuts[-1]] = -table

    def __getitem__(self, glyph):
        "Get the table number for the glyph"
        codepoint = glyph if isinstance(glyph, int) else ord(glyph)
        cuts = self.snip.cut(codepoint)
        this = 1
        for segment in cuts:
            this = self.data[this][segment]
        return -this

    def __delitem__(self, glyph):
        "Remove glyph:table association from lookup table"
        codepoint = glyph if isinstance(glyph, int) else ord(glyph)
        present = self[codepoint]
        if present != 0:
            del self.redo[codepoint]    # Eliminate codepoint from lookup table
            self._preinit()             # Initialize the lookup table
            for codepoint, table in self.redo.iteritems():
                self[codepoint] = table     # Refill the lookup table

    def __len__(self):
        "Return the count of glyphs available for lookup"
        return len(self.redo.keys())


if __name__ == "__main__":
    testdata = u"abcdefghij我有一个绰号愚公移山"
    testdict = {c: (n + 1) * 100 for n, c in enumerate(testdata)}
    test1 = ''.join([c for n, c in enumerate(testdata)])
    test2 = ''.join([c for n, c in enumerate(testdata) if (n % 2) == 0])
    test3 = ''.join([c for n, c in enumerate(testdata) if (n % 3) == 0])
    test5 = ''.join([c for n, c in enumerate(testdata) if (n % 5) == 0])
    dict1 = {ord(c):testdict[c] for c in test1}
    dict2 = {ord(c):testdict[c] for c in test2}
    dict3 = {ord(c):testdict[c] for c in test3}
    dict5 = {ord(c):testdict[c] for c in test5}
    cpt = CPT()
    for codepoint, table in dict1.iteritems():
        cpt[codepoint] = table
        print "POKE\t%s\t%06x\t%d" % (unichr(codepoint), codepoint, table)
    for codepoint, table in dict3.iteritems():
        del cpt[codepoint]
        print "PULL\t%s\t%06x\t%d" % (unichr(codepoint), codepoint, table)
    for codepoint, table in dict1.iteritems():
        table = cpt[codepoint]
        print "PEEK\t%s\t%06x\t%d" % (unichr(codepoint), codepoint, table)
    print "Length: %d" % (len(cpt))
