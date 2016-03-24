#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
	Join article names for the popular concepts found in each community
"""
from collections import defaultdict
import glob, os

IN_DIR = "../../../DATA/CV"

#########################################################
# SR
#########################################################
X = "0.6"
working_subfolder = "SR_communities/"
# the communities we analyze (from the SR graph)
spec_users = working_subfolder + "communitiesSR_" + str(X) + ".txt"
#########################################################
#########################################################
# Mention
#########################################################
#X = "" #dummy
#working_subfolder = "mention_communities/"
# the communities we analyze (from the mention graph)
#spec_users = working_subfolder + "communitiesMent" + str(X) + ".txt"
#########################################################

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
			if cnt % 10000 == 0:
				print line
			cnt += 1

	return article_IDs

#
# extract all concepts in a community and sort them by popularity
# 
def save_popular_articles(com_id, article_IDs):

	f_in = working_subfolder + "top_concepts_SR_" + str(X) + "_COM_" + com_id + ".tab"
	f = open(f_in, "r")

	f_out = working_subfolder + com_id  + "_COM_" + str(X) + "top_articles.tab"
	f2 = open(f_out, "w")

	for line in f:
			line = line[:-1].split('\t')
			aid = line[0]
			aTF = line[1]
			aname = article_IDs[aid]
			f2.write(str(aTF) +  '\t' + str(aname) + '\t' + str(aid) + '\n')

	print "Processed community %s " % (com_id)

###
### call the others
###
def main():

	os.chdir(IN_DIR)
	# number of nodes in a community
	sizeN = 300
	top_communities, com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)

	N = len(top_communities)
	print N, "top communities found ", "of size larger than ", sizeN

	NALL = len(all_communities)
	print NALL, "all communities found"

	article_IDs = read_article_IDs()
	#################################################################
	for community in top_communities:
		save_popular_articles(community, article_IDs)
	#################################################################
	

main()
