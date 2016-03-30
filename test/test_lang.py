import os
import unittest

from glob import glob
from copyright import CLang, Comments, Detector

def teardown():
    for f in glob('tmp.*'):
        os.remove(f)

class TestCLang(unittest.TestCase):
    EXT = 'h hpp C CPP cxx'.split()

    def setUp(self):
        for x in self.EXT:
            with open('tmp.empty.' + x, 'w') as f:
                pass

        with open('tmp.c.0', 'w') as f:
            f.write('#include <stdio.h>');

        with open('tmp.c.1', 'w') as f:
            f.write('#ifndef FOO_H');

        with open('tmp.c.2', 'w') as f:
            f.write('#pragma once');

        with open('tmp.comments.c', 'w') as f:
            f.write('// foo\n// bar\n/* multi\n * line\n */\n#define CODE\n');

    def tearDown(self):
        teardown()

    def test_comment(self):
        s = '1\n2'
        e1 = '/*\n 1\n 2\n*/'
        e2 = '// 1\n// 2'
        c = CLang()

        r = c.comment(s, single=False, pad=1)
        self.assertEqual(e1, r)
        r = c.comment(s, single=True, pad=1)
        self.assertEqual(e2, r)

    def test_detect_ext(self):
        for x in self.EXT:
            n = 'tmp.empty.' + x
            self.assertEqual('c', Detector.detect(n))

    def test_detect_body(self):
        for x in '0 1 2'.split():
            n = 'tmp.c.' + x
            self.assertEqual('c', Detector.detect(n))

    def test_header(self):
        self.assertEqual(13, CLang().header('tmp.comments.c'))

class TestJavaLang(unittest.TestCase):
    def setUp(self):
        for x in 'java js'.split():
            with open('tmp.empty.' + x, 'w') as f:
                pass

        with open('tmp.java.0', 'w') as f:
            f.write('package foo.bar;');

        with open('tmp.java.1', 'w') as f:
            f.write('import foo.bar;');

    def tearDown(self):
        teardown()

    def test_detect_ext(self):
        for x in 'java js'.split():
            n = 'tmp.empty.' + x
            self.assertEqual('java', Detector.detect(n))

    def test_detect_body(self):
        for x in '0 1'.split():
            n = 'tmp.java.' + x
            self.assertEqual('java', Detector.detect(n))

class TestPyLang(unittest.TestCase):
    def setUp(self):
        for x in ['py']:
            with open('tmp.empty.' + x, 'w') as f:
                pass

        with open('tmp.py.0', 'w') as f:
            f.write('#!/usr/bin/env python2.7;');

        with open('tmp.py.1', 'w') as f:
            f.write('from foo import bar');

        with open('tmp.py.2', 'w') as f:
            f.write('import bar');

    def tearDown(self):
        teardown()

    def test_detect_ext(self):
        for x in ['py']:
            n = 'tmp.empty.' + x
            self.assertEqual('py', Detector.detect(n))

    def test_detect_body(self):
        for x in '0 1 2'.split():
            n = 'tmp.py.' + x
            self.assertEqual('py', Detector.detect(n))

class TestShLang(unittest.TestCase):
    EXT = 'bash ksh csh tcsh zsh bash'.split()

    def setUp(self):
        for x in self.EXT:
            with open('tmp.empty.' + x, 'w') as f:
                pass

        with open('tmp.sh.0', 'w') as f:
            f.write('#!/usr/bin/sh;');

        with open('tmp.sh.1', 'w') as f:
            f.write('#!/usr/bin/env bash');

        with open('tmp.sh.2', 'w') as f:
            f.write('source foo');

        with open('tmp.sh.3', 'w') as f:
            f.write('set -x');

        with open('tmp.sh.4', 'w') as f:
            f.write('export foo=1');

    def tearDown(self):
        teardown()

    def test_detect_ext(self):
        for x in self.EXT:
            n = 'tmp.empty.' + x
            self.assertEqual('sh', Detector.detect(n))

    def test_detect_body(self):
        for x in '0 1 2 3 4'.split():
            n = 'tmp.sh.' + x
            self.assertEqual('sh', Detector.detect(n))

class TestXmlLang(unittest.TestCase):
    EXT = 'htm html xml'.split()

    def setUp(self):
        for x in self.EXT:
            with open('tmp.empty.' + x, 'w') as f:
                pass

        with open('tmp.xml.0', 'w') as f:
            f.write('<!--');

        with open('tmp.xml.1', 'w') as f:
            f.write('<!DOCTYPE');

        with open('tmp.xml.2', 'w') as f:
            f.write('<html');

        with open('tmp.xml.3', 'w') as f:
            f.write('<script');

        with open('tmp.xml.4', 'w') as f:
            f.write('<?xml');

    def tearDown(self):
        teardown()

    def test_detect_ext(self):
        for x in self.EXT:
            n = 'tmp.empty.' + x
            self.assertEqual('xml', Detector.detect(n))

    def test_detect_body(self):
        for x in '0 1 2 3 4'.split():
            n = 'tmp.xml.' + x
            self.assertEqual('xml', Detector.detect(n))

class TestComments(unittest.TestCase):
    def setUp(self):
        text = '''// skip

/*
Some long
block
Copyright 2000
*/

// short
// COPYRIGHT 2001
// message

/* Another copyright 2002
*/
// None
// in
// here
#define CODE 1'''
        with open('tmp.c', 'w') as f:
            f.write(text)

    def tearDown(self):
        teardown()

    def test_findCopyright(self):
        offsets = Comments.findCopyright(file='tmp.c',
                                         start='/*', stop='*/', single='//')
        expect = [ (9,45), (47,84), (86,114) ]
        self.assertEqual(expect, offsets)

if '__main__' == __name__:
    unittest.main(verbosity=2)
