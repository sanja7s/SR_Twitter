#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import codecs
from collections import defaultdict

f_in = "mentions_reciprocal_six_months.dat"
f_out = "en_mentions_reciprocal_six_months1K.dat"

def detect_language(text):
	ratios = _calculate_languages_ratios(text)
	most_rated_language = max(ratios, key=ratios.get)
	return most_rated_language


def _calculate_languages_ratios(text):
	languages_ratios = {}
	tokens = wordpunct_tokenize(text)
	words = [word.lower() for word in tokens]
    # Compute per language included in nltk number of unique stopwords appearing in analyzed text
	for language in stopwords.fileids():
		stopwords_set = set(stopwords.words(language))
		words_set = set(words)
		common_elements = words_set.intersection(stopwords_set)
		languages_ratios[language] = len(common_elements) # language "score"
	return languages_ratios

def read_in_tweets(f_in, f_out):
	# count how many tweets (i.e., lines) are read
	cnt_all_tweets = 0
	cnt_en_wteets = 0

	all_lang = defaultdict(int)

	output_file = codecs.open(f_out,'w',encoding='utf8')

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, saves tweets which are found to be eng
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	#line = line.split(' ')
	    	text = line
	    	all_lang[detect_language(text)] += 1
	#outfile.close()
	for lang in all_lang.keys():
		print lang, all_lang[lang]
	#print "Saved tweets: ", len(articles), "ALL READ tweets: ", cnt_all_tweets

read_in_tweets(f_in, f_out)