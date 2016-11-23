# -*- coding: utf8 -*-

__module__     = "test_UniTree.py"
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

from UniTree  import (UniTree)
from Self     import (Self   )


class UniTreeTestCase(unittest2.TestCase):

    def setUp(self):
        self.tree = UniTree()

    def tearDown(self):
        pass

    def test_selfdoc(self):
        """Check for __doc__ string access"""
        d="Check for __doc__ string access"
        self.assertEqual(d, Self.doc(), Self.doc())

    def test_0_size(self):
        """Empty tree: size is 0"""
        self.assertEqual(len(self.tree), 0, Self.doc())

    def test_0_find_fails(self):
        """Empty tree: finding word returns False"""
        self.assertEqual(self.tree['hello'], False, Self.doc())

    def test_0_delete_fails(self):
        """Empty tree: deleting word returns None"""
        self.assertEqual(self.tree.delete('hello'), None, Self.doc())

    def test_1_size(self):
        """Tree of 1 word: size is 1"""
        self.tree('hello')
        self.assertEqual(len(self.tree), 1, Self.doc())

    def test_1_pass(self):
        """Tree of 1 word: find word returns set with word found"""
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), Self.doc())

    def test_1_fail(self):
        """Tree of 1 word: find other word returns False"""
        self.tree('hello')
        self.assertEqual(self.tree['world'], False, Self.doc())

    def test_2_size(self):
        """Tree of 2 words: size is 2"""
        self.tree(['hello', 'world'])
        self.assertEqual(len(self.tree), 2, Self.doc())

    def test_2_pass(self):
        """Tree of 2 words: find words passing"""
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hello'], set(['hello']), Self.doc())
        self.assertEqual(self.tree['world'], set(['world']), Self.doc())

    def test_2_fail(self):
        """Tree of 2 words: find other words failing"""
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hi'], False, Self.doc())
        self.assertEqual(self.tree['globe'], False, Self.doc())

    def test_2_size_idempotent(self):
        """Tree of 2 words: adding same word has no effect on size"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(len(self.tree), 2, Self.doc())

    def test_2_pass_idempotent(self):
        """Tree of 2 words: adding same word has no effect on find passing"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), Self.doc())
        self.assertEqual(self.tree['world'], set(['world']), Self.doc())

    def test_2_fail_idempotent(self):
        """Tree of 2 words: adding same word has no effect on find failing"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hi'], False, Self.doc())
        self.assertEqual(self.tree['globe'], False, Self.doc())

    def test_canonical_individual(self):
        """Tree with word variations: passing"""
        (word, similar) = ('hello', ['helo', 'hllo'])
        self.tree(word)
        for like in similar:
            self.tree.word(word, like)
        for like in similar:
            self.assertEqual(self.tree[like], set([word]), Self.doc(like))
        self.tree.graphviz("test_UniTree_%s.dot" % (Self.name()))

    def test_canonical_four(self):
        """Tree with word variations: passing"""
        many = [
            ('hello', ['helo', 'hllo']),
            ('world', ['wrld', 'word']),
            ('word' , []),
            ('hell' , [])
        ]
        for (word, similar) in many:
            self.tree(word)
            self.tree.word(word, similar)
            for like in similar:
                self.assertEqual(self.tree[like], set([word]), Self.doc(like))
        self.tree.graphviz("test_UniTree_%s.dot" % (Self.name()))

    #"""
    # These unit tests work with dict in UniTree.py
    # These unit tests are excluded when using CPT in UniTree.py
    # TODO When CPT is re-implemented in C, re-introduce these test methods
    def test_canonical_unix_words(self):
        "Tree with thousands of words: passing"
        with open("../local/words") as text:
            words = text.read().split()
            self.tree(words)
            for word in words:
                self.assertEqual(self.tree[word], set([word]), Self.doc())

    def test_canonical_100_words(self):
        "Tree with 100 words: passing"
        with open("../local/words.100.txt") as text:
            words = text.read().split()
            self.tree(words)
            for word in words:
                self.assertEqual(self.tree[word], set([word]), Self.doc())
        self.tree.graphviz("test_UniTree_%s.dot" % (Self.name()))
    #"""

    def test_delete_size(self):
        """Tree word deletion: size decrements by 1"""
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(len(self.tree), 1, Self.doc())

    def test_delete_pass(self):
        """Tree word deletion: find passing for remaining word"""
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(self.tree['hello'], set(['hello']), Self.doc())

    def test_delete_fail(self):
        """Tree word deletion: find failing for deleted word"""
        """ """
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(self.tree['world'], False, Self.doc())

    def test_Chinese(self):
        """Tree accepts CJK characters"""
        words = [ '愚', '公', '移', '山' ]
        self.tree(words)
        for word in words:
            self.assertEqual(self.tree[word], set([word]), Self.doc(word))
        self.assertEqual(len(self.tree), 4, Self.doc("4 CJK chars"))
        self.tree.delete(words[0])
        self.assertEqual(self.tree[words[0]], False, Self.doc("del CJK char"))
        self.assertEqual(len(self.tree), 3, Self.doc("3 CJK chars"))
        #self.tree.graphviz("test_UniTree_%s.dot" % (Self.name()))
