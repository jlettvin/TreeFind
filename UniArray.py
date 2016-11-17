#!/usr/bin/env python
# -*- coding: utf8 -*-
#: PEP8 -E221
# pep8: disable=E221

"""UniArray.py
This class imitates numpy/scipy ndarray without requiring them.
It implements an ndarray constructor and element/subset get/set.

Justification: UniDigit uses a multidimensional array.
This class will be used to manage that array.
"""

__module__     = "UniArray.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = ["Jonathan D. Lettvin"]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161107"

from json import (dumps)


class UniArray(dict):
    "Emulate numpy ndarray without requiring numpy"

    requireTuple = "positive int tuple required"

    @staticmethod
    def _ndlist(shape, value):
        "Recursive assembly of UniArray"
        return [
            UniArray._ndlist(shape[1:], value)
            for _ in xrange(shape[0])] if shape else value

    def __init__(self, *arg):
        "Store shape.  Generate instance values."
        super(UniArray, self).__init__()
        self.__dict__ = self
        assert len(arg) > 0, UniArray.requireTuple
        assert isinstance(arg[0], tuple), UniArray.requireTuple
        self.shape = arg[0]
        assert all([d > 0 for d in self.shape]), UniArray.requireTuple
        self.size = reduce(lambda x, y: x * y, self.shape)
        value = 0 if len(arg) < 2 else arg[1]
        self.data = UniArray._ndlist(self.shape, value)

    def __call__(self, **kw):
        """
        Thia functor substitutes contents of an instance.
        """
        keys  = ('shape', 'data', 'size')
        shape = kw.get('shape', False)
        data  = kw.get('data' , False)
        size  = kw.get('size' , False)
        want = reduce(lambda x, y: x * y, shape)
        assert shape and data and size, 'functor: incompatible update'
        assert all([d > 0 for d in shape]), UniArray.requireTuple
        assert want == size, 'functor: size mismatch'
        temp = data
        total = 1
        for datum in shape[:-1]:
            total *= datum
            assert len(temp) == datum
            uniq = set([(len(item), type(item)) for item in temp])
            temp = temp[0]
            assert len(uniq) == 1, 'all items must be of the same size/type'
        self.update({k: v for k, v in kw.iteritems() if k in keys})

    def __getitem__(self, *index):
        temp = self.data
        for datum in index[0]:
            temp = temp[datum]
        return temp

    def _set(self, data, value, shape):
        """
        Replace existing structure with new structure.
        #if not isinstance(t, tuple):
            #t = (t)
        #if not isinstance(t, list):
            #d[t[0]] = v
        TODO fix error when replacing top level structure.
        """
        print data, value, shape
        if len(shape) == 1:
            data[shape[0]] = value
        else:
            self._set(data[shape[0]], value, shape[1:])

    def __setitem__(self, *index):
        self._set(self.data, index[1], index[0])

    def javascript(self, var):
        "Generate the array as a string in javascript format."
        string  = "var %s = " % (var)
        string += dumps(self.data)
        string += ";"
        return string


if __name__ == "__main__":

    UNIARRAY = UniArray((5, 3, 2), -1)
    UNIARRAY[0, 0, 0] = 0
    UNIARRAY[4, 2, 1] = 9
    UNIARRAY[3, 2] = [5, 6]
    print UNIARRAY[0, 0, 0]
    print UNIARRAY[4, 2, 1]
    print UNIARRAY
    print UNIARRAY.javascript('fun')
    UNIARRAY(shape=(2, 2), size=4, data=[[0, 1], [2, 3]])
    print UNIARRAY[1, 1]
