"""
Filename: cn_law.py
"""
# for string regex
import re
import content_handler

class CnLaw:
    '''CN PIPL'''
    cur_chapter = ""
    cur_section = ""
    cur_article = ""
    cur_clause = ""
    id2content = {}

    def print_clauses(self):
        for k, v in self.id2content.items():
            print(f'[{k}]:{v[0:30]}')

    def print_details(self):
        ''' Print contents '''
        for k, v in self.id2content.items():
            print(f'[{k}]:{v}')

    def get_criteria(self):
        ''' return all criteria '''
        arr = []
        for k, v in self.id2content.items():
            criterion = f"{k} {v}"
            arr.append(criterion)
        return arr

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
            sections = content_handler.remove_first_line(one_chapter)
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
            subs = content_handler.remove_first_line(one_section)
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
            start_pos = item.span()[0] # pos in string
            if content_handler.is_valid_title_position(content, start_pos):
                indices.append(start_pos)
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
                self.cur_clause = ""
                cur_id = self.create_id()
                self.id2content[cur_id] = one_article

    def create_id(self):
        ''' Make id in dict'''
        if len(self.cur_section) > 0:
            if len(self.cur_clause) > 0:
                return self.cur_chapter + "_" + self.cur_section + "_" + self.cur_article \
                    + "_" + self.cur_clause
            else:
                return self.cur_chapter + "_" + self.cur_section + "_" + self.cur_article
        else:
            if len(self.cur_clause) > 0:
                return self.cur_chapter + "_" + self.cur_article + "_" + self.cur_clause
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
        #print('[DBG]', clause_ids)

        totalcount = len(clause_ids)
        if totalcount != len(parts):
            print(f"WARN: Clauses Len: {totalcount} and {len(parts)}.")
            return
        for i in range(totalcount):
            one_clause = parts[i]
            self.cur_clause = clause_ids[i]
            cur_id = self.create_id()
            self.id2content[cur_id] = one_clause
