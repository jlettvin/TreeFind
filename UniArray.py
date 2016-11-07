#!/usr/bin/env python
# -*- coding: utf8 -*-

from pprint import pprint
from ujson  import dumps

class UniArray(dict):

    @staticmethod
    def ndlist(s, v):
        return [UniArray.ndlist(s[1:], v) for i in xrange(s[0])] if s else v

    def __init__(self, *arg):
        self.__dict__ = self
        reuireTuple = 'shape tuple of positive ints required'
        assert len(arg) > 0, requireTuple
        assert isinstance(arg[0], tuple), requireTuple
        self.shape = arg[0]
        assert all([d>0 for d in self.shape]), self.requireTuple
        self.size = reduce(lambda x, y: x * y, self.shape)
        value = 0 if len(arg) < 2 else arg[1]
        data = [value] * self.size
        dims = [d for d in self.shape]
        dims.reverse()
        self.data = UniArray.ndlist(self.shape, value)

    def _offset(self, *index):
        reuireTuple = 'shape tuple of positive ints required'
        assert isinstance(index, tuple), requireTuple
        index = index[0]
        assert len(index) == len(self.shape), 'index tuple wrong length'
        bounds = zip(index, self.shape)
        assert all([n >= 0 and n < d for n,d in bounds]), 'index out of bounds'
        return sum([a*b for a,b in bounds])

    def __getitem__(self, *index):
        temp = self.data
        for d in index[0]:
            temp = temp[d]
        return temp

    def _set(self, d, t, v):
        print v, t, d
        if len(t) == 1:
            d[t[0]] = v
        else:
            self._set(d[t[0]], t[1:], v)

    def __setitem__(self, *index):
        value = index[1]
        self._set(self.data, index[0], index[1])

    def _stack(self):
        result = [n for n in self.data]
        dims = [d for d in self.shape]
        dims.reverse()
        for d in dims:
            result = [result[n:n+d] for n in range(0, len(result), d)]
        return result

    def javascript(self, var):
        string  = "var %s = " % (var)
        string += dumps(self.data)
        string += ";"
        return string

if __name__ == "__main__":

    shape = (5,3,2)
    uniarray = UniArray(shape, -1)
    uniarray[0,0,0] = 0
    uniarray[4,2,1] = 9
    uniarray[3,2] = [5,6]
    print uniarray[0,0,0]
    print uniarray[4,2,1]
    print uniarray
    print uniarray.javascript('fun')
