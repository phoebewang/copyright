import unittest

from copyright import diffdir

class TestDiff(unittest.TestCase):
    def test_diffdir(self):
        d = 'test/data/diff/'
        diffs = diffdir(d+'1', d+'2')
        diffs.sort()
        expect = [
            d+'1/f2',
            d+'1/sub1/f5',
            d+'2/f6',
            d+'2/f8',
            d+'2/sub1/f1',
            d+'2/sub1/f7']
        self.assertEqual(expect, diffs)

if '__main__' == __name__:
    unittest.main(verbosity=2)
