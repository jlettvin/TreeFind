#!/usr/bin/env python
# -*- coding: utf8 -*-

"""UniDigit.py

Usage:
    UniDigit.py [-v] [INTEGER...]
    UniDigit.py -j
    UniDigit.py -t
    UniDigit.py (-h)
    UniDigit.py (--version)

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

INTEGERS... can be strings have mixed digits from any supported language.
They will be read and shown in ASCII.

Author  : Jonathan D. Lettvin (jlettvin@gmail.com)
Date    : 20161106 
Legal   : Copyright(c)2016 Jonathan D. Lettvin, All Rights Reserved
License : GPL 3.0
"""

__module__     = "UniDigit.py"
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
__date__       = "20161106"

import codecs

class UniDigit(list):
    """
    This class ingests UnicodeData.txt and organizes digits from all languages
    into an efficient search tree for conversions.
    """

    class UnicodeDataLine(dict):
        """
        This class supports turning a line into a Unicode compliant dictionary.
        """

        def __init__(self, columnNames):
            self.__dict__ = self
            self.columnNames = columnNames

        def __call__(self, line):
            if not line:
                return False
            line = line.split(';')
            if len(line) != len(self.columnNames):
                return False
            self.update(dict(zip(self.columnNames, line)))
            return True

    def _columnNameIngest(self):
        """ftp://ftp.unicode.org/Public/3.0-Update/UnicodeData-3.0.0.html
        Column names are hand copied from this URL changing ' ' and '.' to '_',
        and changing 10646_comment_field to comment_field_10646,
        and changing column 0 to its common name: Codepoint.
        It is possible to extract column names using BeautifulSoup but
        the added complexity over using manifest constants is not merited.
        The alternative is to use BeautifulSoup to extract column names from
        TR44 which is organized poorly for column name extraction.
        These names become member names in a UnicodeDataLine instance.
        This considerably simplifies maintenance relative to the publications.
        """
        Unicode_3_0_0_columns = """
Codepoint
Character_name
General_Category
Canonical_Combining_Classes
Bidirectional_Category
Character_Decomposition_Mapping
Decimal_digit_value
Digit_value
Numeric_value
Mirrored
Unicode_1_0_Name
comment_field_10646
Uppercase_Mapping
Lowercase_Mapping
Titlecase_Mapping
        """
        columnNames = Unicode_3_0_0_columns.strip().split('\n')
        self.line = UniDigit.UnicodeDataLine(columnNames)

    def _digitDataIngest(self):
        with open("local/UnicodeData.txt") as source:
            while True:
                if not self.line(source.readline()):
                    break
                if self.line.General_Category == 'Nd':
                    codepoint = int(self.line.Codepoint, 0x10)
                    digit = int(self.line.Digit_value)
                    languageparts = self.line.Character_name.split(' ')[:-2]
                    language = ' '.join(languageparts)
                    if language.strip() == "":
                        language = 'ASCII'
                    self.codepointToLanguage[codepoint] = language
                    self.codepointToDigit[codepoint] = digit
                    self.integerToCodepointList[digit].append(codepoint)
                    if self.wide or codepoint < 0x10000:  # unichr restriction
                        self.languageToDigits[language] = self.languageToDigits.get(language, "")
                        self.languageToDigits[language] += unichr(codepoint)

    def _ingest(self):
        if self.kw.get('ingest', False):
            self.integerToCodepointList = {i:[] for i in range(10)}
            self.codepointToDigit = {}
            self.codepointToLanguage = {}
            self.languageToDigits = {}

            self._columnNameIngest()
            self._digitDataIngest()

            if self.verbose:
                print(str(self.integerToCodepointList))
            for d in self.integerToCodepointList.keys():
                for c in self.integerToCodepointList[d]:
                    self(c, d)
        elif self.kw.get('unique', False):
            #self(ord('0'), 0)
            for d, c in enumerate(u"0123456789"):
                self(ord(c), d)
        else:
            for d, c in enumerate(u"0123456789"):
                self(ord(c), d)
            for d, c in enumerate(u"௦௧௨௩௪௫௬௭௮௯"):
                self(ord(c), d)
        return self

    def sequence(self, language=None):
        if language is None:
            return self.languageToDigits.keys()
        return self.languageToDigits.get(language, "unknown")

    def whatLanguageIs(self, codepoint):
        if type(codepoint) == type(u""):
            codepoint = ord(codepoint)
        return self.codepointToLanguage.get(codepoint, 'Unknown')

    def _cut(self, c, d=None):
        cuts = [(c>>(shft*self.bits)) & self.mask for shft in range(self.need)]
        cuts.reverse()
        (type(d) == type(int)) and cuts.append(d)
        return cuts

    def __init__(self, **kw):
        self.kw = kw
        self.verbose = self.kw.get('verbose', False)
        self.codepointToDigit = {}
        codepointBits = 21
        self.base = 10
        self.wide = self.kw.get('wide', False)
        self.bits = self.kw.get('bits', 3)  # 3:8-bit tables, 4:16-bit tables
        self.enum = 1 << self.bits
        self.mask = self.enum - 1
        self.need = (codepointBits / self.bits)
        self.need += int((codepointBits % self.bits) != 0)
        self.poss = self.need * self.bits
        for _ in range(self.base):
            self.append([_] * self.enum)
        self.append([-1] * self.enum)
        self._ingest()

    def __call__(self, codepoint, digit=-1):
        if type(codepoint) in [type(u""), type("")]:
            codepoint = ord(codepoint)
        this = 10
        if digit == -1:
            # get mode
            cuts = self._cut(codepoint)
            for segment in cuts:
                this = self[this][segment]
                if this < self.base:
                    return this
            return digit
        else:
            # put mode
            cuts = self._cut(codepoint)
            if self.verbose:
                print("    INSERT %d %06x %s" % (digit, codepoint, cuts))
            for segment in cuts[:-1]:
                N = len(self)
                that = this
                if self[this][segment] == -1:
                    if this < self.base:
                        self[this][segment] = digit
                    else:
                        self[this][segment] = N
                        self.append([-1] * self.enum)
                        this = N
                else:
                    this = self[this][segment]
                if self.verbose:
                    print 'self[%d][%d] = %d' % (this, segment, this)
            self[this][cuts[-1]] = digit

    def productions(self, target):
        show = u"""
document.jlettvin = {};
document.jlettvin.unidigit = {
/** UniDigit tables for handling digits in all Unicode supported alphabets.
Unicode strings containing numbers may be converted to integer,
arithmetic operations may be performed,
and the result output generated in the alphabet of choice.
Digits may be freely intermixed in number strings.
 */
"""

        # TODO Fix the bug in this code
        show += u"var integerToCodepointList = [\n    "
        show += u',\n    '.join([
            u"%d => %s" % (i, str(self.integerToCodepointList[i]))
            for i in range(10)])
            #for k, w in self.integerToCodepointList.iteritems()])
        show += u"\n];\n"

        show += u"var codepointToDigit = [\n    "
        show += u'\n    '.join([
            u"0x%06x => '%d'" % (k, w)
            for k, w in self.codepointToDigit.iteritems()])
        show += u"\n];\n"

        show += u"var codepointToLanguage = [\n    "
        show += u',\n    '.join([
            u"0x%06x => '%s'" % (k, w)
            for k, w in self.codepointToLanguage.iteritems()])
        show += u"\n];\n"

        show += u"var languageToDigits = [\n    "
        show += u',\n    '.join([
            u"'%s' => '%s'" % (k, w)
            for k, w in self.languageToDigits.iteritems()])
        show += u"\n];\n"

        show += u"var digitLookup = [\n    "
        show += u',\n    '.join([
            u"%3d => %s" % (index, str(page))
            for index, page in enumerate(self)])
        show += u"\n];\n"

        show += """
var cutCodepoint = function(codepoint) {
    var bits = %d;
    var mask = %d;
    var need = %d;
    var cuts = new int[need];
    for (var shft = need; shft--; ) {
        cuts[need-shft-1] = codepoint >> (shft * bits) & mask;
    }
    return cuts;
};

var asDigit = function(codepoint) {
    var cuts = cutCodepoint(codepoint);
    var this = %d;
    var base = %d;
    var done = null;
    for (var segment of cuts) {
        var this = digitLookup[this][segment];
        if (this < base) {
            done = this;
            break;
        }
    }
    cuts = null;
    return done == null ? -1 : done;
};
};
""" % (self.bits, self.mask, self.need, self.base, self.base)

        return show

    def emit(self):
        with open('UniDigit.js', 'w+b') as target:
            UTF8Writer = codecs.getwriter('utf8')
            target = UTF8Writer(target)
            print>>target, self.productions(target)
        return self

if __name__ == "__main__":

    class Arg(dict):
        """Arg
        This class enables direct use of dictionary elements as class members.
        For example: self["foo"] is identical to self.foo.
        Command-line options typically have '-' characters which are stripped.
        """

        def __init__(self, **kw):
            self.__dict__ = self
            self.update({ k.strip('-'): w for k, w in kw.iteritems() })

    def test():
        unidigit = UniDigit(ingest=True, unique=False)
        failpass = ['[FAIL] %d u%06x %s', '[PASS] %d u%06x %s']
        total = 0
        okay = 0
        languages = sorted(unidigit.languageToDigits.keys())
        for language in languages:
            digits = unidigit.languageToDigits[language]
            for digit, char in enumerate(digits):
                total = total + 1
                codepoint = ord(char)
                result = int(unidigit(codepoint) == digit)
                okay = okay + result
                print failpass[result] % (digit, codepoint, language)
        print '[PASS] %d Nd codepoints' % (okay)
        fail = total - okay
        if fail != 0:
            print '[FAIL] %d' % (total - okay)

    from docopt import docopt
    from pprint import pprint

    def main():
        arg = Arg(**docopt(__doc__, version=__version__))
        if arg.verbose:
            pprint(arg)

        if arg.test:
            test()
        else:
            unidigit = UniDigit(ingest=False, unique=True)
            if arg.javascript:
                unidigit.emit()

            for string in arg.INTEGER:
                value = 0
                for codepoint in string.decode('utf-8'):
                    o = ord(codepoint)
                    print '%s %06x' % (codepoint, o),
                    value = value * 10 + unidigit(o)
                print value

            #pprint(unidigit)

    main()