import copyright
import os
import re
import string

c = 'c h cpp hpp cxx c++'.split()
java = 'java javascript js'.split()
py = ['py']
sh = 'bash csh ksh pl sh tcsh zsh'.split()
sql = 'sql psql tsql'.split()
xml = 'htm html php xml'.split()
ignore = 'txt bin'.split()
makefile = 'mk'.split()

extensions = {
    'c': c,
    'java': java,
    'js': java,
    'py': py,
    'sh': sh,
    'sql': sql,
    'xml': xml,
    'ignore': ignore,
    'makefile': makefile
}

class Comments:
    @staticmethod
    def comment(text, start=None, stop=None, single=None, pad=0):
        '''Return multiline string wrapped with single or block comment.'''
        lines = text.splitlines(1)
        margin = ' '*pad
        if single:
            result = ''.join([single + margin + line for line in lines])
        else:
            body = ''.join([margin + line for line in lines])
            result = ('{0}\n{1}\n{2}').format(start, body, stop)
        return result

    @staticmethod
    def escape(pattern):
        '''Escape chars to use as regex search pattern.'''
        return pattern.replace('*', '\*').replace('-', '\-')

    @staticmethod
    def find(file=None, text=None, start='', stop='', single=None, n=1):
        '''Return n spans for all comments found.'''
        if file:
            with open(file, 'r') as f:
                text = f.read()

        matches = []
        if single:
            pat = '({t}.*$)([\r\n][ \t]*{t}.*$)*'.format(t=single)
            it = re.compile(pat, re.MULTILINE).finditer(text)
            nfound = 0
            for match in it:
                matches.append(match.span())
                nfound += 1
                if nfound >= n:
                    break

        if start and stop:
            start = Comments.escape(start)
            stop = Comments.escape(stop)
            pat = '^\s*{a}(.|[\r\n])*?{b}'.format(a=start, b=stop)
            it = re.compile(pat, re.MULTILINE).finditer(text)
            nfound = 0
            for match in it:
                matches.append(match.span())
                nfound += 1
                if nfound >= n:
                    break

        matches.sort()
        return matches[:n]

    @staticmethod
    def findCopyright(file=None, text=None, start='', stop='', single=None):
        spans = Comments.find(file=file, text=text, start=start, stop=stop,
                              single=single, n=100000)
        if file:
            with open(file, 'r') as f:
                text = f.read()
        result = []
        for span in spans:
            if text[span[0]:span[1]].lower().count('copyright'):
                result.append(span)
            elif text[span[0]:span[1]].lower().count('license'):
                result.append(span)
        return result

    @staticmethod
    def header(file=None, text=None, start='', stop='', single=None):
        '''Return end index of opening comment block, else -1.'''
        spans = Comments.find(file=file, text=text, start=start, stop=stop,
                              single=single, n=1)
        if spans and 0 == spans[0][0]:
            return spans[0][1]
        else:
            return -1

class Lang(object):
    def __init__(self, lang, exts, start=None, stop=None, single=None, keywords=[]):
        self.lang = lang
        self.exts = exts
        self.kws = keywords
        self.start = start
        self.stop = stop
        self.single = single

    def comment(self, text, single=False, pad=0):
        '''Return single or block style commented multi-line string.'''
        if single or not self.hasblock():
            single = self.single
        return Comments.comment(text, start=self.start,
                                stop=self.stop, single=single, pad=pad)

    def haskeyword(self, filename):
        '''Return True if can detect from content if uses this lang.'''
        if not filename or not os.path.exists(filename):
            return False

        regexs = [re.compile(k) for k in self.kws]
        with open(filename, 'r') as f:
            for line in f:
                for regex in regexs:
                    if regex.match(line):
                        return True
        return False

    def hasblock(self):
        return self.start != None

    def hasext(self, file):
        '''Return True if filename has extension for this language.'''
        if not file:
            return False

        ext = os.path.splitext(file)[-1].lower()
        strip = ext[1:]
        result = strip in self.exts
        return result

    def header(self, file=None, text=None):
        '''Return offset after opening comment block, if any.'''
        return Comments.header(file=file, text=text, start=self.start,
                               stop=self.stop, single=self.single)

    def isa(self, filename):
        '''Return True if file belongs to lang family.'''
        ext = self.hasext(filename)
        kw = self.haskeyword(filename)
        return ext and kw

    def strip(self, file=None, text=None, newlines=0):
        spans = Comments.findCopyright(file=file, text=text, start=self.start,
                                       stop=self.stop, single=self.single)
        if not text:
            with open(file, 'r') as f:
                text = f.read()

        if not spans:
            return [text]

        result = []
        i,j = 0,0
        for span in spans:
            j = span[0]
            if len(text) <= span[1]+1:
                for l in range(newlines):
                    if j >= 2:
                        if text[j-2:j] == '\r\n' or text[j-2:j] == '\n\r':
                            j -= 2
                    elif j >= 1:
                        if text[j-1:j] == '\n':
                            j -= 1
            sub = text[i:j]
            result.append(sub)
            i = span[1]+1
            if len(text) > i:
                for l in range(newlines):
                    if len(text) - i >= 2:
                        if text[i:i+2] == '\r\n' or text[i:i+2] == '\n\r':
                            i += 2
                            continue
                    else:
                        break
                    if len(text) - i >= 1:
                        if text[i:i+1] == '\n':
                            i += 1
                    else:
                        break

        j = len(text)
        rem = text[i:j]
        result.append(rem)

        return [''.join(result), text, spans]


class CLang(Lang):
    def __init__(self):
        super(CLang, self).__init__('c', extensions['c'], '/*', '*/', '//',
                                    keywords=['#if', '#include', '#pragma', '//', '/\*'])

class JavaLang(Lang):
    def __init__(self):
        super(JavaLang, self).__init__('java', extensions['java'], '/*', '*/', '//',
                                       keywords=['^import.*;$', '^package.*;$'])

class PyLang(Lang):
    def __init__(self):
        super(PyLang, self).__init__('py', ['py'],
            start="'''", stop="'''", single='#',
            keywords=['#!.*python.*', '^from ', '^import .*[^;]$', "^''' ", '^""" '])

class ShLang(Lang):
    def __init__(self):
        super(ShLang, self).__init__('sh', extensions['sh'], single='#',
            keywords=['#!.*sh.*', '#!.*perl.*', '^echo ', '^export ', '^set ', '^source ', '^# '])

    def haskeyword(self, filename):
        return True

class SqlLang(Lang):
    def __init__(self):
        super(SqlLang, self).__init__('sql', extensions['sql'], single='--',
            keywords=['^\-\-'])

class XmlLang(Lang):
    def __init__(self):
        keywords = ['<!\-\-', '<!DOCTYPE',  '<html', '<script', '^\s*<\?xml', 'body {', 'p {', 'h1 {']
        super(XmlLang, self).__init__('xml', extensions['xml'],
                start='<!--', stop='-->', keywords=keywords)

class Ignore(Lang):
    def __init__(self):
        super(Ignore, self).__init__('ignore', extensions['ignore'])

    def haskeyword(self, filename):
        return True

class Makefile(Lang):
    def __init__(self):
        keywords = ['^\.PHONY\s*:', '^all\s*:\s*$', '^clean\s*:\s*$', '^TARGET\s*:', '^CFLAGS']
        super(Makefile, self).__init__('makefile', extensions['makefile'], single='#',
            keywords=keywords)

    def hasext(self, file):
        return Lang.hasext(self, file) or Lang.haskeyword(self, file)

    def haskeyword(self, file):
        return Lang.hasext(self, file) or Lang.haskeyword(self, file)

def langs():
    return dict(
        c=CLang(),
        java=JavaLang(),
        py=PyLang(),
        sh=ShLang(),
        sql=SqlLang(),
        xml=XmlLang(),
        ignore=Ignore(),
        make=Makefile())

class Detector:
    langs = langs()
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    null_trans = string.maketrans("", "")

    @staticmethod
    def istext(filename):
        if not filename or not os.path.exists(filename):
            return False

        with open(filename, 'r') as f:
            s = f.read(512)

            # Empty files are considered text
            if not s:
                return True

            # Get the non-text characters (maps a character to itself then
            # use the 'remove' option to get rid of the text characters.)
            t = s.translate(Detector.null_trans, Detector.text_characters)

            # If more than 30% non-text characters, then
            # this is considered a binary file
            if float(len(t)) / float(len(s)) > 0.30:
                return False
            return True

    @staticmethod
    def detect(filename):
        '''Return None or lang family name.'''
        if not Detector.istext(filename):
            return 'bin'
        names = list(Detector.langs.keys())
        names.sort()
        for name in names:
            if Detector.langs[name].isa(filename):
                return name
        return None

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