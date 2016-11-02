#!/usr/bin/env python
# -*- coding: utf8 -*-

from pprint import pprint

# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
class CodepointTree(set):
    """
    CodepointTree instances as uctree, a tree for fast specified word lookup.

    uctree(word)            functor adds word to the tree.
    uctree[word]            getitem returns True if word is in the tree.
    uctree.delete(word)     remove word from tree
    uctree(word, "delete")  remove word from tree

    A word or list of words may be given while instancing.
    A word or list of words may be added after instancing by functor.

    For canonicalization of word variants, the terminal is a set such that
    common tree variations for dissimilar words can have multiple results.

    TODO; when deleting word, delete its variations (remove from word lists).
    """

    end = 0xFFFF  # 0xFFFF is a non-character so it is usable as the end key.

    #@staticmethod
    #def variations(word):
        #return []

    def __init__(self, wordlist=[], **kw):
        self.tree = {}
        self(wordlist)

    def also(self, word, variation=None):
        (size, temp) = (len(word), self.tree)
        if not variation:
            variation = word
        for o in (ord(c) for c in variation):
            temp[o] = temp.get(o, {})
            temp = temp[o]
        if not temp.get(CodepointTree.end):
            temp[CodepointTree.end] = set([word])
        else:
            temp[CodepointTree.end].add(word)
        self.add(word)
        return self

    def __call__(self, word, *args):
        "also or delete a word or list of words to the tree"
        if type(word) == type([]):
            map(self, word)
        else:
            if "delete" in args:
                self.delete(word)
            else:
                self.also(word)
                self.add(word)
                # TODO: variations mechanism doesn't work yet.
                #for variant in CodepointTree.variations(word):
                    #self.also(word, variant)
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
            terminal = tree and CodepointTree.end in tree
            if terminal:
                tree[CodepointTree.end].discard(word)
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
        return temp.get(CodepointTree.end, False)

# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
if __name__ == "__main__":
    """
    Running this file as a program executes the tests.
    """

    pf = [ '[PASS] %s: %s', '[FAIL] %s: %s']
    data = {
        'bwords': [ 'bye', 'bitterling', 'beneficially' ],
        'hwords': [ 'hello', 'hi', 'hola', 'hold', 'hole', 'holy' ],
        '_words': [ '愚', '公', '移', '山' ],
        'qwords': [ 'quick' ]
    }

    def toPass(uctree, words, msg):
        result = ( data[words] == [uctree[w] for w in data[words]] )
        print pf[result] % (words, msg)

    def toFail(uctree, words, msg):
        result = (     [     ] == [uctree[w] for w in data[words]] )
        print pf[result] % (words, msg)

    def variations(word):
        result = []
        for i in range(1, len(word)-1):
            result.append(word[0:i]+word[i+1:])
        return result

    def test1():
        # Note, we take all but the bwords
        uctree = CodepointTree(data['hwords'])(data['_words'])

        toPass(uctree, 'hwords', '    in uctree ASCII characters after taking')
        toPass(uctree, '_words', '    in uctree CJK   characters after taking')

        toFail(uctree, 'bwords', 'not in uctree before taking')
        uctree(data['bwords'])
        toPass(uctree, 'bwords', '    in uctree after  taking')

        for word in data['bwords']:
            uctree(word, "delete")
        toFail(uctree, 'bwords', 'not in uctree after  deleting')
        for word in data['hwords']:
            uctree.delete(word)
        toFail(uctree, 'hwords', 'not in uctree after  deleting')

        toPass(uctree, '_words', '    in uctree CJK   characters after bh del')

        CodepointTree.variations = variations
        variants = variations('quick')
        uctree.also('quick')
        for variant in variants:
            uctree.also('quick', variant)
        for variant in variants:
            toPass(uctree, 'qwords', '(%s is a variant of %s)' % (
                variant, list(uctree[variant])[0]
            ))

    def test2():
        uctree = CodepointTree(['hello', 'world'])
        uctree.delete('world')
        print len(uctree)
        print uctree['hello']
        print uctree['world']

    def test():
        test1()
        test2()

    test()
