import os
import shlex
import shutil
import unittest

from copyright import App, diffdir

DATA_DIR = 'test/data'
INPUT_DIR = os.path.join(DATA_DIR, 'input')
TMP_DIR = os.path.join(DATA_DIR, 'tmp')
TRUTH_DIR = os.path.join(DATA_DIR, 'truth')

def datadir(suffix):
    return os.path.join(DATA_DIR, suffix)

def inputdir(suffix):
    return os.path.join(INPUT_DIR, suffix)

def tmpdir(suffix):
    return os.path.join(TMP_DIR, suffix)

def truthdir(suffix):
    return os.path.join(TRUTH_DIR, suffix)

class TestApp(unittest.TestCase):
    def diff_dir(self, dir1, dir2):
        diffs = diffdir(dir1, dir2)
        self.assertEqual([], diffs, 'Files differ: {0}'.format(diffs))

    def diff_file_dir(self, dir1, dir2, name):
        self.diff_file(os.path.join(dir1, name), os.path.join(dir2, name))

    def diff_file(self, name1, name2):
        with open(name1) as f1:
            with open(name2) as f2:
                lines1, lines2 = f1.readlines(), f2.readlines()
                msg = '{0} and {1} differ.'
                self.assertEqual(lines1, lines2, msg.format(name1, name2))

    def run_test_force_lang(self, lang):
        dir1 = truthdir('force/' + lang)
        dir2 = tmpdir(lang)
        self.setup(dir2)
        temp = '-L {lang} -a Foo -p Bar -P 4 -s App -y 2016 {d}/empty'
        args = temp.format(lang=lang, d=dir2).split()
        App.main(args)
        file = 'empty'
        self.diff_file_dir(dir1, dir2, file)

    def setup(self, dst):
        self.teardown(dst)

        shutil.copytree(INPUT_DIR, dst)

    def teardown(self, dst):
        shutil.rmtree(dst, True)

    def test_back_single(self):
        tree = 'back_single'
        dir1 = truthdir(tree)
        dir2 = tmpdir(tree)
        self.setup(dir2)
        temp = '-a Foo -p Bar -P 1 -s App -y 2016 --back --single {d}'
        args = temp.format(d=dir2).split()
        App.main(args)
        self.diff_dir(dir1, dir2)

    def test_force_lang_c(self):
        self.run_test_force_lang('c')

    def test_force_lang_sh(self):
        self.run_test_force_lang('sh')

    def test_front_block_include(self):
        tree = 'front_block_include'
        dir1 = truthdir(tree)
        dir2 = tmpdir(tree)
        self.setup(dir2)
        temp = '''-a Foo -p Bar -P 1 -s App -y 2016 --include *.py,f*.h,script? {d}'''
        args = temp.format(d=dir2).split()
        App.main(args)
        self.diff_dir(dir1, dir2)

    def test_config_exclude(self):
        tree = 'config_exclude'
        dir1 = truthdir(tree)
        dir2 = tmpdir(tree)
        self.setup(dir2)
        cfg = datadir(tree + '.json')
        temp = '''-a "Over Ride" -c {cfg} {d}'''
        args = shlex.split(temp.format(cfg=cfg, d=dir2))
        App.main(args)
        self.diff_dir(dir1, dir2)

    def test_no_recurse(self):
        tree = 'no_recurse'
        dir1 = truthdir(tree)
        dir2 = tmpdir(tree)
        self.setup(dir2)
        temp = '''-a Foo -s 'Best app.' -p MyApp -y 2016 -R {d}'''
        args = shlex.split(temp.format(d=dir2))
        App.main(args)
        self.diff_dir(dir1, dir2)

if '__main__' == __name__:
    unittest.main(verbosity=2)
