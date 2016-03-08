#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import glob, os


f_in = "tweets_taxonomy.JSON"
f_out = "tweets_taxonomy_clean.JSON"
in_dir = "../DATA/taxonomy_stats"


def clean_and_save():

	os.chdir(in_dir)

	with codecs.open(f_out,'w', encoding='utf8') as output_file:

		cnt = 0
		with codecs.open(f_in,'r', encoding='utf8') as input_file:
			# the code loops through the input, collects taxonomies per user
			for line7s in input_file: 
				if line7s.strip() != "null":
					output_file.write(line7s)
					cnt += 1

		print("Saved users: ", cnt)

clean_and_save()