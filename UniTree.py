#!/usr/bin/env python
# -*- coding: utf8 -*-

__module__     = "UniTree.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = [ "Jonathan D. Lettvin" ]
__license__    = "GPLv3"
__version__    = "0.0.3"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161102"

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

    end = 0xFFFF  # 0xFFFF is a non-character so it is usable as the end key.

    def __init__(self, wordlist=[], **kw):
        self.tree = {}
        self(wordlist)

    def word(self, word, variation=None):
        (size, temp) = (len(word), self.tree)
        if not variation:
            variation = word
        for o in (ord(c) for c in variation):
            temp[o] = temp.get(o, {})
            temp = temp[o]
        if not temp.get(UniTree.end):
            temp[UniTree.end] = set([word])
        else:
            temp[UniTree.end].add(word)
        self.add(word)
        return self

    def __call__(self, word, *args):
        "word or delete a word or list of words to the tree"
        if type(word) == type([]):
            map(self, word)
        else:
            if "delete" in args:
                self.delete(word)
            else:
                self.word(word)
                self.add(word)
                # TODO: internal variations mechanism doesn't work yet.
                #for variant in UniTree.variations(word):
                    #self.word(word, variant)
        return self

    def delete(self, word, tree=False, level=0, N=0):
        "Prune a word or list of words from the tree"
        if tree is False:
            tree = self.tree
            N = len(word)
            level = 0

        if N <= level:
            self.discard(word)
            unique = (tree and (len(tree) == 1))
            terminal = tree and UniTree.end in tree
            if terminal:
                tree[UniTree.end].discard(word)
            return unique and terminal

        C = word[level]
        O = ord(C)
        if O in tree:
            if self.delete(word, tree[O], level + 1, N) and len(tree) == 1:
                del tree[O]
                return True
            return False

    def __getitem__(self, word):
        "Find a word in the tree"
        temp = self.tree
        for o in (ord(c) for c in word):
            temp = temp.get(o, {})
            if temp == {}:
                break
        return temp.get(UniTree.end, False)
