#!/usr/bin/env python

# =======================================
#
# Common functions used accross modules
# and services.
#
# =======================================

# Join strings together
# Returns a string
def str_join(*args):
    return ''.join(map(str, args))

# Sets is string is numeric
# Returns a boolean
def isnumeric(test):
    import re
    #return(re.match(re.compile("^[\-]?[0-9][0-9]*\.?[0-9]+$"), str(test)))
    return(re.match(re.compile("^[\-]?(([1-9][0-9]*)|[0-9]|[0-9]\.([0-9]+)|(([1-9]?[0-9]*)\.([0-9]+)))$"), str(test)))
