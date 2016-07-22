from prettytable import PrettyTable
from pprint import pprint
from ri_registry.format.plugin import Plugin
import arrow


class Table(Plugin):

    def __repr__(self):
        t = PrettyTable(self.cols)
        for obs in reversed(self.data):
            r = []
            for c in self.cols:
                y = obs.get(c, '')
                if type(y) is list:
                    try:
                        y = ','.join(y)
                    except TypeError:
                        y = len(y)

                # http://stackoverflow.com/questions/3224268/python-unicode-encode-error
                # http://stackoverflow.com/questions/19833440/unicodeencodeerror-ascii-codec-cant-encode-character-u-xe9-in-position-7
                try:
                    if type(y) is unicode:
                        y = y.encode('ascii', 'ignore')
                except NameError:
                    # python3
                    pass

                if y and (c in ['created_at', 'updated_at']):
                    y = arrow.get(y).format('YYYY-MM-DDTHH:mm:ss')
                    y = '{}Z'.format(y)
                else:
                    y = str(y)

                y = (y[:self.max_field_size] + '..') if len(y) > self.max_field_size else y
                r.append(y)
            t.add_row(r)
        return str(t)
