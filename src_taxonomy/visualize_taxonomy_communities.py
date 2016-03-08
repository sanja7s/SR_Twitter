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
spec_users = "SR/communitiesSR_0.95.txt"

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
        print len(res[com])
        if len(res[com]) >= sizeN:
            res7s[com] = res[com]

    return res7s


def read_save_taxonomy(users="ALL", user_list=None, WRITE=False,TOP_N = 20):

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
                taxonomy_tree = el["label"]
                taxonomy_tree = taxonomy_tree.split("/")
                taxonomy_tree.pop(0)
                levels = len(taxonomy_tree)

                s = taxonomies_sum
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

                old_score = s["size"]
                #old_cnt = s[tax_class][1]
                #old_sent = s[tax_class][2]
                new_score = old_score + float(el["score"])
                s["size"] = new_score
                # this shows that it takes as confident only those above 0.4
                if float(el["score"]) < 0.4:
                    print float(el["score"])

            cnt += 1


        com_size = cnt

        N = cnt
     
        print cnt        
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "Total Sentiments found ", len(docSentiment_sum)

        print "Sentiment: [type, score, count, mixed_count]"
        i = 0
        for el in docSentiment_sum:
            print el, docSentiment_sum[el]
            i += 1
            if i == TOP_N:
                break
        print

        TOP_N = 100


        if WRITE:
            f_out_name = "SR/com_taxonomy/taxon_COM_" + str(users) + ".json"

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
    

    sizeN = 100
    top_communities = read_in_communities(sizeN)
    print len(top_communities), "top communities found"

    
    for community in top_communities:
        read_save_taxonomy(str(community), top_communities[community], WRITE=True)
    

main()
