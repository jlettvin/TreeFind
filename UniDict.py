#!/usr/bin/env python
# -*- coding: utf8 -*-

from pprint import pprint
from ujson  import dumps

class UniDict(dict):

    @staticmethod
    def escape(string):
        string = string.replace("'", "\\'")
        return string

    def __init__(self, **kw):
        self.__dict__ = self
        self(**kw)

    def __call__(self, **kw):
        self.update({
            filter(str.isalpha, k): UniDict.escape(w)
            for k, w in kw.iteritems()
        })

    def javascript(self, var):
        string  = "var %s = {\n    " % (var)
        string += ",\n    ".join([
            "%s => '%s'" % (k, w)
            for k, w in self.iteritems()])
        string += "\n};"
        return string

if __name__ == "__main__":

    sample = {
        " Strip.This*Token": "But: Leave+This$Alone",
        "12BuckleMyShoe34TryItSomeMore": "Does'nt this work?"
    }
    unidict = UniDict(**sample)

    print '-'*78
    print unidict.javascript("sample")
    print '-'*78
    print unidict.StripThisToken
    print '-'*78
