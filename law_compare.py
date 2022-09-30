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

class CnLaw:
    '''CN PIPL'''
    cur_chapter = ""
    cur_section = ""
    cur_article = ""
    id2content = {}

    def print_clauses(self):
        for k, v in self.id2content.items():
            print(f'[{k}]:{v[0:30]}')
    
    def parse_chapter(self, content):
        '''Parse each chapter.'''
        arr = re.finditer(r'第[〇一二三四五六七八九]+章', content)
        indices = []
        chapters = []
        chapter_ids = []

        for chapt in arr:
            indices.append(chapt.span()[0])
            chapter_ids.append(chapt.group(0))
        #print(chapter_ids)
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            chapters.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        chapters.append(last)

        totalcount = len(chapter_ids)
        if totalcount != len(chapters):
            print(f"WARN: Chapter Len: {totalcount} and {len(chapters)}.")
            return

        for i in range(totalcount):
            one_chapter = chapters[i]
            self.cur_chapter = chapter_ids[i]
            sections = remove_first_line(one_chapter)
            self.parse_section(sections)

    def parse_section(self, content):
        ''' eg: 第一节　一般规定
        '''
        #print('==> Parsing section ', content[:30], '...')
        if re.search(r'第[〇一二三四五六七八九]+节', content) is None:
            self.cur_section = ""
            self.parse_article(content)
            return
        arr = re.finditer(r'第[〇一二三四五六七八九]+节', content)
        #print("Sections: ", arr, "<==")
        indices = []
        sections = []
        section_ids = []
        
        for item in arr:
            indices.append(item.span()[0])
            section_ids.append(item.group(0))
        #print("section_ids:", section_ids)
        
        if len(indices) == 0:
            print("No Index in ", content[:30], '')
            return
        
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            sections.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        sections.append(last)

        totalcount = len(section_ids)
        if totalcount != len(sections):
            print(f"WARN: Sections Len: {totalcount} and {len(sections)}.")
            return
        
        for i in range(totalcount):
            one_section = sections[i]
            self.cur_section = section_ids[i]
            subs = remove_first_line(one_section)
            self.parse_article(subs)
            
    def parse_article(self, content):
        ''' eg: 第十三条　符合下列...
        '''
        #print('==> Parsing article ', content[:30], '...')
        arr = re.finditer(r'第[〇一二三四五六七八九十]+条', content)
        indices = []
        parts = []
        article_ids = []

        for item in arr:
            indices.append(item.span()[0])
            article_ids.append(item.group(0))

        if len(indices) == 0:
            return

        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        totalcount = len(article_ids)
        if totalcount != len(parts):
            print(f"WARN: Articles Len: {totalcount} and {len(parts)}.")
            return

        for i in range(totalcount):
            one_article = parts[i]
            self.cur_article = article_ids[i]

            if self.has_clause(one_article):
                self.parse_article_clause(one_article)
            else:
                cur_id = self.create_id()
                self.id2content[cur_id] = one_article

    def create_id(self):
        ''' Make id in dict'''
        if len(self.cur_section) > 0:
            return self.cur_chapter + "_" + self.cur_section + "_" + self.cur_article
        else:
            return self.cur_chapter + "_" + self.cur_article

    def has_clause(self, content):
        ''' Does article have clause '''
        return re.search(r'（[〇一二三四五六七八九十]+）', content) is not None

    def parse_article_clause(self, content):
        ''' eg: （三）为履行法定职责或者法定义务所必需；
        '''
        #print('==> Parsing clause ', content[:30], '...')
        arr = re.finditer(r'（[〇一二三四五六七八九十]+）', content)
        indices = []
        parts = []
        clause_ids = []

        for item in arr:
            indices.append(item.span()[0])
            clause_ids.append(item.group(0))

        mainclause = content[:indices[0]]
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(mainclause + part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(mainclause+last)

        totalcount = len(clause_ids)
        if totalcount != len(parts):
            print(f"WARN: Clauses Len: {totalcount} and {len(parts)}.")
            return
        for i in range(totalcount):
            one_clause = parts[i]
            cur_id = self.create_id()
            self.id2content[cur_id] = one_clause

SUB_ARTICLE_MATCH = r'[0-9]+．' # Caution: not English dot 

class EuLaw:
    '''EU GDPR
    EN: CHAPTER III / Section 1 / Article 12 / 1. / (a) 
    ZH: 第三章 / 第一部分 / 第12条 / 1． / (a)
    '''
    cur_chapter = ""
    cur_article = ""
    cur_subarticle = ""
    id2content = {}

    def print_contents(self):
        ''' Print contents '''
        for k, v in self.id2content.items():
            print(f'[{k}]:{v[0:30]}')

    def print_briefings(self):
        ''' Print briefings '''
        print("Total articles: ", len(self.id2content))

    def parse_chapter(self, content):
        '''Parse each chapter. eg: 第二章 原则'''
        arr = re.finditer(r'第[〇一二三四五六七八九]+章', content)
        indices = []
        chapters = []
        chapter_ids = []

        for chapt in arr:
            indices.append(chapt.span()[0])
            chapter_ids.append(chapt.group(0))
        #print(chapter_ids)
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            chapters.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        chapters.append(last)

        totalcount = len(chapter_ids)
        if totalcount != len(chapters):
            print(f"WARN: Chapter Len: {totalcount} and {len(chapters)}.")
            return

        for i in range(totalcount):
            one_chapter = chapters[i]
            self.cur_chapter = chapter_ids[i]
            sections = remove_first_line(one_chapter)
            self.parse_section(sections)

    def parse_section(self, content: str):
        ''' eg: 第一部分 透明性与模式
        '''
        #print('==> Parsing section ', content[:30], '...')
        arr = content.splitlines()
        section_content = ""
        if len(arr) <= 1:
            section_content = content
            self.parse_article(section_content)
            return

        for a_sec in arr:
            if re.search(r'第[〇一二三四五六七八九]+部分', a_sec) is None:
                section_content = section_content + a_sec + '\r\n'

        self.parse_article(section_content)

    def parse_article(self, content):
        ''' eg: 第12条 信息... '''
        print('==> Parsing article [', content[:30], ']...')
        arr = re.finditer(r'第[0-9]+条', content)
        indices = []
        parts = []
        article_ids = []

        for item in arr:
            start_pos = item.span()[0] # pos in string
            indices.append(start_pos) 
            article_ids.append(item.group(0)) # title, eg. 第12条

        if len(indices) == 0:
            return

        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        totalcount = len(article_ids)
        if totalcount != len(parts):
            print(f"WARN: Articles Len: {totalcount} and {len(parts)}.")
            return

        for i in range(totalcount):
            one_article = parts[i]
            #print('Cur Article: ', one_article)
            self.cur_article = article_ids[i]

            if has_sub_article(one_article):
                self.parse_sub_article(one_article)
            else:
                cur_id = self.create_id()
                self.add_article(cur_id, one_article)

    def add_article(self, a_id: int, article: str):
        '''Add an article'''
        self.id2content[a_id] = article

    def parse_sub_article(self, content):
        ''' eg: 第7条 同意的条件 ==> 1．当处理
        '''
        print('==> Parsing sub article ', content[:30], '...')
        arr = re.finditer(SUB_ARTICLE_MATCH, content)
        print("Founded sub articles: ", arr)

        indices = []
        parts = []
        article_ids = []

        for item in arr:
            indices.append(item.span()[0]) # pos in string
            article_ids.append(item.group(0)) # title, eg. 1．当处理

        if len(indices) == 0:
            return

        print(article_ids)
        print('=-=-=-=')
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        totalcount = len(article_ids)
        if totalcount != len(parts):
            print(f"WARN: Sub Articles Len: {totalcount} and {len(parts)}.")
            return

        for i in range(totalcount):
            one_article = parts[i]
            self.cur_subarticle = article_ids[i]

            if self.has_point(one_article):
                #self.parse_point(one_article)
                # TODO
                cur_id = self.create_id()
                self.id2content[cur_id] = one_article
            else:
                cur_id = self.create_id()
                self.id2content[cur_id] = one_article

    def parse_point(self, content):
        ''' eg: (a)第五章规定的
        '''
        #print('==> Parsing point ', content[:30], '...')
        arr = re.finditer(r'([a-z]+)', content)
        indices = []
        parts = []
        point_ids = []

        for item in arr:
            indices.append(item.span()[0]) # pos in string
            point_ids.append(item.group(0)) # title, eg. (a)第五章规定的

        print(point_ids)
        print('=======')
        if len(indices) == 0:
            return

        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        totalcount = len(point_ids)
        if totalcount != len(parts):
            print(f"WARN: Points Len: {totalcount} and {len(parts)}.")
            return

        for i in range(totalcount):
            one_article = parts[i]
            cur_id = self.create_id()
            self.id2content[cur_id] = one_article

    def create_id(self):
        ''' Make id in dict'''
        if len(self.cur_subarticle) == 0:
            return self.cur_chapter + "_" + self.cur_article
        else:
            return self.cur_chapter + "_" + self.cur_article + " (" + self.cur_subarticle + ')'

    def has_point(self, content):
        ''' Does article have clause '''
        return re.search(r'([a-z]+)', content) is not None

def has_sub_article(content: str):
    ''' Does article have sub article '''
    return re.search(SUB_ARTICLE_MATCH, content) is not None

def is_valid_article_index(content: str, pos: int):
    '''
    '第1条 aa' ==> True
    '参考第10条' ==> False
    '''
    prev_pos = pos-1
    if prev_pos < 0:
        # the first char
        print(f"pos: {pos}, in {content}, first char")
        return True
    if prev_pos >= len(content):
        print(f"pos: {pos}, in {content}, exceed")
        return False
    cur_char = content[prev_pos]
    print(f"pos: {pos}, in {content}, char: [{cur_char}]")
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

def compare_gdpr_vs_cn():
    ''' compare EU and cn privacy law '''
    content = read_text_file('CN PIPL Stanford ZH.txt')
    alaw = CnLaw()
    alaw.parse_chapter(content)
    alaw.print_clauses()

    content = read_text_file('EU GDPR.txt')
    eu_law = EuLaw()
    eu_law.parse_chapter(content)
    eu_law.print_contents()
    #eu_law.print_briefings()


def re_demo(content):
    ''' Demo for regex match '''
    idx_match = re.compile(r'[0-9]+\.')
    mo = idx_match.search(content)
    if mo is None:
        return ""
    else:
        return mo.group()

def main():
    ''' Entrance '''
    compare_gdpr_vs_cn()

if __name__ == "__main__":
    main()
