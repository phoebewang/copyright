import copyright
import sys
from colorama import init, Fore

class App(object):
    '''
    Interface for running app programmatically.
    '''

    def __init__(self):
        self.cli = copyright.Cli()
        self.config = copyright.Config()
        self.result = dict(unknown = [], binary = [])

    @staticmethod
    def main(argv):
        app = App()
        result = app.cli.parse(argv)
        if not result:
            return 'Failed to parse commandline.'

        return app.run()

    def detect(self, file):
        langtype = self.config.lang or copyright.Detector.detect(file)
        if not langtype:
            self.result['unknown'].append(['ndetect', file])
            if self.config.debug:
                msg = 'Skipping unknown language: {0}\n'.format(file)
                sys.stdout.write(msg)
            return
        elif langtype == "bin" or langtype == "ignore":
            self.result['binary'].append(['nneed', file])
            if self.config.debug:
                msg = 'binary: {0}\n'.format(file)
                sys.stdout.write(msg)
            return

        lang = self.langs[langtype]
        strip = lang.strip(file)
        if len(strip) < 3:
            self.result.setdefault(langtype, [])
            self.result[langtype].append(['none', file])
            if self.config.debug:
                msg = 'none: {0}\n'.format(file)
                sys.stdout.write(msg)
            return
        if len(strip[2]) > 1:
            self.result.setdefault(langtype, [])
            self.result[langtype].append(['more', file])
            if self.config.debug:
                msg = 'more: {0}\n'.format(file)
                sys.stdout.write(msg)
            return
        text = strip[1][strip[2][0][0]:strip[2][0][1]]
        text = unicode(text, errors='ignore')
        if self.config.debug:
            msg = '%s\n: %s\n' % (file, text)
            sys.stdout.write(msg)
        self.result.setdefault(langtype, [])
        self.result[langtype].append([self.dist.license(text), file])
        if self.config.debug:
            msg = '%s: %s\n' % (langtype, file)
            sys.stdout.write(msg)

    def process(self, file, langtype, clear = False):
        text = copyright.License(self.config).text
        lang = self.langs[langtype]
        if clear:
            commented = ''
        else:
            commented = lang.comment(text,
                                     single=self.config.single,
                                     pad=self.config.pad)
        copyright.license.LicensedFile(file,
                                       lang,
                                       commented).write(back=self.config.back,
                                                        newlines=self.config.newlines)

    def run(self):
        self.config.load(self.cli)
        if self.config.debug:
            copyright.logger.debug("config=" + repr(self.config))

        self.dist = copyright.Dist(self.config.dict['templates'])

        self.langs = copyright.langs()
        walks = copyright.walks(self.config.files,
                                exclude=self.config.exclude,
                                include=self.config.include,
                                regex=self.config.regex,
                                recurse = not self.config.no_recurse,
                                debug=self.config.debug)
        for walk in walks:
            for file in walk:
                if self.config.debug:
                    copyright.logger.debug("file=" + file)
                self.detect(file)
        for key, value in self.result.items():
            print '************************** %s **************************' % key
            for f in value:
                print f
            print
        print '************************** result[lang] **************************'
        for key, value in self.result.items():
            if key in ['unknown', 'ignore']:
                print Fore.YELLOW + '%s\t%d' %(key, len(value)) + Fore.WHITE
            else:
                print '%s\t%d' %(key, len(value))
        print '\n************************** result[license] **************************'
        lic_result = dict()
        for key, value in self.result.items():
            for f in value:
                lic_result.setdefault(f[0], [])
                lic_result[f[0]].append([key, f[1]])
        cannot_write = False
        for key, value in lic_result.items():
            if key in ['unknown', 'gpl3', 'gpl2', 'gpl', 'agpl3', 'lgpl3', 'lgpl2.1', 'lgpl2']:
                cannot_write = True
                print Fore.RED + '%s\t%d' %(key, len(value)) + Fore.WHITE
            elif key in ['ndetect', 'apache2', 'apache1.1', 'apache1', 'mozilla1.1', 'mozilla2A', 'mozilla2B']:
                print Fore.YELLOW + '%s\t%d' %(key, len(value)) + Fore.WHITE
            elif key == 'none':
                print Fore.GREEN + '%s\t%d' %(key, len(value)) + Fore.WHITE
            else:
                print '%s\t%d' %(key, len(value))
        print

        if not (self.config.add or self.config.update or self.config.clr):
            return 0

        if cannot_write:
            print Fore.RED + 'There are incompatible licenses in your floder'
            print 'Please make sure the licenses are right or add the folder to exclude.' + Fore.WHITE
            return 0
        clr = False
        if self.config.add:
            lic = 'none'
        if self.config.update:
            lic = self.config.update
        if self.config.clr:
            clr = True
            lic = self.config.clr
        if lic in copyright.template.Template.DEFAULT.keys():
            print Fore.RED + 'Default licenses cannot be clear or update' + Fore.WHITE
            return 0
        if None == lic_result.get(lic):
            print 'Cannot find %s licensed file' % lic
            return 0
        lang_none = dict()
        for i in lic_result[lic]:
            lang_none.setdefault(i[0], 0)
            lang_none[i[0]] += 1
        print '************************** Will write **************************'
        for key, value in lang_none.items():
            print '%s\t%d' %(key, value)
        content = raw_input("\nAre those file correct Yes/No: ")
        if 'Yes' != content:
            print '\nUser cancled'
            return 0
        for file in lic_result[lic]:
            self.process(file[1], file[0], clr)
        print '\nFinish!'
        return 0

def main():
    '''Run from commandline.'''
    init()
    sys.exit(App.main(sys.argv[1:]))

if '__main__' == __name__: main()

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
