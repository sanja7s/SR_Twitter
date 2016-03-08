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

def read_user_IDs():

    user_ids = defaultdict(str)

    with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_ids[user] = user_id

    return user_ids


def read_save_taxonomy(users="ALL", user_list=None, WRITE=False,TOP_N = 20):

    docSentiment_sum = defaultdict(int) 
    taxonomies_sum = defaultdict(int) 

    user_ids = read_user_IDs()

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
                try:
                    if el["confident"] == "no":
                        continue
                except: KeyError
                taxonomy_tree7s = el["label"]
                taxonomy_tree = taxonomy_tree7s.split("/")
                taxonomy_tree.pop(0)
                levels = len(taxonomy_tree)

                s = taxonomies_sum
                """
                # go until the last element; on the last, we will not create a dict NONO
                for tax_class in taxonomy_tree:
                    #print tax_class
                    if tax_class not in s.keys():
                        s[tax_class] = defaultdict(int)
                        #print taxonomies_sum
                        #return
                    s = s[tax_class]
                #last_tax_class = taxonomy_tree[levels-1]
                #s = s[last_tax_class]
                """
                if taxonomy_tree7s not in s.keys():
                    s[taxonomy_tree7s] = defaultdict(int)
                s = s[taxonomy_tree7s]


                old_score = s["size"]
                #old_cnt = s[tax_class][1]
                #old_sent = s[tax_class][2]
                new_score = old_score + float(el["score"])
                s["size"] = new_score
               
                if sentiment <> "neutral":
                    old_sent = s["sentiment"]
                    new_sent = old_sent + float(docSentiment["score"])
                    s["sentiment"] = new_sent

                    if sentiment == "positive":
                        pos_sent = s["pos_sent"]
                        pos_cnt = s["pos_sent_cnt"]
                        pos_sent = pos_sent + float(docSentiment["score"])
                        pos_cnt = pos_cnt + 1
                        s["pos_sent"] = pos_sent
                        s["pos_sent_cnt"] = pos_cnt
                    elif sentiment == "negative":
                        neg_sent = s["neg_sent"]
                        neg_cnt = s["neg_sent_cnt"]
                        neg_sent = neg_sent + float(docSentiment["score"])
                        neg_cnt = neg_cnt + 1
                        s["neg_sent"] = neg_sent
                        s["neg_sent_cnt"] = neg_cnt

            cnt += 1


        com_size = cnt

        N = cnt
     
        print cnt        
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "Total Sentiments found ", len(docSentiment_sum)

         
        sorted_taxonomies_by_neg_sent =  OrderedDict(sorted(taxonomies_sum.items(), key = lambda x: x[1]["sentiment"]))
        sorted_taxonomies_by_pos_sent =  OrderedDict(sorted(taxonomies_sum.items(), key = lambda x: x[1]["sentiment"], reverse = True))

        print_top_sent = 20
        i = 0
        for top_taxonomy in sorted_taxonomies_by_neg_sent:
            print top_taxonomy, "\t" ,sorted_taxonomies_by_neg_sent[top_taxonomy]["size"], "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["sentiment"], \
             "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["neg_sent"], "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["neg_sent_cnt"], \
             "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["pos_sent"], "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["pos_sent_cnt"]

            i += 1
            if i == print_top_sent:
                break
        print
        print
        i = 0
        for top_taxonomy in sorted_taxonomies_by_pos_sent:
            print top_taxonomy, "\t", sorted_taxonomies_by_pos_sent[top_taxonomy]["size"], "\t", sorted_taxonomies_by_pos_sent[top_taxonomy]["sentiment"], \
            "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["pos_sent"], "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["pos_sent_cnt"], \
             "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["neg_sent"], "\t", sorted_taxonomies_by_neg_sent[top_taxonomy]["neg_sent_cnt"]
            i += 1
            if i == print_top_sent:
                break


        if WRITE:
            f_out_name = "ALL/taxon_ALL.json"

            #taxonomies_out7s = recursive_writeable_json_from_dict(taxonomies_sum)
            print len(taxonomies_sum), type(taxonomies_sum)

            #for el in taxonomies_sum.items():
            #    print el

            taxonomies_out7s = recursive_writeable_json_from_dict(taxonomies_sum, "thing")
            print len(taxonomies_out7s), type(taxonomies_out7s)
 

            with codecs.open(f_out_name,'w', encoding='utf8') as f: 
                f.write("{ \"name\": \"thing\", \n \"children\": \n ")
                f.write(unicode(json.dumps(taxonomies_out7s, ensure_ascii=False)) + '\n')
                f.write("\n }")


def recursive_writeable_json_from_dict(d, dname):

    # stop criteria: len(d) == 1 means this is a leaf 
    # (should not allow here to arrive, for example { "size": 1.381699 }  )
    # only, for example { "poetry": { "size": 1.381699 } }
    if len(d) == 1:
        s = {}
        #print d, d.items()[0][1], d.items()[0][0]
        s["size"] = d.items()[0][1]["size"]
        s["name"] = d.items()[0][0]
        #print s["name"]
        return s
    # recursive criteria satisfied: create a new dict
    # add me my children, since I have
    #s = {}
    #s["children"] = []
    s = []
    for child_k in d.keys():
        if child_k == "size":
            if d[child_k] <> 0:
            #s["size"] = d[child_k]
                s.append({"size":d[child_k], "name":dname})
        else:
            child_el = d[child_k]
            ss = {"name": child_k}
            try:
                ss["size"] = child_el["size"]
            except: KeyError
            # this is a check to avoid passing { "size": 1.381699 } 
            #if child_el.items()[0][0] == "size" and len(child_el) == 1:
            #    s["children"].append()
            #    continue
            #print child_el
            #if len(child_el) > 1: 
                #ss["children"] = recursive_writeable_json_from_dict(child_el)
            if child_el.items()[0][0] == "size" and len(child_el) == 1:
                #s["children"].append(ss)
                s.append(ss)
                continue
            ss["children"] = recursive_writeable_json_from_dict(child_el, child_k)
            #s["children"].append(ss)
            s.append(ss)

    return s

def main():

    os.chdir(IN_DIR)

    read_save_taxonomy(WRITE=False)
    

main()
