import argparse
import sys

from pprint import pprint

class Cli:
    def __init__(self):
        self.args = None
        self.parser = self.createParser()

    def createParser(self):
        # Avoids python3 import hell.
        import copyright

        desc = '''Add or update license/copyright boilerplate in files.
version: {0}'''.format(copyright.version.__version__)

        epilog = '''examples:

# Process all known file types from this path.
copyright -l gpl3 -a "Alice Doe, Joe Smith" -s "My cool app." -p CoolApp

# Use options file.
copyright -c options.json

# Process specific files.
copyright -c options.json file1 dir2/*
        '''
        parser = argparse.ArgumentParser(
            add_help=True,
            description=desc,
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument(
            '-a', '--author',
            help='''Author name(s) to be injected into template. Defaults to username.''')
        parser.add_argument(
            '-b', '--back',
            action="store_true",
            help='''Put license at the end of file. Default is front.''')
        parser.add_argument(
            '-c', '--config',
            help='''Load settings from this JSON file.''')
        parser.add_argument(
            '-d', '--debug',
            action="store_true",
            help='Print debug messages.')
        parser.add_argument(
            '-e', '--exclude',
            help='''Comma delimited list of name patterns to exclude.''')
        parser.add_argument(
            '-i', '--include',
            help='''Comma delimited list of name patterns to include.''')
        parser.add_argument(
            '-L', '--lang',
            choices=sorted(copyright.lang.extensions.keys()),
            help='''Force language comment style on files.''')
        parser.add_argument(
            '-n', '--newlines', type=int, default=2,
            help='Number of newlines before/after injected message.')
        parser.add_argument(
            '-l', '--license',
            action='append',
            choices=sorted(copyright.template.Template.DEFAULT.keys()),
            help='''License.''')
        parser.add_argument(
            '-R', '--no-recurse',
            action="store_true",
            help='Do not recurse into subdirectories.')
        parser.add_argument(
            '-P', '--pad', type=int, default=4,
            help='Number of spaces to left-pad each line in license.')
        parser.add_argument(
            '-p', '--program',
            help='Program name to substitute into templates.')
        parser.add_argument(
            '-q', '--quiet',
            action="store_true",
            help='Do not print files processed.')
        parser.add_argument(
            '-r', '--regex',
            action="store_true",
            help='Include and exclude patterns use regex syntax.')
        parser.add_argument(
            '-s', '--short',
            help='''Short description to inject into templates.''')
        parser.add_argument(
            '-S', '--single',
            action="store_true",
            help='''Use single-line comment style if supported.''')
        parser.add_argument(
            '-t', '--templates',
            help='Extend templates with this JSON file.')
        parser.add_argument(
            '-v', '--version',
            action='version',
            version='copyright ' + copyright.version.__version__)
        parser.add_argument(
            '-y', '--year',
            help='''Year(s) to be injected into template. Defaults to current.''')

        parser.add_argument('files', help='List of files to process.')

        return parser

    def parse(self, argv):
        from copyright import logger

        self.args = self.parser.parse_args(argv)

        if self.args.include:
            self.args.include = self.args.include.split(',')
        if self.args.exclude:
            self.args.exclude = self.args.exclude.split(',')

        if self.args.debug:
            logger.debug('argv={0}'.format(argv))
            logger.debug('args={0}'.format(self.args))

        return self.args

def demo():
    c = Cli()
    import sys
    print(c.parse(sys.argv[1:]))

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