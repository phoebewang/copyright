import os

class License:
    def __init__(self, config):
        temp = config.dict.get('templates')[config.license]
        self.text = temp.format(author=config.author,
                                short=config.short,
                                program=config.program,
                                year=config.year)

class LicensedFile:
    def __init__(self, file, lang, lic):
        self.file = file
        self.lang = lang
        self.lic = lic

    def write(self, back=False, newlines=1):
        '''Write text to file.'''
        if not self.file or not self.lic or not os.path.exists(self.file):
            return

        text = self.lang.strip(file=self.file)
        sep = os.linesep * newlines
        if back:
            text = text.rstrip('\r\n') + sep + self.lic
        else:
            i = self.lang.header(text=text)
            if -1 == i:
                head = ''
                tail = sep + text.lstrip('\r\n')
            else:
                head = text[:i+1].rstrip('\r\n') + sep
                tail = sep + text[i:].lstrip('\r\n')

            text = ''.join([head, self.lic, tail])

        with open(self.file, 'w') as f:
            f.write(text)

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