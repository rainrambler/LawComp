"""
Filename: law_compare.py
"""
# for string regex
import re

common_used_numerals_tmp ={'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, \
    '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}

# https://www.jianshu.com/p/ab16e5af5c32
def chstring2int(uchar):
    '''
    Chinese string to int value. eg. '五十一' ==> 51 (int)
    '''
    ##1）按亿、万分割字符
    sep_char = re.split(r'亿|万',uchar)
    total_sum = 0
    for i,sc in enumerate(sep_char):
        ##2）对每一部分进行转化处理，比如第二部分[ "三千二百四十二"]
        split_num = sc.replace('千', '1000').replace('百', '100').replace('十', '10')
        int_series = re.split(r'(\d{1,})', split_num)
        int_series.append("")
        int_series = ["".join(i) for i in zip(int_series[0::2],int_series[1::2])]
        int_series = ['零' if i == '' else i for i in int_series]
        num = 0
        ##3）求和加总int_series
        for ix, it in enumerate(int_series):
            it = re.sub('零', '', it) if it != '零' else it
            temp = common_used_numerals_tmp[it[0]]*int(it[1:]) \
                if len(it)>1 else common_used_numerals_tmp[it[0]]
            num += temp
        total_sum += num * (10 ** (4*(len(sep_char) - i - 1)))
    return total_sum

def has_point(content: str):
    ''' Does article have point '''
    return re.search(EU_POINT_MATCH, content) is not None

SUB_ARTICLE_MATCH = r'[0-9]+．' # Caution: not English dot

EU_POINT_MATCH = r'\([a-z]\)'

def has_sub_article(content: str):
    ''' Does article have sub article '''
    return re.search(SUB_ARTICLE_MATCH, content) is not None

def is_valid_title_position(content: str, pos: int):
    '''
    '第1条 aa' ==> True
    '参考第10条' ==> False
    '''
    prev_pos = pos-1
    if prev_pos < 0:
        # the first char
        #print(f"pos: {pos}, in {content}, first char")
        return True
    if prev_pos >= len(content):
        #print(f"pos: {pos}, in {content}, exceed")
        return False
    cur_char = content[prev_pos]
    #print(f"pos: {pos}, in {content}, char: [{cur_char}]")
    return cur_char == '\n'

def read_text_file(filename):
    '''
    Read text file to a string
    '''
    with open(filename, 'r', encoding='UTF-8') as file:
        data = file.read()
        return data
    return ''

def remove_first_line(content):
    ''' Remove first line in multi-line content '''
    idx = content.find('\n')
    if idx == -1:
        return content
    return content[idx+1:]

def re_demo(content):
    ''' Demo for regex match '''
    idx_match = re.compile(r'[0-9]+\.')
    mo = idx_match.search(content)
    if mo is None:
        return ""
    else:
        return mo.group()
