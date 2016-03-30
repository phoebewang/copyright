import os
import unittest
from copyright import Walk

class TestWalk(unittest.TestCase):
    DIRS = [
        './tmp/dir1/dir2',
        './tmp/dir3'
    ]

    FILES = [
        './tmp/f',
        './tmp/dir1/f1',
        './tmp/dir3/f3',
        './tmp/dir1/dir2/f2'
    ]

    def setUp(self):
        for d in self.DIRS:
            os.makedirs(d)

        for p in self.FILES:
            with open(p, 'w') as f:
                pass

    def tearDown(self):
        for p in self.FILES:
            if os.path.exists(p):
                os.remove(p)

        for d in self.DIRS:
            if os.path.exists(d):
                os.removedirs(d)

    def test_default(self):
        files = []
        for f in Walk():
            files.append(f)

        for f in self.FILES:
            self.assertTrue(f in files)

    def test_exclude(self):
        files = []
        exclude = ['f1', 'f2']
        for f in Walk(exclude=exclude):
            files.append(f)

        self.assertTrue(self.FILES[0] in files)
        self.assertTrue(self.FILES[2] in files)
        self.assertFalse(self.FILES[1] in files)
        self.assertFalse(self.FILES[3] in files)

    def test_include(self):
        files = []
        include = ['*1', 'dir2']
        for f in Walk(include=include):
            files.append(f)

        self.assertFalse(self.FILES[0] in files)
        self.assertTrue(self.FILES[1] in files)
        self.assertFalse(self.FILES[2] in files)
        self.assertTrue(self.FILES[3] in files)

    def test_include_regex(self):
        files = []
        include = ['f[\d]$']
        for f in Walk(include=include, regex=True):
            files.append(f)

        self.assertTrue(self.FILES[1] in files)
        self.assertTrue(self.FILES[2] in files)
        self.assertTrue(self.FILES[3] in files)
        self.assertFalse(self.FILES[0] in files)

    def test_path(self):
        files = []
        for f in Walk(path='./tmp'):
            files.append(f)

        for f in self.FILES:
            self.assertTrue(f in files)

if '__main__' == __name__:
    unittest.main(verbosity=2)
