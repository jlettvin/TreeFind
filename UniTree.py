#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
This module creates word trees, splices, prunes, and queries.
"""

__module__     = "UniTree.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = ["Jonathan D. Lettvin"]
__license__    = "GPLv3"
__version__    = "0.0.3"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161102"

from CPT import CPT


# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
class UniTree(set):
    """
    UniTree instances as unitree, a tree for fast specified word lookup.

    unitree(word)               functor adds word to tree.
    unitree[word]               getitem returns True if word is in tree.
    unitree(word, "delete")     remove word from tree
    unitree.delete(word)        remove word from tree
    unitree.word(word, variant) add variant targeting word to tree

    A word or list of words may be given while instancing.
    A word or list of words may be added after instancing by functor.

    For canonicalization of word variants, the terminal is a set such that
    common tree variations for dissimilar words can have multiple results.

    TODO; when deleting word, delete its variations (remove from word lists).
    """

    def __init__(self, **kw):
        self.kw = kw
        self.wordlist = kw.get('wordlist', [])
        self.case = kw.get('ignorecase', False)
        self.end = kw.get('end', 0xFFFF)  # non-codepoint usable as end key.
        self.tree = {}  # CPT()  # {}
        self(self.wordlist)

    def word(self, root, also=None):
        "For a word, insert it into tree or retrieve it from tree"
        if isinstance(also, list):
            for variation in also:
                self.word(root, variation)
            return self
        fork = self.tree
        if not also:
            also = root
        for o in (ord(c) for c in also):  # iteration costs less than recursion
            fork[o] = fork.get(o, {})
            fork = fork[o]
        if not fork.get(self.end):
            fork[self.end] = set([root])
        else:
            fork[self.end].add(root)
        self.add(root)
        return self

    def __call__(self, word, *args):
        "word or delete a word or list of words to the tree"
        if isinstance(word, list):
            map(self, word)
        else:
            if "delete" in args:
                self.delete(word)
            else:
                self.word(word)
                self.add(word)
                # TODO: internal variations mechanism doesn't work yet.
                # for variant in UniTree.variations(word):
                #     self.word(word, variant)
        return self

    def delete(self, root, tree=False, level=0, N=0):
        "Prune a word or list of words from the tree"
        # TODO delete variations as well as root
        if tree is False:
            tree = self.tree
            N = len(root)
            level = 0

        if N <= level:
            self.discard(root)
            unique = (tree and (len(tree) == 1))
            terminal = tree and self.end in tree
            if terminal:
                tree[self.end].discard(root)
            return unique and terminal

        C = root[level]
        O = ord(C)
        if O in tree:
            if self.delete(root, tree[O], level + 1, N) and len(tree) == 1:
                del tree[O]
                return True
            return False

    def _graphviz(self, tree, token=u""):
        text = u""
        for k, w in tree.iteritems():
            if k == self.end:
                terminal = u','.join(w)
                text += u'"%s" -> "[%s]" [label="$"];\n' % (token, terminal)
                text += u'"[%s]" -> "STOP";\n' % (terminal)
            else:
                newtoken = token + unichr(k)
                text += u'"%s";\n' % (newtoken)
                if token is not u"":
                    label = u'[label="' + unichr(k) + u'"];'
                    text += u'"%s" -> "%s" %s\n' % (token, newtoken, label)
                text += self._graphviz(w, newtoken)
                if tree == self.tree:
                    fmt = '"START" -> "%s" [label="%s"];\n'
                    text += fmt % (newtoken, unichr(k))
        return text

    def graphviz(self, dotname="UniTree.dot"):
        "Produce .dot file for use by graphviz external program"
        head = 'digraph tree {\n  rankdir=LR;\n  concentrate=true;\n'
        tail = "}"

        with open(dotname, "w+b") as dotstream:
            try:
                print>>dotstream, head + self._graphviz(self.tree) + tail
            except Exception as why:  # pylint: disable=broad-except
                print("Can't output: %s(%s)" % (dotname, str(why)))
            finally:
                pass

    def __getitem__(self, find):
        "Find in the tree"
        fork = self.tree
        for o in (ord(c) for c in find):
            fork = fork.get(o, {})
            if fork == {}:
                break
        return fork.get(self.end, False)
