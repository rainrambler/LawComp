import unittest
import law_compare

class StringTest(unittest.TestCase):
    # Returns True or False. 
    def testConvert(self):
        v = law_compare.chstring2int('五十一')
        self.assertTrue(v == 51)

if __name__ == "__main__":
    unittest.main()
