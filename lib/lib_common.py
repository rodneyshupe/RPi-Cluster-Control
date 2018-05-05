#!/usr/bin/env python
""" Module of common functions used across several other modules and services. """

def str_join(*args):
    """ Join strings together. Returns a string """
    return ''.join(map(str, args))

def isnumeric(test):
    """ Sets is string is numeric. Returns a boolean """
    import re
    return re.match(
        re.compile(r"^[\-]?(([1-9][0-9]*)|[0-9]|[0-9]\.([0-9]+)|(([1-9]?[0-9]*)\.([0-9]+)))$"),
        str(test)
    )
