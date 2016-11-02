# -*- coding: utf8 -*-
import unittest2

from UniTree import ( UniTree )

import inspect
class UniTreeTestCase(unittest2.TestCase):

    def setUp(self):
        self.tree = UniTree()

    def tearDown(self):
        pass

    def doc(self, msg = ""):
        more = " (%s)" % (msg) if msg else ""
        frame = inspect.currentframe().f_back
        for objref in frame.f_globals.values():
            if inspect.isfunction(objref):
                if objref.func_code == frame.f_code:
                    return objref.__doc__ + more
            elif inspect.isclass(objref):
                for name, member in inspect.getmembers(objref):
                    if inspect.ismethod(member):
                        if member.im_func.func_code == frame.f_code:
                            return member.__doc__ + more

    def test_selfdoc(self):
        """Check for __doc__ string access"""
        d="Check for __doc__ string access"
        self.assertEqual(d, self.doc(), self.doc())

    def test_0_size(self):
        """Empty tree: size is 0"""
        self.assertEqual(len(self.tree), 0, self.doc())

    def test_0_find_fails(self):
        """Empty tree: finding word returns False"""
        self.assertEqual(self.tree['hello'], False, self.doc())

    def test_0_delete_fails(self):
        """Empty tree: deleting word returns None"""
        self.assertEqual(self.tree.delete('hello'), None, self.doc())

    def test_1_size(self):
        """Tree of 1 word: size is 1"""
        self.tree('hello')
        self.assertEqual(len(self.tree), 1, self.doc())

    def test_1_pass(self):
        """Tree of 1 word: find word returns set with word found"""
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), self.doc())

    def test_1_fail(self):
        """Tree of 1 word: find other word returns False"""
        self.tree('hello')
        self.assertEqual(self.tree['world'], False, self.doc())

    def test_2_size(self):
        """Tree of 2 words: size is 2"""
        self.tree(['hello', 'world'])
        self.assertEqual(len(self.tree), 2, self.doc())

    def test_2_pass(self):
        """Tree of 2 words: find words passing"""
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hello'], set(['hello']), self.doc())
        self.assertEqual(self.tree['world'], set(['world']), self.doc())

    def test_2_fail(self):
        """Tree of 2 words: find other words failing"""
        self.tree(['hello', 'world'])
        self.assertEqual(self.tree['hi'], False, self.doc())
        self.assertEqual(self.tree['globe'], False, self.doc())

    def test_2_size_idempotent(self):
        """Tree of 2 words: adding same word has no effect on size"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(len(self.tree), 2, self.doc())

    def test_2_pass_idempotent(self):
        """Tree of 2 words: adding same word has no effect on find passing"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hello'], set(['hello']), self.doc())
        self.assertEqual(self.tree['world'], set(['world']), self.doc())

    def test_2_fail_idempotent(self):
        """Tree of 2 words: adding same word has no effect on find failing"""
        self.tree(['hello', 'world'])
        self.tree('hello')
        self.assertEqual(self.tree['hi'], False, self.doc())
        self.assertEqual(self.tree['globe'], False, self.doc())

    def test_canonical_individual(self):
        """Tree with word variations: passing"""
        (word, similar) = ('hello', ['helo', 'hllo'])
        self.tree(word)
        for like in similar:
            self.tree.word(word, like)
        for like in similar:
            self.assertEqual(self.tree[like], set([word]), self.doc(like))

    def test_canonical_bulk(self):
        """Tree with word variations: passing"""
        (word, similar) = ('hello', ['helo', 'hllo'])
        self.tree(word)
        self.tree.word(word, similar)
        for like in similar:
            self.assertEqual(self.tree[like], set([word]), self.doc(like))

    def test_delete_size(self):
        """Tree word deletion: size decrements by 1"""
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(len(self.tree), 1, self.doc())

    def test_delete_pass(self):
        """Tree word deletion: find passing for remaining word"""
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(self.tree['hello'], set(['hello']), self.doc())

    def test_delete_fail(self):
        """Tree word deletion: find failing for deleted word"""
        """ """
        self.tree(['hello', 'world'])
        self.tree.delete('world')
        self.assertEqual(self.tree['world'], False, self.doc())

    def test_Chinese(self):
        """Tree accepts CJK characters"""
        words = [ '愚', '公', '移', '山' ]
        self.tree(words)
        for word in words:
            self.assertEqual(self.tree[word], set([word]), self.doc(word))
        self.assertEqual(len(self.tree), 4, self.doc("4 CJK chars"))
        self.tree.delete(words[0])
        self.assertEqual(self.tree[words[0]], False, self.doc("del CJK char"))
        self.assertEqual(len(self.tree), 3, self.doc("3 CJK chars"))
