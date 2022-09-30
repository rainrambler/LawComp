import unittest
import re
import content_handler

class StringTest(unittest.TestCase):
    ''' testcase of string functions '''
    def test_convert(self):
        v = content_handler.chstring2int('五十一')
        self.assertTrue(v == 51)

    def test_remove_first_line(self):
        content = 'aa\r\nbb\r\ncc'
        v = content_handler.remove_first_line(content)
        self.assertTrue(v == 'bb\r\ncc')

    def test_remove_first_line2(self):
        content = 'aabbcc'
        v = content_handler.remove_first_line(content)
        self.assertTrue(v == content)

    def test_re_demo(self):
        content = '1. aaa'
        v = content_handler.re_demo(content)
        self.assertTrue(v == '1.')

    def test_re_demo2(self):
        content = 'ha'
        v = content_handler.re_demo(content)
        self.assertTrue(v == '')

    def test_re_demo3(self):
        content = 'aa 22. bb'
        v = content_handler.re_demo(content)
        self.assertTrue(v == '22.')

    def test_has_sub_article_1(self):
        content = 'aa 22． bb'
        v = content_handler.has_sub_article(content)
        self.assertTrue(v is True)

    def test_has_sub_article_2(self):
        content = 'aa . bb'
        v = content_handler.has_sub_article(content)
        self.assertTrue(v is False)

    def test_has_sub_article_3(self):
        content = '''
        第60条 领导性监管机构和其他相关监管机构的合作

1．领导性监管机构应当根据本条和其他相关监管机构进行合作，努力达成共识。领导性监管机构和相关监管机构应当彼此分享相关信息。

2．领导性监管机构可以随时要求其他相关监管机构提供第61条规定的互助合作，而且可以根据第62条而进行联合行动，这尤其适用于如下情形：为了进行调查，或者为了实施涉及到设立在另一成员国的控制者或处理者的措施。

        '''
        v = content_handler.has_sub_article(content)
        self.assertTrue(v is True)

    def test_is_valid_article_index_1(self):
        content = '第1条 aa'
        mo = re.search(r'第[0-9]+条', content)
        start_pos = mo.span()[0] # pos in string
        v = content_handler.is_valid_title_position(content, start_pos)
        self.assertTrue(v)

    def test_is_valid_article_index_2(self):
        content = '参考第10条'
        mo = re.search(r'第[0-9]+条', content)
        start_pos = mo.span()[0] # pos in string
        v = content_handler.is_valid_title_position(content, start_pos)
        self.assertFalse(v)

    def test_has_point_1(self):
        content = '(a) xx'
        v = content_handler.has_point(content)
        self.assertTrue(v)

    def test_has_point_2(self):
        content = 'axx'
        v = content_handler.has_point(content)
        self.assertFalse(v)

    def test_has_point_3(self):
        content = '123 (a) xx'
        v = content_handler.has_point(content)
        self.assertTrue(v)

if __name__ == "__main__":
    unittest.main()
