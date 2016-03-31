import datetime
import json
import os

class Config:
    def __init__(self, **kargs):
        self.dict = self.newdict()
        self.dict.update(kargs)

    def __repr__(self):
        return 'Config({0})'.format(repr(self.dict))

    def load(self, cli):
        '''Load from commandline settings file, then cli overrides.'''
        self.loadfile(cli.args.config)
        self.loadargs(cli.args)
        self.__dict__.update(self.dict)

    def loadargs(self, args):
        # Avoids python3 import hell.
        import copyright
        for key in self.dict.keys():
            v = args.__dict__[key]
            if v:
                self.dict[key.replace('-', '_')] = v

        self.dict['templates'] = copyright.template.Template.loadf(self.dict['templates'])

    def loadfile(self, filename):
        if filename:
            with open(filename) as f:
                js = json.load(f)
                if js.get('include', None):
                    js['include'] = str(js['include']).split(',')
                if js.get('exclude', None):
                    js['exclude'] = str(js['exclude']).split(',')

                self.dict.update(js)

    @staticmethod
    def newdict():
        return dict(
            author=os.environ['USER'],
            back=False,
            config=None,
            debug=False,
            exclude=None,
            files=[],
            include=None,
            lang=None,
            license='gpl3',
            newlines=1,
            no_recurse=False,
            pad=4,
            program=None,
            quiet=False,
            regex=False,
            short='',
            single=False,
            templates=None,
            year=datetime.datetime.now().year)

# copyright - Add or replace license boilerplate.
# Copyright (C) 2016 Remik Ziemlinski
#
# copyright is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# copyright is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.