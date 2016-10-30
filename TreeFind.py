#!/usr/bin/env python
# -*- coding: utf8 -*-

"""TreeFind.py

Usage:
    TreeFind.py [-inrst] [-w WORDS] [-v] [FILE...]
    TreeFind.py (-h | --help)
    TreeFind.py (--version)

Options:
    -i --ignorecase                 Caseless comparison
    -n --noJSON                     Use ingest words without backstore
    -r --renewJSON                  Generate new JSON backstore
    -s --showtree                   Show args and tree using pretty print
    -t --test                       Run tests
    -v --verbose                    Show verbose output
    -w WORDS --words=WORDS          Source [default: /usr/share/dict/words]
    -h --help                       Show this Usage message
    --version                       Show version

Concepts:
    Searching for established words is improved by creating
    a dictionary tree from which individual character can be
    tested until a special token is found meaning terminal ('$').
    This application reads from the standard unix word source
    /usr/share/dict/words
    from which it constructs the dictionary and then stores it
    as a .json file which is faster to dump and load than cPickle.

Unit tests include:
    1. reporting non-matches from the ASCII in this python script.
       NOTE: some acceptable English words are not in the words dictionary.
    2. reporting no output when searching the words dictionary.

Examples:
    ./TreeFind.py -w testwords -i -n -s TreeFind.py  # local only, show tree

    Given a file 'testwords' with the following contents:
hello
hi
hola
hold
hole
work
world

    the output would finish with:
{'arg': {'FILE': ['TreeFind.py'],
         'haveJSON': True,
         'help': False,
         'ignorecase': True,
         'noJSON': True,
         'renewJSON': False,
         'showtree': True,
         'test': False,
         'verbose': False,
         'version': False,
         'words': 'testwords'},
 u'h': {u'e': {u'l': {u'l': {u'o': {'$': u'hello'}}}},
        u'i': {'$': u'hi'},
        u'o': {u'l': {u'a': {'$': u'hola'},
                      u'd': {'$': u'hold'},
                      u'e': {'$': u'hole'}}}},
 u'w': {u'o': {u'r': {u'k': {'$': u'work'}, u'l': {u'd': {'$': u'world'}}}}}}

Author  : Jonathan D. Lettvin (jlettvin@gmail.com)
Date    : 20161029 
Legal   : Copyright(c) Jonathan D. Lettvin, All Rights Reserved
License : GPL 3.0
"""

__module__     = "TreeFind.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = [ "Jonathan D. Lettvin" ]
__license__    = "GPLv3"
__version__    = "0.0.2"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161029"


import os
import re
import sys
import ujson
import codecs
import docopt
import pprint

class Arg(dict):
    """Arg
    This class enables direct use of dictionary elements as class members.
    For example: self["foo"] is identical to self.foo.
    Command-line options typically have '-' characters which are stripped.
    """

    def __init__(self, **kw):
        self.__dict__ = self
        self.update({ k.strip('-'): w for k, w in kw.iteritems() })

class TreeFind(dict):
    """TreeFind
    This class ingests or restores the unix word dictionary into a tree.
    If it ingests, it converts the words file to a searchable tree
    then it saves it in a local file to be restored on the next execution.

    The __call__ functor simply returns True or False to flag dictionary words.
    """

    defaultDictionary = "/usr/share/dict/words"
    dictionary = defaultDictionary

    def verbose(self, msg, nl=1):
        """
        Service function to aid in observing progress during debugging.
        nl is the number of newlines to append.
        """
        if self.arg.verbose:
            print(msg),
            sys.stdout.flush()
            for _ in range(nl):
                print()

    def __init__(self, arg=None):
        """
        Initialization checks for existing file to restore or
        ingests unix word dictionary, generates a tree, and creates this file.
        """
        self.__dict__ = self
        if arg is None:  # docopt args were not offered.
            # This mechanism guarantees presence of all docopt args.
            arg = {}
            with open(sys.argv[0]) as source:
                while True:
                    line = source.readline().strip()
                    if line == '"""':
                        break
                    if line.startswith('    -'):
                        m = re.search('--(\w+)')
                        d = re.search('\[default: ([^\]]*)\s\]')
                        arg[m.group(0)] = d.group(0) if d else False
            arg['words'] = '/usr/share/dict/words'

        arg.haveJSON = os.path.isfile('TreeFind.json')
        self.arg = arg

        if arg.haveJSON and not arg.renewJSON and not arg.noJSON:
            self.verbose('restoring from json backup')
            with open('TreeFind.json', 'rb') as source:
                codecs.UTF8Reader = codecs.getreader('utf8')
                source = codecs.UTF8Reader(source)
                self.update(ujson.load(source))
        else:
            self.verbose('ingesting from %s' % (TreeFind.dictionary))
            with open(TreeFind.dictionary) as source:
                self.verbose('opened')
                codecs.UTF8Reader = codecs.getreader('utf8')
                source = codecs.UTF8Reader(source)
                words = (w.strip() for w in source.readlines())
                self.verbose('loops')
                for word in words:
                    self.verbose("%s%s\r" % (word, ' ' * 50), 0)
                    if arg.ignorecase:
                        word = word.lower()
                    self.ingest(word)
                self.verbose("done")
            self.verbose('saving to json backup')
            if not arg.noJSON:
                with open('TreeFind.json', 'wb') as target:
                    codecs.UTF8Writer = codecs.getreader('utf8')
                    target = codecs.UTF8Writer(target)
                    ujson.dump(self, target)

    def ingest(self, word, tree=None, level=0):
        """
        Service function is usually only to be called by __init__.
        This is the tree generation method.
        It can be called after the fact to add new words to the tree.
        """
        if tree == None:
            tree = self
        if len(word) > level:
            char = word[level]
            tree[char] = tree.get(char, {})
            self.ingest(word, tree[char], level + 1)
        else:
            tree['$'] = word
        return tree

    def __call__(self, word):
        """
        External functor interface to detect word presence.
        """
        temp = self
        if self.arg.ignorecase:
            word = word.lower()
        for i, c in enumerate(list(word)):
            temp = temp.get(c, None)
            if not temp:
                break
        return (temp and {} == temp.get('$', None)) or False

if __name__ == "__main__":

    def test(filename, treefind, doc, arg):
        """
        Test service function.
        Read regex recognized words (including '-') from named file.
        Report words not in the unix dictionary.
        """
        print('+' * 79)
        print(doc)
        print('-' * 79)
        with open(filename) as source:
            codecs.UTF8Reader = codecs.getreader('utf8')
            source = codecs.UTF8Reader(source)
            missing = set()
            for phrase in [w.strip() for w in source.read().split()]:
                for word in re.sub('[^\w\-]+', ' ', phrase).strip().split():
                    if word and not treefind(word):
                        missing.add(word)
            print('\n'.join(sorted(list(missing))))
        if arg.showtree:
            pprint.pprint(treefind)

    def main():
        """
        Entrypoint of this script.
        """
        arg = Arg(**docopt.docopt(__doc__, version=__version__))
        if arg.verbose:
            pprint.pprint(arg)

        if len(sys.argv) == 1:
            print(__doc__)
            exit(0)

        TreeFind.dictionary = arg.words
        if arg.verbose:
            print("using words from: %s" % (TreeFind.dictionary))
        treefind = TreeFind(arg)
        if arg.test:
            test1doc = """
self: %s (should see all non-member words in this python)'
      even some like capitalized and "creating"'
      which are curiously absent from unix words'
""" % (sys.argv[0])
            test(sys.argv[0], treefind, test1doc, arg)
            test2doc = """
words: %s (should see no output)' % (TreeFind.dictionary)
       in other words, an empty line'
"""
            test(TreeFind.dictionary, treefind, test2doc, arg)
        else:
            for filename in arg.FILE:
                print('    filename: %s' % (filename))
                test(filename, treefind, "normal operation", arg)


    main()
