import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)

class BloomTests(unittest.TestCase):

    def test_no_false_negatives(self):
        f = m.BloomFilter(200)
        for value in map(str, range(200)):
            f.add(value)
        self.assertTrue(all((f.contains(str(i)) for i in range(200))))

    def test_empty_has_no_members(self):
        f = m.BloomFilter()
        self.assertFalse(f.contains('a'))
        self.assertEqual(f.stats()['set_bits'], 0)




if __name__ == '__main__':
    unittest.main()
