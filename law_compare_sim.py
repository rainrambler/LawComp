"""
Filename: law_compare_sim.py
"""

from sentence_transformers import SentenceTransformer, util

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

    ai_model = SentenceTransformer("../paraphrase-multilingual-MiniLM-L12-v2")
    em_cn = ai_model.encode(crit_cn)
    em_eu = ai_model.encode(crit_eu)

    # Compute cosine-similarities for each sentence with each other sentence
    cos_scores = util.cos_sim(em_cn, em_eu)

    # Ref: https://www.sbert.net/docs/usage/semantic_textual_similarity.html 
    for i in range(len(crit_cn)):
        for j in range(len(crit_eu)):
            sim_val = cos_scores[i][j]
            if sim_val > 0.5:
                print("{} \t {} \t Score: {:.4f}".format(content_handler.trim_str(crit_cn[i], 30), \
                    content_handler.trim_str(crit_eu[j], 30), sim_val))
    #print(cos_scores) 

def main():
    ''' Entrance '''
    compare_gdpr_vs_cn()

if __name__ == "__main__":
    main()
