#!/usr/bin/env python
# -*- coding: utf8 -*-

# CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
class UCTree(object):
    """
    UCTree instances as uctree, a tree for fast specified word lookup.

    uctree(word)            functor adds word to the tree.
    uctree[word]            getitem returns True if word is in the tree.
    uctree.delete(word)     remove word from tree
    uctree(word, "delete")  remove word from tree

    A word or list of words may be given while instancing.
    A word or list of words may be added after instancing by functor.
    """

    end = 0xFFFF  # 0xFFFF is a non-character so it is usable as the end key.

    def __init__(self, wordlist=[]):
        self.tree = {}
        self(wordlist)

    def __call__(self, word, *args):
        "Add or delete a word or list of words to the tree"
        if type(word) == type([]):
            map(self, word)
        else:
            if "delete" in args:
                self.delete(word)
            else:
                (size, temp) = (len(word), self.tree)
                for o in (ord(c) for c in word):
                    temp[o] = temp.get(o, {})
                    temp = temp[o]
                temp[UCTree.end] = word
        return self

    def delete(self, word, level=0, tree=None):
        "Prune a word or list of words from the tree"
        tree == tree if tree else self.tree
        if len(word) >= level:
            return tree and UCTree.end in tree and len(tree) == 1
        elif word[level] in tree:
            if self.delete(word, level + 1, tree) and len(tree) == 1:
                del tree[word[level]]
                return True
            return False

    def __getitem__(self, word):
        "Find a word in the tree"
        temp = self.tree
        for o in (ord(c) for c in word):
            temp = temp.get(o, {})
            if temp == {}:
                break
        return UCTree.end in temp

# MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
if __name__ == "__main__":
    """
    Running this file as a program executes the tests.
    """

    pf = [ '[PASS] %s: %s', '[FAIL] %s: %s']
    data = {
        'bwords': [ 'bye', 'bitterling', 'beneficially' ],
        'hwords': [ 'hello', 'hi', 'hola', 'hold', 'hole', 'holy' ],
        '_words': [ '愚', '公', '移', '山' ]
    }

    def toPass(uctree, words, msg):
        result = ( data[words] == [uctree[w] for w in data[words]] )
        print pf[result] % (words, msg)

    def toFail(uctree, words, msg):
        result = (     [     ] == [uctree[w] for w in data[words]] )
        print pf[result] % (words, msg)

    def test():
        # Note, we add all but the bwords
        uctree = UCTree(data['hwords'])(data['_words'])

        toPass(uctree, 'hwords', '    in uctree ASCII characters after adding')
        toPass(uctree, '_words', '    in uctree CJK   characters after adding')

        toFail(uctree, 'bwords', 'not in uctree before adding')
        uctree(data['bwords'])
        toPass(uctree, 'bwords', '    in uctree after  adding')
        for word in data['bwords']:
            uctree(word, "delete")
        toFail(uctree, 'bwords', 'not in uctree after  deleting')
        for word in data['hwords']:
            uctree.delete(word)
        toFail(uctree, 'hwords', 'not in uctree after  deleting')
        toPass(uctree, '_words', '    in uctree CJK   characters after bh del')

    test()
