__author__ = 'Excelle'

'''
    Advanced Dict object that supports attributive access.
    Like this:
    a = Dict()
    a.attr = value  # Assignment
    val = a.attr    # Retrieve
'''


class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for key, value in zip(names, values):
            self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError("'Dict' object has no attribute %s" % item)

    def __setattr__(self, key, value):
        self[key] = value