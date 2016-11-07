#!/usr/bin/env python
# -*- coding: utf8 -*-

"""UniArray.py
This class imitates numpy/scipy ndarray without requiring them.
It implements an ndarray constructor and element/subset get/set.

Justification: UniDigit uses a multidimensional array.
This class will be used to manage that array.
"""

from ujson  import dumps

class UniArray(dict):

    @staticmethod
    def ndlist(s, v):
        return [UniArray.ndlist(s[1:], v) for i in xrange(s[0])] if s else v

    def __init__(self, *arg):
        self.__dict__ = self
        self.reuireTuple = 'shape tuple of positive ints required'
        assert len(arg) > 0, self.requireTuple
        assert isinstance(arg[0], tuple), self.requireTuple
        self.shape = arg[0]
        assert all([d>0 for d in self.shape]), self.requireTuple
        self.size = reduce(lambda x, y: x * y, self.shape)
        value = 0 if len(arg) < 2 else arg[1]
        data = [value] * self.size
        dims = [d for d in self.shape]
        dims.reverse()
        self.data = UniArray.ndlist(self.shape, value)

    def __call__(self, **kw):
        """
        Thia functor substitutes contents of an instance.
        """
        keys  = ('shape', 'data', 'size')
        shape = kw.get('shape', False)
        data  = kw.get('data' , False)
        size  = kw.get('size' , False)
        assert shape and data and size, 'incompatible update'
        assert all([d>0 for d in shape]), self.requireTuple
        temp = data
        total = 1
        for d in shape[:-1]:
            total *= d
            assert len(temp) == d
            uniq = set([(len(item), type(item)) for item in temp])
            temp = temp[0]
            assert len(uniq) == 1, 'all items must be of the same size/type'
        self.update({k:v for k,v in kw.iteritems() if k in keys})

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
    shape = (2,2)
    size  = 4
    data  = [[0,1], [2,3]]
    uniarray(shape=shape, size=size, data=data)
    print uniarray[1,1]
