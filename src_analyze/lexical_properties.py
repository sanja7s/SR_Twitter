#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def lexical_diversity(text):
	return len(text) / len(set(text))


def word_percentage(word, text):
	return 100 * text.count(word) / len(text)


# find what index of the word is in the vocabulary
text4.index('awaken')


# find vocabulary and frequencies
 fdist1 = FreqDist(text1)
 vocabulary1 = fdist1.keys()
fdist1['whale']

#long frequent words
sorted([w for w in set(text5) if len(w) > 7 and fdist5[w] > 7])

# collocations or frequent bigrams
text4.collocations()

# To derive the vocabulary, collapsing case distinctions and ignoring punctuation, we can write 
set([w.lower() for w in text if w.isalpha()])