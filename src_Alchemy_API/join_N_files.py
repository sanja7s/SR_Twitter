#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import codecs
import glob, os


f_out = "tweets_taxonomy.JSON"
in_dir = "taxonomy/"


def collect_and_save():

	os.chdir(in_dir)

	with codecs.open(f_out,'w', encoding='utf8') as output_file:
		cnt = 0
		for f_in in glob.glob("*.json"):
			print(f_in)
			with codecs.open(f_in,'r', encoding='utf8') as input_file:
				# the code loops through the input, collects taxonomies per user
				for line7s in input_file: 
					cnt += 1
					output_file.write(line7s)
					if cnt % 10000 == 0:
						print('Processing users: ', cnt)
	print("Read ALL users: ", cnt)


collect_and_save()
