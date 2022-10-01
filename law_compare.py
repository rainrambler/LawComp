"""
calculate text2vec similarity
"""
# https://github.com/jpegbert/text2vec
from text2vec import SearchSimilarity
from cn_law import CnLaw
from eu_law import EuLaw
import content_handler

def compare_gdpr_vs_cn():
    ''' compare EU and cn privacy law '''
    content = content_handler.read_text_file('CN PIPL Stanford ZH.txt')
    alaw = CnLaw()
    alaw.parse_chapter(content)
    #alaw.print_details()

    content = content_handler.read_text_file('EU GDPR.txt')
    eu_law = EuLaw()
    eu_law.parse_chapter(content)
    #eu_law.print_details()

    compare_two_law(alaw, eu_law)

TOTAL_RESULT = 3

def compare_two_law(cl: CnLaw, el: EuLaw):
    ''' compare CN PIPL and EU GDPR '''
    crit_eu = el.get_criteria()
    crit_cn = cl.get_criteria()

    print(f'CN: {len(crit_cn)}, EU: {len(crit_eu)}')

    search_sim = SearchSimilarity(corpus = crit_eu)

    results = []
    for cnc1 in crit_cn:
        res = search_sim.get_similarities(query=cnc1)
        scores = search_sim.get_scores(query=cnc1)

        if len(scores) > 0:
            #print(scores[0], ':', cnc1, res[0])
            #print("-----------------------------------")
            result_num = TOTAL_RESULT
            if result_num > len(scores):
                result_num = len(scores)
            
            for i in range(result_num):
                cur_score = scores[i]
                if cur_score > 0:
                    results.append((cur_score, cnc1, res[i]))
        else:
            print("No scores found.")

    sort_results = sorted(results, key = lambda x: x[0], reverse=True)
    print(f"INFO: Total {len(sort_results)} results.")
    for item in sort_results:
        print(f'{item[0]}: {item[1]} | {item[2]}')

def main():
    ''' Entrance '''
    compare_gdpr_vs_cn()

if __name__ == "__main__":
    main()
