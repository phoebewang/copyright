import re
import os

RE_CHARS = r'[\w~=+,.\-/\\]'

def wildcardToRegex(old):
    '''Replace '*' and '?' with proper regex rules.'''
    result = old.replace('*', RE_CHARS+'*').replace('?', RE_CHARS).replace('.', '\.')
    if len(result) != len(old):
         result += '$'
    return result

class Countdown:
    def __init__(self, infinite=True):
        self.i = 1e30 if infinite else 1

    def dec(self):
        prev = self.i
        if self.i > 0:
            self.i -= 1
        return prev

class Walk(object):
    '''Recursively walk a directory tree and filter files by name.'''
    def __init__(self, path='', exclude=None, include=None, regex=False,
                 recurse=True, debug=False):
        '''
        Args
        ----
        exclude: (optional) list of file name patterns to skip
        include: (optional) list of file name patterns to process
        path: Top directory to start traversal. If none, use current.
        regex: If exclude/include lists use regex syntax.
        '''
        self.debug = debug

        if os.path.isfile(path):
            self.files = [path]
            self.root = ''
        else:
            self.files = []
            self.root = []
            if not path:
                path = os.path.curdir
        self.walk = os.walk(path)

        if exclude:
            if not regex:
                exclude = [wildcardToRegex(s) for s in exclude]
            self.exclude = [re.compile(s) for s in exclude]
        else:
            self.exclude = []

        if include:
            if not regex:
                include = [wildcardToRegex(s) for s in include]
            self.include = [re.compile(s) for s in include]
        else:
            self.include = []

        self.ctr = Countdown(recurse)

    def __next__(self):
        return self.next()

    def __str__(self):
        return 'root={0} files={1}'.format(self.root, self.files)

    def __iter__(self):
        return self

    def _search(self):
        if self.files:
            while self.files:
                f = self.files.pop()
                name = os.path.join(self.root, f)
                if self.isvalid(name):
                    return name
        return None

    def isvalid(self, file):
        from copyright import logger

        if not os.path.exists(file):
            return False

        for regex in self.exclude:
            match = regex.search(file)
            if match:
                return False

        if self.include:
            for regex in self.include:
                match = regex.search(file)
                if self.debug:
                    msg = 'regex={0} file={1} match={2}'
                    logger.debug(msg.format(regex.pattern, file, match is not None))
                if match:
                    return True
            return False

        return True

    def next(self):
        # Return a filtered filename or throw if no more next.
        filename = self._search()
        while not filename:
            if not self.ctr.dec():
                raise StopIteration

            self.root, _, self.files = next(self.walk)
            filename = self._search()

        return filename

def walks(paths, exclude=None, include=None, regex=None, recurse=True, debug=False):
    '''Return list of walkers.'''
    if type(paths) is str:
        paths = [paths]

    result = [Walk(p, exclude=exclude, include=include, regex=regex,
                   recurse=recurse, debug=debug)
              for p in paths]
    return result

def demo():
    for f in Walk(): print(f)

    exclude = ['*.py', 'd1', '.d4']
    print('\nexclude=', exclude)
    for f in Walk(exclude=exclude): print(f)

    include = ['_*.py', 'd1']
    print('\ninclude=', include)
    for f in Walk(include=include): print(f)

    include = ['f[\d]$']
    print('\nregex include=', include)
    for f in Walk(include=include, regex=True): print(f)

    include = ['f[\d]$']
    print('\npath regex include=', include)
    for f in Walk(path='./d1', include=include, regex=True): print(f)

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