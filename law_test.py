import unittest
import law_compare

class StringTest(unittest.TestCase):
    def test_convert(self):
        v = law_compare.chstring2int('五十一')
        self.assertTrue(v == 51)

    def test_remove_first_line(self):
        content = 'aa\r\nbb\r\ncc'
        v = law_compare.remove_first_line(content)
        self.assertTrue(v == 'bb\r\ncc')

    def test_remove_first_line2(self):
        content = 'aabbcc'
        v = law_compare.remove_first_line(content)
        self.assertTrue(v == content)

if __name__ == "__main__":
    unittest.main()
