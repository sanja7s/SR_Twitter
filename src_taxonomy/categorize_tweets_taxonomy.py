#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
from collections import defaultdict, OrderedDict
import json
import re
import glob, os
import math
import itertools

f_in = "tweets_taxonomy_clean.JSON"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../DATA/taxonomy_stats/"
spec_users = "communitiesMent.txt"

def read_user_IDs():

    user_ids = defaultdict(str)

    with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_ids[user] = user_id

    return user_ids

# to return top sizeN communities, as many as there are
# in a form of a dictionary: {community_id: defaultdict{id_usr1:1, id_usr2:1, ...}}
def read_in_communities(sizeN=300):

    res = defaultdict(int)
    res7s = defaultdict(int)

    f = open(spec_users, "r")

    for line in f:
        line = line.split()
        user_id = line[0]
        com_id = line[1]
        if com_id not in res:
            res[com_id] = defaultdict(int)
        res[com_id][user_id] = 1

    for com in res:
        if len(res[com]) >= sizeN:
            res7s[com] = res[com]

    return res7s


def read_save_taxonomy(users="ALL", user_list=None, WRITE=False,TOP_N = 20, f=None):

    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    docSentiment_sum = defaultdict(int) 
    taxonomies_sum = defaultdict(int) 

    user_ids = read_user_IDs()

    cnt = 0

    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                if users <> "ALL":
                    user_name = line["_id"]
                    user_id = user_ids[user_name]
                    if user_list[user_id] == 0:
                        continue 
                taxonomy_all = line["taxonomy"]
                keywords = taxonomy_all["keywords"]
                entities = taxonomy_all["entities"]
                taxonomy = taxonomy_all["taxonomy"] 
                docSentiment = taxonomy_all["docSentiment"] 
                concepts = taxonomy_all["concepts"] 
            except KeyError:
                #print line7s
                continue

            for el in keywords:
                category = el["text"]
                if not category in keywords_sum:
                    keywords_sum[category] = defaultdict(int)
                old_relev = keywords_sum[category][0]
                old_cnt = keywords_sum[category][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                keywords_sum[category] = (new_relev, new_cnt)

            sentiment = docSentiment["type"]
            if sentiment == "neutral":
                docSentiment_sum[sentiment] += 1
            else:
                if not sentiment in docSentiment_sum:
                    docSentiment_sum[sentiment] = defaultdict(int)
                old_score = docSentiment_sum[sentiment][0]
                old_cnt = docSentiment_sum[sentiment][1]
                old_mixed_cnt = docSentiment_sum[sentiment][2]
                try:
                    new_score = old_score + float(docSentiment["score"])
                except KeyError:
                    continue
                new_cnt = old_cnt + 1
                try:
                    new_mixed_cnt = old_mixed_cnt + int(docSentiment["mixed"])
                except KeyError:
                    continue
                docSentiment_sum[sentiment] = (new_score, new_cnt, new_mixed_cnt)


            for el in taxonomy:
                taxonomy_tree = el["label"]
                taxonomy_tree = taxonomy_tree.split("/")
                levels = len(taxonomy_tree)
                taxon = ""
                for taxon_level in range(levels-1, 0, -1):
                    taxon = taxonomy_tree[taxon_level] + "/" + taxon
                    if not taxon in taxonomies_sum:
                        taxonomies_sum[taxon] = defaultdict(int)
                    old_score = taxonomies_sum[taxon][0]
                    old_cnt = taxonomies_sum[taxon][1]
                    old_sent = taxonomies_sum[taxon][2]
                    new_score = old_score + float(el["score"])
                    new_cnt = old_cnt + 1
                    pos_sent = taxonomies_sum[taxon][3]
                    pos_cnt = taxonomies_sum[taxon][4]
                    neg_sent = taxonomies_sum[taxon][5]
                    neg_cnt = taxonomies_sum[taxon][6]
                    if sentiment == "positive":
                        pos_sent = pos_sent + float(docSentiment["score"])
                        pos_cnt = pos_cnt + 1
                    elif sentiment == "negative":
                        neg_sent = neg_sent + float(docSentiment["score"])
                        neg_cnt = neg_cnt + 1
                    level = levels - taxon_level
                    taxonomies_sum[taxon] = (new_score, new_cnt, level, pos_sent, pos_cnt, neg_sent, neg_cnt)


            for el in entities:
                entity = el["text"]
                if not entity in entities_sum:
                    entities_sum[entity] = defaultdict(int)
                old_relev = entities_sum[entity][0]
                old_cnt = entities_sum[entity][1]
                old_internal_count = entities_sum[entity][2]
                old_weighted_relev = entities_sum[entity][4]
                new_relev = old_relev + float(el["relevance"])
                new_weighted_relev = old_weighted_relev + (float(el["relevance"]) * float(el["count"]))
                new_cnt = old_cnt + 1
                new_internal_count = old_internal_count + int(el["count"])
                entities_sum[entity] = (new_relev, new_cnt, new_internal_count, el["type"], new_weighted_relev)


            for el in concepts:
                concept = el["text"]
                if not concept in concepts_sum:
                    concepts_sum[concept] = defaultdict(int)
                old_relev = concepts_sum[concept][0]
                old_cnt = concepts_sum[concept][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                concepts_sum[concept] = (new_relev, new_cnt)

            cnt += 1


        com_size = cnt

        N = cnt
        for kw in keywords_sum:
            tot_relev = keywords_sum[kw][0]
            tot_cnt = keywords_sum[kw][1]
            keywords_sum[kw] = (tot_relev, tot_cnt, float(tot_relev * math.log(N/tot_cnt)))

        
        for sn in taxonomies_sum:
            tot_score = taxonomies_sum[sn][0]
            tot_pos_sent = taxonomies_sum[sn][3]
            tot_pos_cnt = taxonomies_sum[sn][4]
            tot_neg_sent = taxonomies_sum[sn][5]
            tot_neg_cnt = taxonomies_sum[sn][6]
            tot_cnt = taxonomies_sum[sn][1]
            tot_level = taxonomies_sum[sn][2]
            tot_pos_sent = float(tot_pos_sent / tot_pos_cnt) if tot_pos_cnt else 0
            tot_neg_sent = float(tot_neg_sent / tot_neg_cnt) if tot_neg_cnt else 0
            taxonomies_sum[sn] = (tot_score, tot_cnt, tot_level, tot_pos_sent, tot_pos_cnt, tot_neg_sent, tot_neg_cnt)
        '''
        for en in entities_sum:
            tot_relev = entities_sum[en][0]
            tot_cnt = entities_sum[en][1]
            tot_internal_cnt = entities_sum[en][2]
            tot_type = entities_sum[en][3]
            tot_weighted_relev = float(entities_sum[en][4] / tot_internal_cnt)
            entities_sum[en] = (tot_relev, tot_cnt, tot_internal_cnt, tot_type, tot_weighted_relev)  
        '''    

        print cnt        
        print "Total keywords found ", len(keywords_sum)
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "Total Sentiments found ", len(docSentiment_sum)
        print "Total entities found ", len(entities_sum)
        print "Total concepts found ", len(concepts_sum)

        print
        print "Keywords (ordered by TF-IDF score): [relevance, count, TF-IDF]"
        ord_keywords_sum2 = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][2], reverse = True))
        i = 0
        for el in ord_keywords_sum2:
            print el, ord_keywords_sum2[el]
            i += 1
            if i == TOP_N:
                break
        print

        print
        print "Keywords: [relevance, count, TF-IDF]"
        ord_keywords_sum = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_keywords_sum:
            print el, ord_keywords_sum[el]
            i += 1
            if i == TOP_N:
                break
        print

        print "Taxonomies: [relevance, tot_count, level, pos_sentiment, pos_sentiment_cnt, neg_sentiment, neg_sentiment_cnt]"
        ord_taxonomies_sum = OrderedDict(sorted(taxonomies_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_taxonomies_sum:
            print el, ord_taxonomies_sum[el]
            i += 1
            if i == TOP_N:
                break
        print

        print "Sentiment: [type, score, count, mixed_count]"
        i = 0
        for el in docSentiment_sum:
            print el, docSentiment_sum[el]
            i += 1
            if i == TOP_N:
                break
        print

        print "Entities: [relevance, cnt, internal_cnt, type, weighted_relev]"
        ord_entities_sum = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_entities_sum:
            print el, ord_entities_sum[el]
            i += 1
            if i == TOP_N:
                break
            
        print

        print "Entities (sorted by weighted_relev): [relevance, cnt, internal_cnt, type, weighted_relev]"
        ord_entities_sum2 = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1][4], reverse = True))
        i = 0
        for el in ord_entities_sum2:
            print el, ord_entities_sum2[el]
            i += 1
            if i == TOP_N:
                break
        print

        print "Concepts: [relevance, count]"
        ord_concepts_sum = OrderedDict(sorted(concepts_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_concepts_sum:
            print el, ord_concepts_sum[el]
            i += 1
            if i == TOP_N:
                break

        TOP_N = 100

        if WRITE:
            taxonomies_sum7 = dict(itertools.islice(ord_taxonomies_sum.items(), 0, TOP_N))
            keywords_sum7 = dict(itertools.islice(ord_keywords_sum.items(), 0, TOP_N))
            entities_sum7 = dict(itertools.islice(ord_entities_sum.items(), 0, TOP_N))
            concepts_sum7 = dict(itertools.islice(ord_concepts_sum.items(), 0, TOP_N))

            taxonomies_sum7s = OrderedDict(sorted(taxonomies_sum7.items(), key=lambda x: x[1][1], reverse = True))
            keywords_sum7s  = OrderedDict(sorted(keywords_sum7.items(), key=lambda x: x[1][1], reverse = True))
            entities_sum7s = OrderedDict(sorted(entities_sum7.items(), key=lambda x: x[1][4], reverse = True))
            concepts_sum7s = OrderedDict(sorted(concepts_sum7.items(), key=lambda x: x[1][1], reverse = True))

            taxonomies_out7s = {}
            taxonomies_out7s['_id'] = users
            taxonomies_out7s['size'] = com_size
            taxonomies_out7s['taxonomy'] = taxonomies_sum7s
            taxonomies_out7s['keywords'] = keywords_sum7s
            taxonomies_out7s['sentiment'] = docSentiment_sum
            taxonomies_out7s['entities'] = entities_sum7s
            taxonomies_out7s['concepts'] = concepts_sum7s

            f.write(unicode(json.dumps(taxonomies_out7s, ensure_ascii=False)) + '\n')


def main():

    os.chdir(IN_DIR)
    
    #read_in_taxonomy(WRITE=True)

    sizeN = 300
    top_communities = read_in_communities(sizeN)


    f_out_name = "taxonomy_summary_of_" + str(sizeN) + ".json"

    print len(top_communities), "top communities found"

    with codecs.open(f_out_name,'a', encoding='utf8') as f: 
        for community in top_communities:
            read_save_taxonomy(str(community), top_communities[community], WRITE=True, f=f)
    

main()
