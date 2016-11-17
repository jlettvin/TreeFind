#!/usr/bin/env python
# -*- coding: utf8 -*-
# pylint: disable=too-few-public-methods

"""UniClass.py
A namespace for identifying a codepoint character class.

This module has been hand-crafted for Unicode 9.0.0.
It is constructed by extracting data from UnicodeData.txt and PropList.txt,
both being core normative Unicode resources.
UnicodeData.txt has a linear sequence of codepoints with gaps.
PropList.txt has groups of individual codepoint and codepoint ranges.
Both identify a label given in column 3 of UnicodeData.txt.
PropList.txt may be sufficient, but redundancy is not problematic.

The properties (label) count is 30 (0-29) including '__' for error.
A linear string of bytes having values 0-29 of length 0x110000 is constructed
where byte values are indices of the property (label) name in the label list.

The advantage for this method is that vast tracts of unicode comprise
codepoints sharing a single property.  These are excellent statistics for
compression of the string by bz2 encoded in b64.  The count of bytes in the b64
is 4204 bytes representing a complete set of properties for 1114112 codepoints.

These 4204 bytes are decompressed to 1114112 bytes of property label indices
at module import time (class member initialization).
The memory footprint of this module is slightly more than 1MiB.
Once decompressed, the time to determine a label is simply a double dereference
with the codepoint dereferencing a index byte from the decompressed string and
the index byte dereferencing a property label from the label list.
This is an O(1) operation where a dictionary lookup would be O(logN) at least
if dictionaries are used.  Also, no branch points are used.

The label list contains an alphabetically sorted sequence of
all the documented codepoint classifications and
'__' is used for errors although it is not a legal classifier.

The index string contains a b64 encoded bz2 compressed string which expands to
a string of length 0x110000, which means that
there is one character for each valid codepoint in all of Unicode 9.0.0.

Each character is actually an ordinal which is a direct index into label.
label could be a list instead of a dictionary.
"""

__module__     = "UniClass.py"
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
__date__       = "20161110"

import bz2


class UniClass(object):
    "Identify the Unicode gc class of a codepoint."

    label = ["__",  # Added index 0 error label '__' to existing labels.
             "Cc", "Cf", "Cn", "Co", "Cs", "Ll", "Lm", "Lo", "Lt", "Lu",
             "Mc", "Me", "Mn", "Nd", "Nl", "No", "Pc", "Pd", "Pe", "Pf",
             "Pi", "Po", "Ps", "Sc", "Sk", "Sm", "So", "Zl", "Zp", "Zs"]
    index = bz2.decompress("""
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
Jt4TdgiKWlR/8XckU4UJCdVo7kA=
""".decode('base64'))

    @staticmethod
    def classify(codepoint):
        "This fetches a codepoint gc classification by multiple dereference"
        codepoint = codepoint if isinstance(codepoint, int) else ord(codepoint)
        return UniClass.label[ord(UniClass.index[codepoint])]

if __name__ == "__main__":

    for c in u"ABCabc012$=*愚公移山":
        print "%s\t%06x\t%s" % (c, ord(c), UniClass.classify(c))
