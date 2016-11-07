# -*- coding: utf8 -*-

"""UniDoc.py
This function enables the calling function to retrieve its own __doc__ string.
"""

__module__     = "UniDoc.py"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = [ "Jonathan D. Lettvin" ]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161107"

import inspect

def UniDoc(msg = ""):
    more = " (%s)" % (msg) if msg else ""
    frame = inspect.currentframe().f_back
    for objref in frame.f_globals.values():
        if inspect.isfunction(objref):
            if objref.func_code == frame.f_code:
                return objref.__doc__ + more
        elif inspect.isclass(objref):
            for name, member in inspect.getmembers(objref):
                if inspect.ismethod(member):
                    if member.im_func.func_code == frame.f_code:
                        return member.__doc__ + more
