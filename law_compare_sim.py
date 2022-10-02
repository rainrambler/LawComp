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
DESIRED_LEN = 40

def compare_two_law(cl: CnLaw, el: EuLaw):
    ''' compare CN PIPL and EU GDPR '''
    crit_eu = el.get_criteria()
    crit_cn = cl.get_criteria()

    print(f'CN: {len(crit_cn)}, EU: {len(crit_eu)}')

    ai_model = SentenceTransformer("../paraphrase-multilingual-MiniLM-L12-v2")
    em_cn = ai_model.encode(crit_cn, convert_to_tensor=True)
    em_eu = ai_model.encode(crit_eu, convert_to_tensor=True)

    # Compute cosine-similarities for each sentence with each other sentence
    cos_scores = util.cos_sim(em_cn, em_eu)

    # Ref: https://www.sbert.net/docs/usage/semantic_textual_similarity.html
    top_pairs = []
    least_pairs = []
    for i, c_i in enumerate(crit_cn):
        pairs = []
        for j in range(len(crit_eu)):
            sim_val = cos_scores[i][j]
            if sim_val > 0.1:
                pairs.append({'index': [i, j], 'score': sim_val})

        #Sort scores in decreasing order
        pairs = sorted(pairs, key=lambda x: x['score'], reverse=True)

        # Append max and min matched items
        top_pair = pairs[0]
        bottom_pair = pairs[len(pairs)-1]
        top_pairs.append(top_pair)
        least_pairs.append(bottom_pair)

        for pair in pairs[0:TOTAL_RESULT]:
            i, j = pair['index']
            print("{} | {} | Score: {:.4f}".format(c_i, crit_eu[j], pair['score']))
            print('----------------------------------')

    print('==Top matches==================')
    #Sort scores in decreasing order
    top_pairs = sorted(top_pairs, key=lambda x: x['score'], reverse=True)
    for pair in top_pairs:
        i, j = pair['index']
        print("{} | {} | Score: {:.4f}".format(crit_cn[i], crit_eu[j], pair['score']))
        print('----------------------------------')

    print('==Least matches==================')
    #Sort scores in increasing order
    least_pairs = sorted(least_pairs, key=lambda x: x['score'], reverse=False)
    for pair in least_pairs:
        i, j = pair['index']
        print("{} | {} | Score: {:.4f}".format(crit_cn[i], crit_eu[j], pair['score']))
        print('----------------------------------')

def main():
    ''' Entrance '''
    compare_gdpr_vs_cn()

if __name__ == "__main__":
    main()
