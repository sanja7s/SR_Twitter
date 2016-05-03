#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	use ete2 and represent our taxonomy data using Newick format to render them nicely
"""
import os, codecs, json
from ete2 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace, TextFace
from collections import defaultdict
###
# our custom layout to increase the node size with weight and
# to show the names for all the nodes
###
def layout(node):

	if not node.is_root():
		# give node name to all but the root
		faces.add_face_to_node(TextFace(node.name), node, 0)
		# and increase them with the wight
		if "weight" in node.features:
			# Creates a sphere face whose size is proportional to node's
			# feature "weight"
			C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
			# Let's make the sphere transparent 
			C.opacity = 0.34
			# And place as a float face over the tree
			faces.add_face_to_node(C, node, 0, position="float")

###
# give the ete2 tree to this function to send us back a layout for it
# where the weight of the nodes is based on the property distance
# (that is where we saved the cumulative score for each taxonomy node)
###
def give_tree_layout(t):

	# for all nodes give them the weight = score
	for n in t.traverse():
		n.add_features(weight=n.dist/20.0)

	# Create an empty TreeStyle
	ts = TreeStyle()

	# Set our custom layout function
	ts.layout_fn = layout

	ts.show_leaf_name = False
	# Draw a tree 
	ts.mode = "c"
	#ts.arc_start = -180
	#ts.arc_span = 180
	#ts.scale = 100
	ts.min_leaf_separation = 10
	ts.show_scale = False

	return ts

###
# when creating the Newick format, we use our Tree7s class and recursion
###
class Tree7s(object):
	def __init__(self, lab):
		self.root = Node7s(lab, 0, 0)

	def find_root(self):
		return self.root

###
# each node has data (= taxonomy name), score and level
###
class Node7s(object):
	def __init__(self, data, score, lev):
		self.data = data
		self.score = score
		self.level = lev
		self.children = []

	def add_child(self, lab, score, lev):
		if int(self.level) == int(lev-1):
			nn = self.find_child(lab)
			if nn == None:
				self.children.append(Node7s(lab, score, lev))
			else:
				nn.increase_score(score)
		else:
			# with the way how we populate this tree, this should never happen
			# is serves only as a check of correctness
			print "Trying to add to a wrong level?", lev-1, self.level, lab, self.data

	def find_child(self, label):
		for el in self.children:
			if el.data == label:
				return el
		return None

	def increase_score(self, sc):
		self.score += sc

	def print_me(self):
		print self.data, self.score
		for el in self.children:
			el.print_me()

	# here we create the Newick string format for ete2
	# we use the format 1 from 
	# http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#trees
	def create_newick(self):
		if self.children == []:
			return str(self.data + ":" + str(self.score))
		newick = "("
		for el in self.children:
			newick += el.create_newick() + ","
		newick = newick[:-1]
		if self.level == 0:
			newick += ")" + str(self.data) +  "."
		else:
			newick += ")" + str(self.data) + ":" + str(self.score)
		return newick


###
# data file sources
###
f_in = "tweets_taxonomy_clean.JSON"
#f_in = "testme"
f_in_user_ids = "user_IDs.dat"
IN_DIR = "../../../DATA/taxonomy_stats/BUBBLE"

#mention
THE_FOLDER = "mention/"
spec_users = THE_FOLDER + "communitiesMent.txt"
SAVE_IN = THE_FOLDER + "100/"

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
# here we will extract IDF values, i.e., document counts for the taxonomies
# 
def find_full_tfIDF_taxonomy(user_com):

	taxonomies_sum= defaultdict(int) 
	user_ids = read_user_IDs()
	cnt = 0

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				user_name = line["_id"]
				user_id = user_ids[user_name]
				COM = user_com[user_id]
				taxonomy_all = line["taxonomy"]
				taxonomy = taxonomy_all["taxonomy"] 
			except KeyError:
				continue

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
					if tax_class not in s.keys():
						s[tax_class] = defaultdict(int)
						s[tax_class]["documents_found"] = []
					s = s[tax_class]

				if COM <> -1:
					s["documents_found"].append(COM)
	return taxonomies_sum

#
# here we will extract IDF values, i.e., document counts for the taxonomies
# 
def read_in_comm_taxonomy(user_ids, user_list):

	t7s  = Tree7s("ThingAdamsFamily")
	cnt = 0

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				user_name = line["_id"]
				user_id = user_ids[user_name]
				if user_list[user_id] == 0:
					continue    
				taxonomy_all = line["taxonomy"]
				taxonomy = taxonomy_all["taxonomy"] 
			except KeyError:
				continue

			for el in taxonomy:
				n = t7s.find_root()
				taxonomy_tree = el["label"]
				taxonomy_tree = taxonomy_tree.split("/")
				taxonomy_tree.pop(0)
				levels = len(taxonomy_tree)
				score = float(el["score"])
				if float(score) > 0.4:
					#print levels, taxonomy_tree, score
					for i in range(levels):
						label = taxonomy_tree[i]
						n.add_child(label, score, i+1)
						n = n.find_child(label)
			cnt += 1

	print "Taxonomy collected for %d users " % (cnt)
	     
	#t7s.find_root().print_me()
	t = t7s.find_root()
	S =  t.create_newick() + ";"

	#print S
	#T = Tree(S, format=8)
	T = Tree(S, format=1)

  	return T


def prune_tree(t, threshold=100.0):

	to_delete_nodes = []

	for node in t.iter_descendants():
  		# delete too small nodes
  		if float(node.dist) < threshold:
  			to_delete_nodes.append(node)
  			node.delete(prevent_nondicotomic=False,preserve_branch_length=False)

def check_tree(t):

	for node in t.traverse():
		if node.name == "sex":
  			print node.name, node.dist
  		if node.name == "movies":
  			print node.name, node.dist
  		if node.name == "crime":
  			print node.name, node.dist
  		if "entertainment" in node.name:
  			print node.name, node.dist

if __name__ == "__main__":

	os.chdir(IN_DIR)

	sizeN = 300
	top_communities, com_id_map, all_communities, all_com_id_map = read_in_communities(sizeN)

	N = len(top_communities)
	print N, "top communities found"

	NALL = len(all_communities)
	print NALL, "all communities found"

	# holds all the user ids
	user_ids = read_user_IDs()

	for community in top_communities:
		t = read_in_comm_taxonomy(user_ids, top_communities[community])
		print "FIRST check"
		check_tree(t)
		#print "SECOND check"
		prune_tree(t, 20.0)
		print "LAST check"
		check_tree(t)
		ts = give_tree_layout(t)
		#t.show(tree_style=ts)
		t.render(SAVE_IN + str(community) + "_COM_bubble_map.png", w=1200, dpi=440, tree_style=ts)