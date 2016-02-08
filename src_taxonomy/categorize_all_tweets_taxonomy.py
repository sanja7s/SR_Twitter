#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
from collections import defaultdict, OrderedDict
import json
import re
import glob, os

f_in = "tweets_taxonomy_clean.JSON"
f_in_users = "user_IDs.dat"
f_out = "summary_taxonomy.JSON"
IN_DIR = "../DATA/taxonomy_stats/"


def read_in_taxonomy():

    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    docSentiment_sum = defaultdict(int) 
    taxonomies_sum = defaultdict(int) 

    cnt = 0

    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
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
                    new_score = old_score + float(el["score"])
                    new_cnt = old_cnt + 1
                    level = levels - taxon_level
                    taxonomies_sum[taxon] = (new_score, new_cnt, level)

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

            for el in entities:
                entity = el["text"]
                if not entity in entities_sum:
                    entities_sum[entity] = defaultdict(int)
                old_relev = entities_sum[entity][0]
                old_cnt = entities_sum[entity][1]
                old_internal_count = entities_sum[entity][2]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                new_internal_count = old_internal_count + int(el["count"])
                entities_sum[entity] = (new_relev, new_cnt, new_internal_count, el["type"])


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
        
        print cnt        
        print "Total keywords found ", len(keywords_sum)
        print "Total taxonomies on different  levels found ", len(taxonomies_sum)
        print "Total Sentiments found ", len(docSentiment)
        print "Total entities found ", len(entities_sum)
        print "Total concepts found ", len(concepts_sum)

        TOP_N = 20

        print
        print "Keywods: [relevance, count]"
        ord_keywords_sum = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_keywords_sum:
            print el, ord_keywords_sum[el]
            i += 1
            if i == TOP_N:
                break
        print
        print "Taxonomies: [relevance, count, level]"
        ord_taxonomies_sum = OrderedDict(sorted(taxonomies_sum.items(), key=lambda x: x[1][1], reverse = True))
        i = 0
        for el in ord_taxonomies_sum:
            print el, ord_taxonomies_sum[el]
            i += 1
            if i == TOP_N:
                break
        print
        print "Sentiment: [type, score, count, mixed_count]"
        ord_docSentiment_sum = OrderedDict(sorted(docSentiment_sum.items(), key=lambda x: x[1], reverse = True))
        i = 0
        for el in docSentiment_sum:
            print el, docSentiment_sum[el]
            i += 1
            if i == TOP_N:
                break
        print
        print "Entities: [relevance, cnt, internal_cnt]"
        ord_entities_sum = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1], reverse = True))
        i = 0
        for el in ord_entities_sum:
            print el, ord_entities_sum[el]
            i += 1
            if i == TOP_N:
                break
        print
        print "Concepts: [relevance, count]"
        ord_concepts_sum = OrderedDict(sorted(concepts_sum.items(), key=lambda x: x[1], reverse = True))
        i = 0
        for el in ord_concepts_sum:
            print el, ord_concepts_sum[el]
            i += 1
            if i == TOP_N:
                break



def main():

    os.chdir(IN_DIR)
    read_in_taxonomy()

main()
