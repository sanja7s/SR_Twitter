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

	if not node.is_root() or node.is_root():
		# give node name to all but the root
		faces.add_face_to_node(TextFace(node.name), node, 0)
		# and increase them with the wight
		if "weight" in node.features:
			# Creates a sphere face whose size is proportional to node's
			# feature "weight"
			C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
			# Let's make the sphere transparent 
			C.opacity = 0.3
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
		n.add_features(weight=n.dist*20.0)

	# Create an empty TreeStyle
	ts = TreeStyle()

	# Set our custom layout function
	ts.layout_fn = layout

	ts.show_leaf_name = False
	# Draw a tree 
	#ts.mode = "c"
	ts.min_leaf_separation = 7
	ts.show_scale = False
	#ts.arc_start = -180
	#ts.arc_span = 180
	ts.scale = 200

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
IN_DIR = "../../../DATA/taxonomy_stats"

def read_user_IDs():

    user_ids = defaultdict(str)

    with codecs.open(f_in_user_ids,'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_ids[user] = user_id

    return user_ids

###
# 
###
def read_in_data(uid):
	
	# resulting dictionary in which the taxonomy is collected
	res = defaultdict(int)
	# holds all the user ids
	user_ids = read_user_IDs()

	t7s  = Tree7s("thing")

	cnt = 0
	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		for line7s in input_file:
			try:
				line = json.loads(line7s)
				taxonomy_all = line["taxonomy"]
				user_name = line["_id"]
				user_id = user_ids[user_name]
				#docSentiment = taxonomy_all["docSentiment"] 
				# the user we analyze
				user_name = line["_id"]
				user_id = user_ids[user_name]
				if uid != user_id:
					continue
				res[user_id] = defaultdict(int)
				taxonomy = taxonomy_all["taxonomy"]

				for el in taxonomy:
						n = t7s.find_root()
						taxonomy_tree = el["label"]
						taxonomy_tree = taxonomy_tree.split("/")
						taxonomy_tree.pop(0)
						levels = len(taxonomy_tree)
						score = float(el["score"])
						if float(score) > 0.4:
							print levels, taxonomy_tree, score
							for i in range(levels):
								label = taxonomy_tree[i]
								n.add_child(label, score, i+1)
								n = n.find_child(label)
				cnt += 1
			except KeyError:
				#print line7s
				# we don't print since it is tested, there some 10% users for whom
				# the taxonomy was not successfuly downloaded and they would be listed here
				continue
	print "Taxonomy collected for %d users " % (cnt)

	#t7s.find_root().print_me()
	t = t7s.find_root()
	S =  t.create_newick() + ";"

	#print S
	#T = Tree(S, format=8)
	T = Tree(S, format=1)

  	return T


def prune_tree(t, threshold=10.0):

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

	#usr_lst = [3695,	28692,26424,	25042, 2898,	15791, 23083,	23813, 17609,	6798, 26643, \
	#			27353, 15791,	2898, 28692,	3695, 25042,	26424, 14992,	24020, 24020,	14992, \
	#			7250,	6317, 23813,	23083, 6317,	7250, 3817,	6793, 6793,	3817, 27711,	11388, \
	#			11388,	27711, 6798,	17609, 27353,	26643, 25713,	10382, 10382,	25713]

	usr_lst = [1345,  26125,6035,	12406, 13952,	19631, 24923,	26301, 10907,	27318, \
				21405,	10725, 19966,	330, 15810,	22078, 14156,	23485, 890,	21148, 7513,	14191 ]

	usr_lst = [str(usr) for usr in set(usr_lst)]
	print usr_lst

	#usr_lst = ['3817']

	for uid in usr_lst:

		t = read_in_data(uid)
		print "FIRST check"
		check_tree(t)
		#print "SECOND check"
		#prune_tree(t, 0.0)
		print "LAST check"
		check_tree(t)
		ts = give_tree_layout(t)
		#t.show(tree_style=ts)
		t.render("BUBBLE/users/opposite_sentiment/" + str(uid) + "bubble_map.png", w=3440, dpi=650, tree_style=ts)