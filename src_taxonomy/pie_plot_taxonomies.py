#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    plot the pie plots of the top concepts, entities, taxonomies etc. per community and for the whole dataset
    also output the stats for the top keywords, concepts, entities and for the sentiment per community (and the whole dataset)
'''
from __future__ import unicode_literals
#
import codecs
from collections import defaultdict, OrderedDict
import json
import glob, os
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys

font = {'family' : 'sans-serif',
        'variant' : 'normal',
        'weight' : 'light',
        'size'   : 14}

matplotlib.rc('font', **font)


#ARG = "SR"
ARG = "mention"
#ARG = "ment_SR"

f_in = "tweets_taxonomy_clean.JSON"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats/"
spec_users = ARG + "/communitiesMent.txt"
#spec_users =  ARG + "/communitiesSR_0.2.txt"
#spec_users = ARG + "/communitiesMent_SR.txt"

#TOP_GROUP = "reciprocal/"
#TOP_GROUP = "hubs_SR_0.9/"
#DIR_top_users = "TOP_users/" + str(TOP_GROUP)
#PREFIX = "100_top_"

#DIR_single_users = "pie_plots"

##################################################
# read in a map for the twitter username --> id
##################################################
def read_user_IDs():

    user_ids = defaultdict(str)

    with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_ids[user] = user_id

    return user_ids

##################################################
# read in the users (top in something)
##################################################
def read_TOP_users():

    user_ids = defaultdict(str)

    for top_users_file in os.listdir(DIR_top_users):
        if not top_users_file.startswith(PREFIX):
            continue
        with codecs.open(os.path.join(DIR_top_users, top_users_file),'r', encoding='utf8') as f:
            user_ids[top_users_file] = defaultdict(int)
            for line in f:
                line = line.split()
                user_id = line[0]
                user_ids[top_users_file][user_id] = 1

    return user_ids

####################################################################################################
# return top communities larger than sizeN, as many as there are of that size
# in a form of a dictionary: {community_id: defaultdict{id_usr1:1, id_usr2:1, ...}}
# and also return another dict, as a map (res3) to tell us the community id of a user
# and finally the whole set of communities (not limited in size) 
# and a similar map in res4
####################################################################################################
def read_in_communities(sizeN=300):

    res = defaultdict(int)
    res7s = defaultdict(int)
    res3 = defaultdict(int)
    res3 = defaultdict(lambda: -1, res3)
    res4 = defaultdict(int)
    #res4 = defaultdict(lambda: -1, res4)

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
        for usr in res[com]:
            res4[usr] = com

    for com in res7s:
        for usr in res7s[com]:
            res3[usr] = com

    return res7s, res3, res, res4

####################################################################################################
# in order to calculate TF-IDF for concepts, keywords and entities, we treat communities as documents
# here we extract document frequency for each of them (a one pass through the taxonomy dataset)
####################################################################################################
def community_IDFs(user_com):

    # resulting dictionaries in which the needed counts for com_IDFs are collected
    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    #
    taxonomies_sum = defaultdict(int)
    # holds all the user ids (username --> user_id, map)
    user_ids = read_user_IDs()

    cnt = 0
    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                user_name = line["_id"]
                user_id = user_ids[user_name]
                # so here we assign the COM of that user
                COM = user_com[user_id]
                taxonomy_all = line["taxonomy"]
                keywords = taxonomy_all["keywords"]
                entities = taxonomy_all["entities"]
                concepts = taxonomy_all["concepts"] 
                #
                taxonomy = taxonomy_all["taxonomy"]
                # this counts how many user we have analyzed
                cnt += 1
            except KeyError:
                #print line7s
                # we don't print since it is tested, there some 10% users for whom
                # the taxonomy was not successfuly downloaded and they would be listed here
                continue
            
            for el in keywords:
                category = el["text"]
                # if we first time encounter this keyword, add a list for it in the result
                if not category in keywords_sum:
                    keywords_sum[category] = []
                # we just put in a list all the recorded communities where this is found
                keywords_sum[category].append(COM)

            for el in entities:
                entity = el["text"]
                # if we first time encounter this entity, add a list for it in the result
                if not entity in entities_sum:
                    entities_sum[entity] = []
                # we just put in a list all the recorded communities where this is found
                entities_sum[entity].append(COM)

            for el in concepts:
                concept = el["text"]
                if concept in ['Trigraph', 'Gh', 'trigraph']:
                    continue
                # if we first time encounter this concept, add a list for it in the result
                if not concept in concepts_sum:
                    concepts_sum[concept] = []
                # we just put in a list all the recorded communities where this is found
                concepts_sum[concept].append(COM)

            for el in taxonomy:
                taxonomy_tree = el["label"]
                taxon = taxonomy_tree
                # if we first time encounter this taxon, add a list for it in the result
                if not taxon in taxonomies_sum:
                    taxonomies_sum[taxon] = []
                taxonomies_sum[taxon].append(COM)


        # now we count for each keyword, entitiy or concept in how many distinct communities they were recorded
        keywords_res = defaultdict(int)
        entities_res = defaultdict(int)
        concepts_res = defaultdict(int)
        #
        taxonomies_res = defaultdict(int)

        for el in keywords_sum:
            keywords_res[el] = len(set(keywords_sum[el]))

        for el in entities_sum:
            entities_res[el] = len(set(entities_sum[el]))

        for el in concepts_sum:
            concepts_res[el] = len(set(concepts_sum[el]))

        for el in taxonomies_sum:
            taxonomies_res[el] = len(set(taxonomies_sum[el]))

    return keywords_res, entities_res, concepts_res, taxonomies_res

##################################################
# the core function
##################################################
"""
    here, the options are to visualize the taxonomy for the whole dataset (COM="ALL")
    and to visualize for different communities (COM="COM") that are read in through read_in_communities()
    in the case of communities, this functions is invoked once per each community
    -- user_list holds the ids of the users in one community
    -- TOP_N holds the number of top concepts, keywords and entities that we want to visualize and record
    -- user_com holds a map for user_id --> com_id
    -- N_COM holds the total number of communities found (changes depending on the community detection algorithm)
"""
def visualize_taxonomy_pies(COM="ALL", user_list=None, TOP_N=10, user_com=None, N_COM=0):

    # resulting dictionaries in which the counts and tfidf relevance are collected
    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    taxonomies_sum = defaultdict(int) 
    #
    docSentiment_sum = defaultdict(int)
    # holds all the user ids
    user_ids = read_user_IDs()

    cnt = 0
    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                # if dealing with a community, check the user membership
                if COM <> "ALL":
                    user_name = line["_id"]
                    user_id = user_ids[user_name]
                    if user_list[user_id] == 0:
                        continue
                # if dealing with ALL, take all the users
                taxonomy_all = line["taxonomy"]
                keywords = taxonomy_all["keywords"]
                entities = taxonomy_all["entities"]
                concepts = taxonomy_all["concepts"] 
                taxonomy = taxonomy_all["taxonomy"] 
                #
                docSentiment = taxonomy_all["docSentiment"] 
                # this counts how many user we have analyzed
                cnt += 1
            except KeyError:
                #print line7s
                # we don't print since it is tested, there some 10% users for whom
                # the taxonomy was not successfuly downloaded and they would be listed here
                continue
            
            for el in keywords:
                category = el["text"]
                # if we first time encounter this keyword, add a dict for it in the result
                if not category in keywords_sum:
                    keywords_sum[category] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = keywords_sum[category][0]
                old_cnt = keywords_sum[category][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                keywords_sum[category] = (new_relev, new_cnt)

            for el in entities:
                entity = el["text"]
                if entity in ['#', '#MentionTo', 'twitter', 'Twitter']:
                    continue
                entity = entity.lower()
                # if we first time encounter this entity, add a dict for it in the result
                if not entity in entities_sum:
                    entities_sum[entity] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = entities_sum[entity][0]
                old_cnt = entities_sum[entity][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                entities_sum[entity] = (new_relev, new_cnt, el["type"])

            for el in concepts:
                concept = el["text"]
                if concept in ['Trigraph', 'Gh', 'trigraph']:
                    continue
                # if we first time encounter this concept, add a dict for it in the result
                if not concept in concepts_sum:
                    concepts_sum[concept] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = concepts_sum[concept][0]
                old_cnt = concepts_sum[concept][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                concepts_sum[concept] = (new_relev, new_cnt)

            # a bit different procedure for extracting the sentiment
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
                taxon = taxonomy_tree
                if not taxon in taxonomies_sum:
                    taxonomies_sum[taxon] = defaultdict(int)
                old_score = taxonomies_sum[taxon][0]
                old_cnt = taxonomies_sum[taxon][1]
                new_score = old_score + float(el["score"])
                new_cnt = old_cnt + 1
                taxonomies_sum[taxon] = (new_score, new_cnt)

        com_size = cnt
        # THIS IS A CONSTANT, because we know how many users there are in total after we did one ALL run
        N = 27665
        print "*** The community %s ***" % COM
        print "Analyzed %d users out of total %d users " % (com_size, N)
        try:
            pos_users = docSentiment_sum["positive"][1]
            pos_score = docSentiment_sum["positive"][0]
        except TypeError:
            pos_users = 0
            pos_score = 0.0
        try:
            neg_users = docSentiment_sum["negative"][1]
            neg_score = docSentiment_sum["negative"][0]
        except TypeError:
            neg_users = 0
            neg_score = 0.0
        try:
            neu_users = docSentiment_sum["neutral"]
        except TypeError:
            neu_users = 0

        
        
        print "___________________"
        print "Sentiment stats: positive %d users; negative %d users; and neutral %d " % (pos_users, neg_users, neu_users)
        print "Sentiment score: positive %f ; negative %f; and the sum sentiment %f " % (pos_score, neg_score, pos_score + neg_score)
        print "Overall positive sentiment pct is %f " % (float(pos_users)/com_size)
        print "___________________"
        print "Total keywords found ", len(keywords_sum)
        print "Total entities found ", len(entities_sum)
        print "Total concepts found ", len(concepts_sum)
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "___________________"

        # if we deal with communities, then the number of documents is the total number of communities
        # and IDF values are found with help of the function community_IDFs
        if COM <> 'ALL':
            keywords_res, entities_res, concepts_res, taxonomies_res = community_IDFs(user_com)
            N = N_COM

        #####################
        ## STARTS plotting ##
        #####################
        if COM == 'ALL':
            os.chdir('ALL/pie_plots')
        else:
            #os.chdir(ARG + '/pie_plots')
            #os.chdir(ARG + '/pie_plots_0.2')
            os.chdir(ARG + '/pie_plots_PRETTY7s')
        
        #####################
        ##    KEYWORDS     ##
        #####################
        for kw in keywords_sum:
            tot_relev = keywords_sum[kw][0]
            tot_cnt = keywords_sum[kw][1]
            # v1 for ALL
            if COM == 'ALL':
                inv_kw_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
                tfidf = float(tot_relev * math.log(1.0 + inv_kw_fq))
            else:
                # v2 THIS ONE IS USED for COMMUNITIES
                com_N = keywords_res[kw]
                inv_fq = 0 if com_N == 0 else N/float(com_N)
                tfidf = float(tot_cnt * math.log(1.0 + inv_fq))
            keywords_sum[kw] = (tot_relev, tot_cnt, tfidf)
        
        print
        print "Keywords (ordered by TF-IDF): [relevance, count, TF-IDF]"
        ord_keywords_sum2 = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][2], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_keywords_sum2:
            print el.encode('utf-8'), ord_keywords_sum2[el]
            labels[i] = el
            sizes[i] = float(ord_keywords_sum2[el][2])
            sizes_tot[i] = float(ord_keywords_sum2[el][0])
            i += 1
            if i == TOP_N:
                break
        plot_pie(labels, sizes, "kw_tfid_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        plot_pie(labels, sizes_tot, "kw_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        print

        #####################
        ##    ENTITIES     ##
        #####################
        for en in entities_sum:
            tot_relev = entities_sum[en][0]
            tot_cnt = entities_sum[en][1]
            # v1 for ALL
            if COM == 'ALL':
                inv_ent_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
                tfidf = tot_relev * math.log(1.0 + inv_ent_fq)
            else:
                # v2 THIS IS USED for COMMUNITIES
                com_N = entities_res[en]
                inv_fq = 0 if com_N == 0 else N/float(com_N)
                tfidf = float(tot_cnt * math.log(1.0 + inv_fq))
            entities_sum[en] = (tot_relev, tot_cnt, tfidf)  

        print "Entities (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_entities_sum2 = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1][2], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_entities_sum2:
            print el.encode('utf-8'), ord_entities_sum2[el]
            labels[i] = el
            #print labels
            sizes_tot[i] = float(ord_entities_sum2[el][0])
            sizes[i] = float(ord_entities_sum2[el][2])
            i += 1
            if i == TOP_N:
                break
        plot_pie(labels, sizes, "ent_tfidf_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        plot_pie(labels, sizes_tot, "ent_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        print

        #####################
        ##    CONCEPTS     ##
        #####################
        for conc in concepts_sum:
            tot_relev = concepts_sum[conc][0]
            tot_cnt = concepts_sum[conc][1]
            # v1 COM = ALL
            if COM == 'ALL':
                inv_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
                tfidf = float(tot_relev * math.log(1.0 + inv_fq))
            else:
                # v2 THIS IS USED for COMMUNITIES
                com_N = concepts_res[conc]
                inv_fq = 0 if com_N == 0 else N/float(com_N)
                tfidf = float(tot_cnt * math.log(1.0 + inv_fq))
            concepts_sum[conc] = (tot_relev, tot_cnt, tfidf)

        print "Concepts (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_concepts_sum = OrderedDict(sorted(concepts_sum.items(), key=lambda x: x[1][2], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_concepts_sum:
            print el.encode('utf-8'), ord_concepts_sum[el]
            labels[i] = el
            sizes[i] = float(ord_concepts_sum[el][2])
            sizes_tot[i] = float(ord_concepts_sum[el][0])
            i += 1
            if i == TOP_N:
                break
        plot_pie(labels, sizes, "concept_tfidf_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        plot_pie(labels, sizes_tot, "concept_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        print

        #####################
        ##   TAXONOMIES    ##
        #####################
        for taxon in taxonomies_sum:
            tot_score = taxonomies_sum[taxon][0]
            tot_cnt = taxonomies_sum[taxon][1]
            # v1 COM = ALL
            if COM == 'ALL':
                inv_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
                tfidf = float(tot_score * math.log(1.0 + inv_fq))
            else:
                # v2 THIS IS USED for COMMUNITIES
                com_N = taxonomies_res[taxon]
                inv_fq = 0 if com_N == 0 else N/float(com_N)
                tfidf = float(tot_cnt * math.log(1.0 + inv_fq))
            taxonomies_sum[taxon] = (tot_score, tot_cnt, tfidf)


        print "Taxonomies (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_taxonomies_sum = OrderedDict(sorted(taxonomies_sum.items(), key=lambda x: x[1][2], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_taxonomies_sum:
            print el.encode('utf-8'), ord_taxonomies_sum[el]
            labels[i] = el
            sizes[i] = float(ord_taxonomies_sum[el][2])
            sizes_tot[i] = float(ord_taxonomies_sum[el][0])
            i += 1
            if i == TOP_N:
                break
        plot_pie(labels, sizes, "taxon_tfidf_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        plot_pie(labels, sizes_tot, "taxon_com_" + str(COM) + "_top_" + str(TOP_N) + ".eps")
        plt.clf()
        print


        os.chdir("../../")



##################################################
# the core function for the user lists (TOP etc.)
##################################################
"""
    here, the options are to visualize the taxonomy for the whole dataset (COM="ALL")
    and to visualize for different communities (COM="COM") that are read in through read_in_communities()
    in the case of communities, this functions is invoked once per each community
    -- user_list holds the ids of the users in one community
    -- TOP_N holds the number of top concepts, keywords and entities that we want to visualize and record
    -- user_com holds a map for user_id --> com_id
    -- N_COM holds the total number of communities found (changes depending on the community detection algorithm)
"""
def visualize_taxonomy_pies_user_list(user_ids, COM, user_list=None, TOP_N=20):

    # resulting dictionaries in which the counts and tfidf relevance are collected
    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    taxonomies_sum = defaultdict(int) 
    #
    docSentiment_sum = defaultdict(int)

    cnt = 0
    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                user_name = line["_id"]
                user_id = user_ids[user_name]
                if user_list[user_id] == 0:
                    continue
                # if dealing with ALL, take all the users
                taxonomy_all = line["taxonomy"]
                keywords = taxonomy_all["keywords"]
                entities = taxonomy_all["entities"]
                concepts = taxonomy_all["concepts"] 
                taxonomy = taxonomy_all["taxonomy"] 
                #
                docSentiment = taxonomy_all["docSentiment"] 
                # this counts how many user we have analyzed
                cnt += 1
            except KeyError:
                #print line7s
                # we don't print since it is tested, there some 10% users for whom
                # the taxonomy was not successfuly downloaded and they would be listed here
                continue
            
            for el in keywords:
                category = el["text"]
                # if we first time encounter this keyword, add a dict for it in the result
                if not category in keywords_sum:
                    keywords_sum[category] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = keywords_sum[category][0]
                old_cnt = keywords_sum[category][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                keywords_sum[category] = (new_relev, new_cnt)

            for el in entities:
                entity = el["text"]
                if entity in ['#', '#MentionTo', 'twitter', 'Twitter']:
                    continue
                # if we first time encounter this entity, add a dict for it in the result
                if not entity in entities_sum:
                    entities_sum[entity] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = entities_sum[entity][0]
                old_cnt = entities_sum[entity][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                entities_sum[entity] = (new_relev, new_cnt, el["type"])

            for el in concepts:
                concept = el["text"]
                if concept in ['Trigraph', 'Gh', 'trigraph']:
                    continue
                # if we first time encounter this concept, add a dict for it in the result
                if not concept in concepts_sum:
                    concepts_sum[concept] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = concepts_sum[concept][0]
                old_cnt = concepts_sum[concept][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                concepts_sum[concept] = (new_relev, new_cnt)

            # a bit different procedure for extracting the sentiment
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
                taxon = taxonomy_tree
                if not taxon in taxonomies_sum:
                    taxonomies_sum[taxon] = defaultdict(int)
                old_score = taxonomies_sum[taxon][0]
                old_cnt = taxonomies_sum[taxon][1]
                new_score = old_score + float(el["score"])
                new_cnt = old_cnt + 1
                taxonomies_sum[taxon] = (new_score, new_cnt)

        com_size = cnt
        # THIS IS A CONSTANT, because we know how many users there are in total after we did one ALL run
        N = 27665
        print "*** The user list %s ***" % COM
        print "Analyzed %d users out of total %d users " % (com_size, N)
        try:
            pos_users = docSentiment_sum["positive"][1]
            pos_score = docSentiment_sum["positive"][0]
        except TypeError:
            pos_users = 0
            pos_score = 0
        try:
            neg_users = docSentiment_sum["negative"][1]
            neg_score = docSentiment_sum["negative"][0]
        except TypeError:
            neg_users = 0
            neg_score = 0
        try:
            neu_users = docSentiment_sum["neutral"]
        except TypeError:
            neu_users = 0

        print "___________________"
        print "Sentiment stats: positive %d users; negative %d users; and neutral %d " % (pos_users, neg_users, neu_users)
        print "Sentiment score: positive %f ; negative %f; and the sum sentiment %f " % (pos_score, neg_score, pos_score + neg_score)
        print "Overall positive sentiment pct is %f " % (float(pos_users)/com_size)
        print "___________________"
        print "Total keywords found ", len(keywords_sum)
        print "Total entities found ", len(entities_sum)
        print "Total concepts found ", len(concepts_sum)
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "___________________"

        #####################
        ## STARTS plotting ##
        #####################
        os.chdir(DIR_top_users)
        #####################
        ##    KEYWORDS     ##
        #####################
        for kw in keywords_sum:
            tot_relev = keywords_sum[kw][0]
            tot_cnt = keywords_sum[kw][1]
            inv_kw_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
            tfidf = float(tot_relev * math.log(1.0 + inv_kw_fq))
            keywords_sum[kw] = (tot_relev, tot_cnt, tfidf)
        
        print
        print "Keywords (ordered by TF-IDF): [relevance, count, TF-IDF]"
        ord_keywords_sum2 = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_keywords_sum2:
            print el.encode('utf-8'), ord_keywords_sum2[el]
            labels[i] = el
            sizes[i] = float(ord_keywords_sum2[el][2])
            sizes_tot[i] = float(ord_keywords_sum2[el][0])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes, "kw_tfid_com_" + str(COM) + ".eps")
        #plt.clf()
        plot_pie(labels, sizes_tot, "kw_com_" + str(COM) + ".eps")
        plt.clf()
        print

        #####################
        ##    ENTITIES     ##
        #####################
        for en in entities_sum:
            tot_relev = entities_sum[en][0]
            tot_cnt = entities_sum[en][1]
            inv_ent_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
            tfidf = tot_relev * math.log(1.0 + inv_ent_fq)
            entities_sum[en] = (tot_relev, tot_cnt, tfidf)  

        print "Entities (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_entities_sum2 = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_entities_sum2:
            print el.encode('utf-8'), ord_entities_sum2[el]
            labels[i] = el
            #print labels
            sizes_tot[i] = float(ord_entities_sum2[el][0])
            sizes[i] = float(ord_entities_sum2[el][2])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes, "ent_tfidf_com_" + str(COM) +  ".eps")
        #plt.clf()
        plot_pie(labels, sizes_tot, "ent_com_" + str(COM) + ".eps")
        plt.clf()
        print

        #####################
        ##    CONCEPTS     ##
        #####################
        for conc in concepts_sum:
            tot_relev = concepts_sum[conc][0]
            tot_cnt = concepts_sum[conc][1]
            inv_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
            tfidf = float(tot_relev * math.log(1.0 + inv_fq))
            concepts_sum[conc] = (tot_relev, tot_cnt, tfidf)

        print "Concepts (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_concepts_sum = OrderedDict(sorted(concepts_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_concepts_sum:
            print el.encode('utf-8'), ord_concepts_sum[el]
            labels[i] = el
            sizes[i] = float(ord_concepts_sum[el][2])
            sizes_tot[i] = float(ord_concepts_sum[el][0])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes, "concept_tfidf_" + str(COM) + ".eps")
        #plt.clf()
        plot_pie(labels, sizes_tot, "concept_" + str(COM) + ".eps")
        plt.clf()
        print

        #####################
        ##   TAXONOMIES    ##
        #####################
        for taxon in taxonomies_sum:
            tot_score = taxonomies_sum[taxon][0]
            tot_cnt = taxonomies_sum[taxon][1]
            inv_fq = 0 if tot_cnt == 0 else N/float(tot_cnt)
            tfidf = float(tot_score * math.log(1.0 + inv_fq))
            taxonomies_sum[taxon] = (tot_score, tot_cnt, tfidf)


        print "Taxonomies (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_taxonomies_sum = OrderedDict(sorted(taxonomies_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_taxonomies_sum:
            print el.encode('utf-8'), ord_taxonomies_sum[el]
            labels[i] = el
            sizes[i] = float(ord_taxonomies_sum[el][2])
            sizes_tot[i] = float(ord_taxonomies_sum[el][0])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes, "taxon_tfidf_" + str(COM) + ".eps")
        #plt.clf()
        plot_pie(labels, sizes_tot, "taxon_" + str(COM) + ".eps")
        plt.clf()
        print

        os.chdir("../../")

def visualize_taxonomy_pies_single_user(user_ids, COM, user_list=None, TOP_N=20):

    # resulting dictionaries in which the counts and tfidf relevance are collected
    keywords_sum = defaultdict(int)
    entities_sum = defaultdict(int)
    concepts_sum = defaultdict(int)
    taxonomies_sum = defaultdict(int) 
    #
    docSentiment_sum = defaultdict(int)

    cnt = 0
    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        for line7s in input_file:
            try:
                line = json.loads(line7s)
                user_name = line["_id"]
                user_id = user_ids[user_name]
                if user_list[user_id] == 0:
                    continue
                # if dealing with ALL, take all the users
                taxonomy_all = line["taxonomy"]
                keywords = taxonomy_all["keywords"]
                entities = taxonomy_all["entities"]
                concepts = taxonomy_all["concepts"] 
                taxonomy = taxonomy_all["taxonomy"] 
                #
                docSentiment = taxonomy_all["docSentiment"] 
                # this counts how many user we have analyzed
                cnt += 1
            except KeyError:
                #print line7s
                # we don't print since it is tested, there some 10% users for whom
                # the taxonomy was not successfuly downloaded and they would be listed here
                continue
            
            for el in keywords:
                category = el["text"]
                # if we first time encounter this keyword, add a dict for it in the result
                if not category in keywords_sum:
                    keywords_sum[category] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = keywords_sum[category][0]
                old_cnt = keywords_sum[category][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                keywords_sum[category] = (new_relev, new_cnt)

            for el in entities:
                entity = el["text"]
                # if we first time encounter this entity, add a dict for it in the result
                if not entity in entities_sum:
                    entities_sum[entity] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = entities_sum[entity][0]
                old_cnt = entities_sum[entity][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                entities_sum[entity] = (new_relev, new_cnt, el["type"])

            for el in concepts:
                concept = el["text"]
                if concept in ['Trigraph', 'Gh', 'trigraph']:
                    continue
                # if we first time encounter this concept, add a dict for it in the result
                if not concept in concepts_sum:
                    concepts_sum[concept] = defaultdict(int)
                # we use this not so well coded part because tuples do not allow assignment
                old_relev = concepts_sum[concept][0]
                old_cnt = concepts_sum[concept][1]
                new_relev = old_relev + float(el["relevance"])
                new_cnt = old_cnt + 1
                concepts_sum[concept] = (new_relev, new_cnt)

            # a bit different procedure for extracting the sentiment
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
                taxon = taxonomy_tree
                if not taxon in taxonomies_sum:
                    taxonomies_sum[taxon] = defaultdict(int)
                old_score = taxonomies_sum[taxon][0]
                old_cnt = taxonomies_sum[taxon][1]
                new_score = old_score + float(el["score"])
                new_cnt = old_cnt + 1
                taxonomies_sum[taxon] = (new_score, new_cnt)

        com_size = cnt
        # THIS IS A CONSTANT, because we know how many users there are in total after we did one ALL run
        N = 27665
        print "*** The user %s ***" % COM
        print "Analyzed %d users out of total %d users " % (com_size, N)
        try:
            pos_users = docSentiment_sum["positive"][1]
            pos_score = docSentiment_sum["positive"][0]
        except TypeError:
            pos_users = 0
            pos_score = 0
        try:
            neg_users = docSentiment_sum["negative"][1]
            neg_score = docSentiment_sum["negative"][0]
        except TypeError:
            neg_users = 0
            neg_score = 0
        try:
            neu_users = docSentiment_sum["neutral"]
        except TypeError:
            neu_users = 0

        print "___________________"
        print "Sentiment stats: positive %d users; negative %d users; and neutral %d " % (pos_users, neg_users, neu_users)
        print "Sentiment score: positive %f ; negative %f; and the sum sentiment %f " % (pos_score, neg_score, pos_score + neg_score)
        print "Overall positive sentiment pct is %f " % (float(pos_users)/com_size)
        print "___________________"
        print "Total keywords found ", len(keywords_sum)
        print "Total entities found ", len(entities_sum)
        print "Total concepts found ", len(concepts_sum)
        print "Total taxonomies on different levels found ", len(taxonomies_sum)
        print "___________________"

        #####################
        ## STARTS plotting ##
        #####################
        os.chdir(DIR_single_users)
        #####################
        ##    KEYWORDS     ##
        #####################
        for kw in keywords_sum:
            tot_relev = keywords_sum[kw][0]
            tot_cnt = keywords_sum[kw][1]
            keywords_sum[kw] = (tot_relev, tot_cnt)
        
        print
        print "Keywords (ordered by TF-IDF): [relevance, count, TF-IDF]"
        ord_keywords_sum2 = OrderedDict(sorted(keywords_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_keywords_sum2:
            el_out =  el.encode('utf8', 'replace')
            print el_out.encode('utf-8'), ord_keywords_sum2[el]
            labels[i] = el
            sizes[i] = float(ord_keywords_sum2[el][1])
            sizes_tot[i] = float(ord_keywords_sum2[el][0])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes_tot, "kw_user_" + str(COM) + ".eps")
        #plt.clf()
        print

        #####################
        ##    ENTITIES     ##
        #####################
        for en in entities_sum:
            tot_relev = entities_sum[en][0]
            tot_cnt = entities_sum[en][1]
            entities_sum[en] = (tot_relev, tot_cnt)  

        print "Entities (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_entities_sum2 = OrderedDict(sorted(entities_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_entities_sum2:
            el_out =  el.encode('utf8', 'replace')
            print el_out.encode('utf-8'), ord_entities_sum2[el]
            labels[i] = el
            sizes_tot[i] = float(ord_entities_sum2[el][0])
            sizes[i] = float(ord_entities_sum2[el][1])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes_tot, "ent_user_" + str(COM) + ".eps")
        #plt.clf()
        print

        #####################
        ##    CONCEPTS     ##
        #####################
        for conc in concepts_sum:
            tot_relev = concepts_sum[conc][0]
            tot_cnt = concepts_sum[conc][1]
            concepts_sum[conc] = (tot_relev, tot_cnt)

        print "Concepts (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_concepts_sum = OrderedDict(sorted(concepts_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_concepts_sum:
            el_out =  el.encode('utf8', 'replace')
            print el_out.encode('utf-8'), ord_concepts_sum[el]
            labels[i] = el
            sizes[i] = float(ord_concepts_sum[el][1])
            sizes_tot[i] = float(ord_concepts_sum[el][0])
            i += 1
            if i == TOP_N:
                break

        #plot_pie(labels, sizes_tot, "concept_" + str(COM) + ".eps")
        #plt.clf()
        print

        #####################
        ##   TAXONOMIES    ##
        #####################
        for taxon in taxonomies_sum:
            tot_score = taxonomies_sum[taxon][0]
            tot_cnt = taxonomies_sum[taxon][1]
            taxonomies_sum[taxon] = (tot_score, tot_cnt)


        print "Taxonomies (sorted by TF-IDF): [relevance, count, TF-IDF]"
        ord_taxonomies_sum = OrderedDict(sorted(taxonomies_sum.items(), key=lambda x: x[1][0], reverse = True))
        labels = np.empty([TOP_N], dtype="<U26")
        sizes = np.empty([TOP_N], dtype=float)
        sizes_tot = np.empty([TOP_N], dtype=float)
        i = 0
        for el in ord_taxonomies_sum:
            el_out =  el.encode('utf8', 'replace')
            print el_out, ord_taxonomies_sum[el]
            labels[i] = el
            sizes[i] = float(ord_taxonomies_sum[el][1])
            sizes_tot[i] = float(ord_taxonomies_sum[el][0])
            i += 1
            if i == TOP_N:
                break
        #plot_pie(labels, sizes_tot, "taxon_" + str(COM) + ".eps")
        #plt.clf()
        print

        os.chdir("../")

def plot_pie(labels, sizes, f_pie_name):
    colors = ['yellowgreen', 'mediumpurple', 'lightskyblue', 'lightcoral', 'paleturquoise',
            'navy', 'mistyrose', 'mediumspringgreen', 'mediumaquamarine', 'limegreen',
            'gray', 'lavenderblush', 'lightgoldenrodyellow',  'lightgreen', 'lightsalmon' ] 
    ax = plt.subplot( 111 ) 
    print labels
    print sizes
    #explode = np.zeros(sizes.shape[0])    # proportion with which to offset each wedge
    ax.pie(sizes,              # data
            #explode=explode,    # offset parameters 
            labels=labels,      # slice labels
            colors=colors,      # array of colours
            autopct='%1.1f%%',  # print the values inside the wedges
            shadow=True,        # enable shadow
            startangle=70       # starting angle
            )
    #plt.axis('equal')
    wedges = [patch for patch in ax.patches if isinstance(patch, matplotlib.patches.Wedge)]
    for w in wedges:
        w.set_linewidth( 2 )
        w.set_edgecolor( 'cyan' )
    plt.savefig(f_pie_name)

def main_TOP_users():

    os.chdir(IN_DIR)
    user_ids = read_user_IDs()
    TOP_users_lists = read_TOP_users()

    for top_list in TOP_users_lists:
        sys.stdout = open(DIR_top_users + "STATS_" + top_list, 'w')
        visualize_taxonomy_pies_user_list(user_ids, top_list, user_list=TOP_users_lists[top_list])

def main_SINGLE_users(user):

    user_ids = read_user_IDs()
    sys.stdout = open('BUBBLE/opposite_sentiment/' + 'stats_' + str(user), 'w')
    visualize_taxonomy_pies_single_user(user_ids, str(user), user_list={str(user):1})


def main(COM='ALL'):

    os.chdir(IN_DIR)

    if COM == "ALL":
        sys.stdout = open('ALL/top_20_stats', 'w')
        visualize_taxonomy_pies("ALL")
    else:
        sizeN = 1
        sys.stdout = open(ARG + '/modular_com_taxon_stats' + str(sizeN), 'w')
        top_communities, com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)
        print len(top_communities), "top communities found of size ", str(sizeN)
        NALL = len(all_communities)
        print NALL, "all communities found"
        for community in top_communities:
            visualize_taxonomy_pies(str(community), user_list=top_communities[community], TOP_N=15, user_com=all_com_id_map, N_COM=NALL)

# other possible argument is 'COM' or any other string to print pies for the communities
# 'ALL' prints the pie stats for the whole dataset
# cannot call these at the same time, but in two python script calls

###############################################################################
#main('ALL')

# runme as 
# python pie_plot_taxonomies.py > "/home/sscepano/Projects7s/Twitter-workspace/DATA/taxonomy_stats/ALL/pie_plots/ALL_stats.txt"
###############################################################################


###############################################################################
main('COM')

# runme as
# python pie_plot_taxonomies.py > "/home/sscepano/Projects7s/Twitter-workspace/DATA/taxonomy_stats/SR/pie_plots_0.6/com_20_stats.txt"
# or
# python pie_plot_taxonomies.py > "/home/sscepano/Projects7s/Twitter-workspace/DATA/taxonomy_stats/SR_that_mention/pie_plots/com_20_stats.txt"
###############################################################################

###############################################################################
# I am a bit different 
###############################################################################
#main_TOP_users()
###############################################################################

#users = [1345,   26125, 6035,  12406, 13952,   19631, 24923,   26301, 10907, \
#       27318, 21405,   10725, 19966,   330, 15810, 22078, 14156,   23485, 890, 21148, 7513,    14191]

#users = [1345]

#os.chdir(IN_DIR)
#for user in users:
#   main_SINGLE_users(user)