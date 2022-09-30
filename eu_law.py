"""
Filename: en_law.py
"""
# for string regex
import re
import content_handler

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

    def print_details(self):
        ''' Print contents '''
        for k, v in self.id2content.items():
            print(f'[{k}]:{v}')

    def print_briefings(self):
        ''' Print briefings '''
        print("Total articles: ", len(self.id2content))

    def get_criteria(self):
        ''' return all criteria '''
        arr = []
        for k, v in self.id2content.items():
            criterion = f"{k} {v}"
            arr.append(criterion)
        return arr

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
            sections = content_handler.remove_first_line(one_chapter)
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
        #print('==> Parsing article [', content[:30], ']...')
        arr = re.finditer(r'第[0-9]+条', content)
        indices = []
        parts = []
        article_ids = []

        for item in arr:
            start_pos = item.span()[0] # pos in string
            if content_handler.is_valid_title_position(content, start_pos):
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
            self.cur_article = article_ids[i]

            if content_handler.has_sub_article(one_article):
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
        #print('==> Parsing sub article ', content[:30], '...')
        arr = re.finditer(content_handler.SUB_ARTICLE_MATCH, content)
        #print("Founded sub articles: ", arr)

        indices = []
        parts = []
        article_ids = []

        for item in arr:
            indices.append(item.span()[0]) # pos in string
            article_ids.append(item.group(0)) # title, eg. 1．当处理

        if len(indices) == 0:
            return

        #print(article_ids)
        #print('=-=-=-=')
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

            if content_handler.has_point(one_article):
                self.parse_point(one_article)
                #cur_id = self.create_id()
                #self.id2content[cur_id] = one_article
            else:
                cur_id = self.create_id()
                self.id2content[cur_id] = one_article

    def parse_point(self, content):
        ''' eg: (a)对涉及到
        '''
        #print('==> Parsing point ', content[:30], '...')
        arr = re.finditer(content_handler.EU_POINT_MATCH, content)
        indices = []
        parts = []
        point_ids = []

        for item in arr:
            start_pos = item.span()[0] # pos in string
            if content_handler.is_valid_title_position(content, start_pos):
                indices.append(start_pos)
                point_ids.append(item.group(0)) # title, eg. (a)

        if len(indices) == 0:
            return

        print(point_ids)
        print('=======')
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
            a_point = parts[i]
            point_id = point_ids[i]
            cur_id = self.create_id()
            self.id2content[cur_id+"_"+point_id] = a_point

    def create_id(self):
        ''' Make id in dict'''
        if len(self.cur_subarticle) == 0:
            return self.cur_chapter + "_" + self.cur_article
        else:
            pure_id = self.cur_subarticle.replace('．', '')
            return self.cur_chapter + "_" + self.cur_article + " (" + pure_id + ')'
