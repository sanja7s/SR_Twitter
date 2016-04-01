#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	Let's extract main concepts (CVs) in each community
	or for a given TOP USER list
	Find their frequency histogram
"""
# for reading json files with possible unicode chars
import codecs
from collections import defaultdict, OrderedDict
import json
import glob, os
import math
import numpy as np
import matplotlib.pyplot as plt


# here we have the CVs per user
f_in = "CVs_usrs.json"
# the id map we defined for the Twitter usernames
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/CV"

#########################################################
# TOP USER lists
#########################################################
TOP_GROUP = "hubs_SR_0.6/"
DIR_top_users = "TOP_users/" + str(TOP_GROUP)
PREFIX = "100_top_"

#########################################################
# SR
#########################################################
#X = "0.8"
#working_subfolder = "SR_commmunities/"
# the communities we analyze (from the SR graph)
#spec_users = working_subfolder + "communitiesSR_" + str(X) + ".txt"
#########################################################
#########################################################
# Mention
#########################################################
X = "" #dummy
working_subfolder = "mention_communities/"
# the communities we analyze (from the mention graph)
spec_users = working_subfolder + "communitiesMent" + str(X) + ".txt"
#########################################################

f_in_article_IDs = "articles_selected"
#
# read in all article IDs
#
def read_article_IDs(): #TODO fin

	article_IDs = defaultdict(int)
	cnt = 0

	with open(f_in_article_IDs) as f:
		for line in f:
			line = line[:-1].split('\t')
			aid = line[0]
			aname = line[1]
			article_IDs[aid] = aname
			#if cnt % 10000 == 0:
				#print line
			cnt += 1

	return article_IDs


#
# all the user ids (id map)
#
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

# to return top sizeN communities, as many as there are
# in a form of a dictionary: {community_id: defaultdict{id_usr1:1, id_usr2:1, ...}}
# and also another dict, as a map (res3) to tell us the community id of a user
# and finally the whole set of communities (not limited in size) and similar map in res4
def read_in_communities(sizeN=300):

	res = defaultdict(int)
	res7s = defaultdict(int)
	res3 = defaultdict(int)
	res3 = defaultdict(lambda: -1, res3)
	res4 = defaultdict(int)
	res4 = defaultdict(lambda: -1, res4)

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

#
# read in all user CVs
#
def read_all_user_CVs():

	user_IDs = read_user_IDs()
	user_CVs = defaultdict(int)
	cnt = 0

	with open(f_in) as f:
	    for line in f:
	        line_dict = json.loads(line)
	        usr = line_dict["_id"]
	        usr_id = user_IDs[usr]
	        user_CVs[usr_id] = {}
	        user_CVs[usr_id]["num_tweets"] = line_dict["num_tweets"]
	        CVa = line_dict["CV"]
	        user_CVs[usr_id]["CV"] = { k: v for d in CVa for k, v in d.items() }
	        if cnt % 10000 == 0:
	        	print cnt, usr, usr_id
	        cnt += 1

	return user_CVs

#
# extract all concepts in a community and sort them by popularity
# 
def find_popular_concepts(com_id, com, user_CVs):

	CV_sum = defaultdict(int)

	for usr in com:
		CV = user_CVs[usr]
		if CV <> 0:
			cv = CV["CV"]
			num_tweets = CV["num_tweets"]
			for concept in cv:
				CV_sum[concept] += float(cv[concept]) / float(num_tweets) # do we need the scaling??

	top_CVs = OrderedDict(sorted(CV_sum.items(), key=lambda x: x[1], reverse= True))
	fig_name = working_subfolder + "top_concepts" + str(X) + "_COM_" + com_id + ".png"
	plot_popular_concepts(top_CVs,fig_name, com_id)

	f_out = working_subfolder + "top_concepts_SR_" + str(X) + "_COM_" + com_id + ".tab"
	f = open(f_out, "w")
	for c in top_CVs:
		f.write(str(c) +  '\t' + str(top_CVs[c]) + '\n')

	print "Processed community %s and found %d different concepts" % (com_id, len(CV_sum))

def plot_popular_concepts(data,fig_name, com_id):
	N = len(data)
	x = np.arange(0,N,1)
	y = np.array(data.values())
	plt.loglog(x, y, label='COM'+com_id)
	plt.grid(True)
	plt.title('Top concepts in different communities: count')
	plt.legend()
	plt.savefig(fig_name,format='png',dpi=440)
#
# extract all concepts in a community and sort them by popularity
# 
def find_popular_concepts_user_list(lst_name, lst, user_CVs):

	CV_sum = defaultdict(int)
	aids = read_article_IDs()

	for usr in lst:
		CV = user_CVs[usr]
		if CV <> 0:
			cv = CV["CV"]
			num_tweets = CV["num_tweets"]
			for concept in cv:
				CV_sum[concept] += float(cv[concept]) # / float(num_tweets) # do we need the scaling??

	top_CVs = OrderedDict(sorted(CV_sum.items(), key=lambda x: x[1], reverse= True))
	fig_name = working_subfolder + "top_concepts" + lst_name + ".png"
	plot_popular_concepts_user_list(top_CVs,fig_name, lst_name)

	f_out = DIR_top_users + "top_concepts_" + lst_name + ".tab"
	f = open(f_out, "w")
	for c in top_CVs:
		f.write(str(c) +  '\t' + str(top_CVs[c]) + '\t' + str(aids[c]) + '\n')

	print "Processed %s and found %d different concepts" % (lst_name, len(CV_sum))

def plot_popular_concepts_user_list(data,fig_name, com_id):
	N = len(data)
	x = np.arange(0,N,1)
	y = np.array(data.values())
	plt.loglog(x, y, label=com_id)
	plt.grid(True)
	plt.title("Top concepts in " + com_id + " : count")
	plt.legend()
	plt.savefig(fig_name,format='png',dpi=440)


###
### call the others
###
def main():

	os.chdir(IN_DIR)
	# number of nodes in a community
	sizeN = 300
	top_communities, com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)

	f_out_name = "CV_summary_of_" + str(sizeN) + ".json"

	N = len(top_communities)
	print N, "top communities found ", "of size larger than ", sizeN

	NALL = len(all_communities)
	print NALL, "all communities found"

	#all_users = read_user_IDs()
	#################################################################
	# 
	#full_taxonomy_tfidf = find_full_tfIDF_taxonomy(all_com_id_map) #TODO
	user_CVs = read_all_user_CVs()
	for community in top_communities:
		find_popular_concepts(community, top_communities[community], user_CVs)
	#################################################################
	

###
### call the others
###
def main_user_list():

	os.chdir(IN_DIR)

	user_CVs = read_all_user_CVs()
	TOP_users_lists = read_TOP_users()

	for top_list in TOP_users_lists:
		find_popular_concepts_user_list(top_list, TOP_users_lists[top_list], user_CVs)

#main()

main_user_list()
