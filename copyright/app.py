import copyright
import sys

class App(object):
    '''
    Interface for running app programmatically.
    '''

    def __init__(self):
        self.cli = copyright.Cli()
        self.config = copyright.Config()

    @staticmethod
    def main(argv):
        app = App()
        result = app.cli.parse(argv)
        if not result:
            return 'Failed to parse commandline.'

        return app.run()

    def process(self, file):
        langtype = self.config.lang or copyright.Detector.detect(file)
        if not langtype:
            msg = 'Skipping unknown language: {0}\n'.format(file)
            sys.stdout.write(msg)
            return

        text = copyright.License(self.config).text
        lang = self.langs[langtype]
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
                self.process(file)
        return 0

def main():
    '''Run from commandline.'''
    sys.exit(App.main(sys.argv))

if '__main__' == __name__: main()
