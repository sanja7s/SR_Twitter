#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import random
from ete2 import Tree, TreeStyle, NodeStyle, faces, AttrFace, CircleFace, TextFace

def layout(node):
	if not node.is_root():
		# Add node name to laef nodes
		#N = AttrFace("name", fsize=14, fgcolor="black")
		#faces.add_face_to_node(N, node, 0)
		#pass
		faces.add_face_to_node(TextFace(node.name), node, 0)
		if "weight" in node.features:
			# Creates a sphere face whose size is proportional to node's
			# feature "weight"
			C = CircleFace(radius=node.weight, color="RoyalBlue", style="sphere")
			# Let's make the sphere transparent 
			C.opacity = 0.3
			# And place as a float face over the tree
			faces.add_face_to_node(C, node, 0, position="float")

def give_tree_layout(t):

	# Some random features in all nodes
	for n in t.traverse():
		n.add_features(weight=n.dist*20)

	# Create an empty TreeStyle
	ts = TreeStyle()

	# Set our custom layout function
	ts.layout_fn = layout

	# Draw a tree 
	#ts.mode = "c"
	#ts.arc_start = -180
	#ts.arc_span = 180

	# We will add node names manually
	#ts.show_leaf_name = True
	# Show branch data
	#ts.show_branch_length = True
	#ts.show_branch_support = True

	return ts

class Tree7s(object):
	def __init__(self, lab):
		self.root = Node7s(lab, 0, 0)

	def find_root(self):
		return self.root

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


def test_data():

	D = {'taxonomy': [{"score": "0.718868", "label": "/art and entertainment/movies and tv/movies"},\
	{"confident": "no", "score": "0.304296", "label": "/pets/cats"},\
	{"score": "0.718868", "label": "/art and entertainment/movies and tv/series"}]}

	t7s  = Tree7s("ThingAdamsFamily")
	
	for el in D["taxonomy"]:
		#n = t7s
		n = t7s.find_root()
		taxonomy_tree = el["label"]
		taxonomy_tree = taxonomy_tree.split("/")
		taxonomy_tree.pop(0)
		levels = len(taxonomy_tree)
		score = float(el["score"])
		print levels, taxonomy_tree, score
		for i in range(levels):
			label = taxonomy_tree[i]
			#if n.find_child(label) == None:
			n.add_child(label, score, i+1)
			n = n.find_child(label)

	t7s.find_root().print_me()
	t = t7s.find_root()
	S =  t.create_newick() + ";"

	print S
	#S = "(((A,B,(C.,D)E)F,(S,N)K)R);"
	#T = Tree(S, format=8)
	T = Tree(S, format=1)

	for node in T.traverse("postorder"):
  	# Do some analysis on node
  		print node.name

	for node in T.traverse("levelorder"):
  	# Do some analysis on node
  		print node.name

  	#for branch in T

  	return T

if __name__ == "__main__":

	#t.render("bubble_map.png", w=600, dpi=300, tree_style=ts)
	#t.show(tree_style=ts)

	t = test_data()
	
	ts = give_tree_layout(t)
	t.show(tree_style=ts)
	t.render("bubble_map.png", w=600, dpi=300, tree_style=ts)