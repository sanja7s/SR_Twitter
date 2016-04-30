#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    Given the taxonomy output from AlchemyAPI, for each level of taxonomies, extract the graph
    so that the taxons in this level are connected based on the number of users sharing these taxons 
    in their tweets
"""

import codecs
from collections import defaultdict, OrderedDict
import json
import re
import glob, os
import math
import itertools

f_in = "tweets_taxonomy_clean.JSON"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../DATA/taxonomy_stats"

def read_user_IDs():

    user_ids = defaultdict(str)

    with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_ids[user] = user_id

    return user_ids


def read_save_taxonomy_graph():

    docSentiment_sum = defaultdict(int) 
    taxonomies_sum = [defaultdict(int)]*5
    taxonomies_sum[0] = defaultdict(int)
    taxonomies_sum[1] = defaultdict(int)
    taxonomies_sum[2] = defaultdict(int)
    taxonomies_sum[3] = defaultdict(int)
    taxonomies_sum[4] = defaultdict(int)

    user_ids = read_user_IDs()

    cnt = 0

    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                """
                if users <> "ALL":
                    user_name = line["_id"]
                    user_id = user_ids[user_name]
                    if user_list[user_id] == 0:
                        continue 
                """
                taxonomy_all = line["taxonomy"]
                #keywords = taxonomy_all["keywords"]
                #entities = taxonomy_all["entities"]
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


            one_user_taxon = [defaultdict(int)]*5
            one_user_taxon[0] = []
            one_user_taxon[1] = []
            one_user_taxon[2] = []
            one_user_taxon[3] = []
            one_user_taxon[4] = []

            for el in taxonomy:
                try:
                    if el["confident"] == "no":
                        continue
                except: KeyError
                taxonomy_tree = el["label"]
                taxonomy_tree = taxonomy_tree.split("/")
                taxonomy_tree.pop(0)
                levels = len(taxonomy_tree)

                #print levels, taxonomy_tree

                

                for i in range(levels):
                    tax_class = taxonomy_tree[i]
                    #print tax_class
                    if tax_class not in one_user_taxon[i]:
                    	one_user_taxon[i].append(tax_class)


	        #print one_user_taxon

	        for i in range(5):
	        	level_i = len(one_user_taxon[i])
	        	#print level_i
	        	for id1 in range(level_i-1):
	        		for id2 in range(id1+1, level_i):
	        			el1 = one_user_taxon[i][id1]
	        			el2 = one_user_taxon[i][id2]
	        			if el1 == el2:
	        				print id1, el1, id2, el2 #, taxonomy_all
	        			key_sorted = tuple(sorted((el1,el2)))
	        			taxonomies_sum[i][key_sorted] += 1

	        #print taxonomies_sum


            #if cnt == 2:
            #	return

            cnt += 1


        com_size = cnt

        N = cnt
     
        print cnt        
        print "Total taxonomy edges on different levels found ", len(taxonomies_sum[0]), len(taxonomies_sum[1]),len(taxonomies_sum[2]), len(taxonomies_sum[3]), len(taxonomies_sum[4])
        print "Total Sentiments found ", len(docSentiment_sum)



    	for i in range(5):
        	f_out_name = "graph/level_" + str(i) + ".tab"

        
       		print len(taxonomies_sum[i]), type(taxonomies_sum[i])

       		taxonomies_sum_i = OrderedDict(sorted(taxonomies_sum[i].items(), key=lambda x: x[1], reverse = True))

       		with codecs.open(f_out_name,'w', encoding='utf8') as f: 
       			for el in taxonomies_sum_i:
       				f.write(str(el[0]) + "\t"  + str(el[1]) + "\t" +  str(taxonomies_sum[i][el])   + "\n ")


def main():

    os.chdir(IN_DIR)
    read_save_taxonomy_graph()
    

main()
