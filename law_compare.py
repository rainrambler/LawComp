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
        ##print("level 1:{}-----{}".format(i,sc))
        ##2）对每一部分进行转化处理，比如第二部分[ "三千二百四十二"]
        split_num = sc.replace('千', '1000').replace('百', '100').replace('十', '10')
        int_series = re.split(r'(\d{1,})', split_num)
        int_series.append("")
        int_series = ["".join(i) for i in zip(int_series[0::2],int_series[1::2])]
        int_series = ['零' if i == '' else i for i in int_series]
        num = 0
        ##int_series：["三1000", "二100", "四10", "二"]
        ##3）求和加总int_series
        for ix, it in enumerate(int_series):
            it = re.sub('零', '', it) if it != '零' else it
            ##print("level 2:{}{}".format(ix,it))
            temp = common_used_numerals_tmp[it[0]]*int(it[1:]) if len(it)>1 else common_used_numerals_tmp[it[0]]
            num += temp
            ##print("transformed part sum %s"%str(num))
        total_sum += num * (10 ** (4*(len(sep_char) - i - 1)))
    return total_sum

class CnLaw:
    '''CN PIPL'''
    curChapter = -1
    curSection = -1
    curArticle = -1
    id2content = {}
    
    def parse_chapter(self, content):
        '''Parse each chapter.'''
        arr = re.finditer(r'第[〇一二三四五六七八九]+章', content)
        #print("Total chapter:", len(arr))
        indices = []
        chapters = []

        for chapt in arr:
            #print(chapt)
            indices.append(chapt.span()[0])
        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            chapters.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        chapters.append(last)

        for item in chapters:
            self.parse_section(item)

    def parse_section(self, content):
        ''' eg: 第一节　一般规定
        '''
        print('==> Parsing section ', content[:30], '...')
        if re.search(r'第[〇一二三四五六七八九]+节', content) is None:
            self.parse_article(content)
            return
        arr = re.finditer(r'第[〇一二三四五六七八九]+节', content)
        #print("Sections: ", arr, "<==")
        indices = []
        sections = []
        
        for item in arr:
            #print(item)
            indices.append(item.span()[0])
        #print("Index:", indices)
        
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
        
        for item in sections:
            #print("Articles: ", item)
            #print('===')
            self.parse_article(item)
            
    def parse_article(self, content):
        ''' eg: 第十三条　符合下列...
        '''
        print('==> Parsing article ', content[:30], '...')
        arr = re.finditer(r'第[〇一二三四五六七八九十]+条', content)
        indices = []
        parts = []

        for item in arr:
            #print(item)
            indices.append(item.span()[0])
        #print(indices)

        if len(indices) == 0:
            return

        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        for item in parts:
            print(item[0:20])
            print('===')

    def parse_article_clause(self, content):
        ''' eg: （三）为履行法定职责或者法定义务所必需；
        '''
        print('==> Parsing clause ', content[:30], '...')
        arr = re.finditer(r'（[〇一二三四五六七八九十]+）', content)
        indices = []
        parts = []

        for item in arr:
            #print(item)
            indices.append(item.span()[0])
        #print(indices)

        if len(indices) == 0:
            return

        i = 0
        while i < len(indices)-1:
            part = content[indices[i]:indices[i+1]]
            parts.append(part)
            i+=1
        last = content[indices[len(indices)-1]:]
        parts.append(last)

        for item in parts:
            print(item[0:20])
            print('===')

def read_text_file(filename):
    '''
    Read text file to a string
    '''
    with open(filename, 'r', encoding='UTF-8') as file:
        data = file.read()
        return data
    return ''

def compare_gdpr_vs_cn():
    content = read_text_file('CN PIPL Stanford ZH.txt')
    alaw = CnLaw()
    alaw.parse_chapter(content)
    #print(content)

def main():
    compare_gdpr_vs_cn()

if __name__ == "__main__":
    main()
