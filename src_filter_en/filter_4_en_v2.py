from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
import codecs

f_in = "mentions_reciprocal_six_months1K.dat"
f_out = "en_mentions_reciprocal_six_months1K.dat"


ENGLISH_STOPWORDS = set(stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(stopwords.words()) - ENGLISH_STOPWORDS

def is_eng(text):
    """Return True if text is probably English, False if text is probably not English
    """
    text = text.lower()
    words = set(wordpunct_tokenize(text))
    return len(words & ENGLISH_STOPWORDS) > len(words & NON_ENGLISH_STOPWORDS)

def read_and_filter_eng_tweets(f_in, f_out):
	# count how many tweets (i.e., lines) are read
	cnt_all_tweets = 0
	cnt_en_tweets = 0

	output_file = codecs.open(f_out,'w',encoding='utf8')

	with codecs.open(f_in,'r', encoding='utf8') as input_file:
		# the code loops through the input, saves tweets which are found to be eng
	    for line in input_file:	
	    	cnt_all_tweets += 1
	    	text = line
	    	if is_eng(text):
	    		output_file.write(text)
	    		cnt_en_tweets += 1

	    	if cnt_all_tweets % 100000 == 0:
	    		print cnt_all_tweets, cnt_en_tweets, line
	output_file.close()
	print "Found ENG tweets: ", cnt_en_tweets, "ALL READ tweets: ", cnt_all_tweets

read_and_filter_eng_tweets(f_in, f_out)