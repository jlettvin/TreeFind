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

    For canonicalization of word variants, the terminal is a set such that
    common tree variations for dissimilar words can have multiple results.
    """

    end = 0xFFFF  # 0xFFFF is a non-character so it is usable as the end key.

    #@staticmethod
    #def variations(word):
        #return []

    def __init__(self, wordlist=[], **kw):
        self.tree = {}
        self(wordlist)

    def add(self, word, variation=None):
        (size, temp) = (len(word), self.tree)
        if not variation:
            variation = word
        for o in (ord(c) for c in variation):
            temp[o] = temp.get(o, {})
            temp = temp[o]
        if not temp.get(UCTree.end):
            temp[UCTree.end] = set([word])
        else:
            temp[UCTree.end].add(word)
        return self

    def __call__(self, word, *args):
        "Add or delete a word or list of words to the tree"
        if type(word) == type([]):
            map(self, word)
        else:
            if "delete" in args:
                self.delete(word)
            else:
                self.add(word)
                # TODO: variations mechanism dpesn't work yet.
                #for variant in UCTree.variations(word):
                    #self.add(word, variant)
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
        return temp.get(UCTree.end, False)

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

        UCTree.variations = variations
        variants = variations('quick')
        uctree.add('quick')
        for variant in variants:
            uctree.add('quick', variant)
        for variant in variants:
            toPass(uctree, 'qwords', '(%s is a variant of %s)' % (
                variant, list(uctree[variant])[0]
            ))

    test()
