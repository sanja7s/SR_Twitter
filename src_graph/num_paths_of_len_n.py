#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np 
import os


# for ORIGINAL
f_in_graph_SR = "undir_threshold95.tab"
IN_DIR = "../../../DATA/SR_graphs/num_paths"
f_out_res = "num_paths/res.txt"


N = 26717 # or 29610 if some error with ids, possibleeee

Adj_Mat = np.zeros((N,N), dtype=int)

def read_in_network():
	f = open(f_in_graph_SR)
	for line in f:
		(u1, u2) = line.split()
		u1 = int(u1)
		u2 = int(u2)
		Adj_Mat[u1,u2] = 1
	return Adj_Mat

def test_network():

	M = np.array([[0, 1, 1], [1, 0, 0], [1, 0, 0]])

	return M

def find_paths(k, Adj_Mat):

	os.chdir(IN_DIR)

	res = Adj_Mat

	for i in range(k-1):
		print i+1
		print res
		print Adj_Mat
		res = np.dot(res, Adj_Mat)
		np.fill_diagonal(res, 0)

	k_paths = np.sum(res) / 2

	return k_paths, res


if __name__ == '__main__':

	k = 111

	M = test_network()
	k_paths, res = find_paths(k, M)

	print "######"
	print res
	print "res for %d is %d paths " % (k, k_paths)


