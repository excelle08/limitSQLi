__author__ = 'Excelle'

IGNORED_DBS = ['information_schema', 'performance_schema', 'mysql']


def isIgnorable(name):
    result = False
    for val in IGNORED_DBS:
        if val == name.lower():
            result = False
    return result