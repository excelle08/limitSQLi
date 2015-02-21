__author__ = 'Excelle'


class Column():
    values = []

    def __init__(self, name, *values):
        self.name = name
        for v in values:
            self.values.append(v)


class Table():
    columns = []

    def __init__(self, database, *kw):
        self.schema = database
        for v in kw:
            self.columns.append(v)


class Database():
    tables = []

    def __init__(self, name, *tables):
        self.name = name
        for v in tables:
            self.tables.append(v)

