#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#	Copyright 2013 AlchemyAPI
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import print_function
from alchemyapi import AlchemyAPI
import codecs
from collections import defaultdict, OrderedDict
import json
import re


f_in = "../tweets_per_usr"
f_out = "../resall/tweets_taxonomy.json"


def read_tweet_text_per_user(f_in):
    cnt_all_tweets = 0
    user_tweets = OrderedDict()
    with codecs.open(f_in,'r', encoding='utf8') as input_file:
        # the code loops through the input, collects tweets for each user into a dict
        for line7s in input_file: 
            cnt_all_tweets += 1
            line = line7s.split('\t')
	    try:
            	user = line[0]
            	#print(user)
            	tweets = line[1]
            	user_tweets[user] = tweets
	    except IndexError:
		print("IndexErrror", user)
            if cnt_all_tweets % 100000 == 0:
                print('Processing lines: ', cnt_all_tweets, ' and tweet text:', tweet)
    print("Read users count: ", cnt_all_tweets)
    return user_tweets


# go through our tweets collections pers user. send each collection to API
# collect the taxonomy and save in a JSON object with the user _id (suitable for input to MongoDB)
def main():

    alchemyapi = AlchemyAPI()

    user_tweets = read_tweet_text_per_user(f_in)
    cnt = 0
    LAST_USR = "SAMMYLEEJONES"
    UNPROCESSED = False
    with codecs.open(f_out, 'a', encoding='utf8') as output_file:
        for user1 in user_tweets.iterkeys():
            cnt+= 1
            if not UNPROCESSED:
                if user1 != LAST_USR:
                    continue
                else:
                    UNPROCESSED = True
                    print("Found", LAST_USR, cnt)
            if cnt % 100 == 0:
                print(cnt, user1)
            tweets1 = user_tweets[user1]
            BREAK, taxonomy_result1 = alchemy_on_tweets(alchemyapi, user1, tweets1)
            # there is the API daily limit so we check when exceeded and continue tomorrow from
            # the last processed users
            if BREAK:
                print("Last processed user: ", user1)
                return
            output_file.write(unicode(json.dumps(taxonomy_result1, ensure_ascii=False)) + '\n')
            return



# Create the AlchemyAPI Object
# the code from the API. we adapted to save output in a reasonabel JSON for us
def alchemy_on_tweets(alchemyapi, usr, tweets):
    BREAK = False
    demo_text = tweets
    res = defaultdict(int)

    response = alchemyapi.combined('text', demo_text)

    if response['status'] == 'OK':
        #print('## Response Object ##')
        #print(json.dumps(response, indent=4))

        res['keywords'] = response['keywords']

        res['concepts'] = response['concepts']

        res['entities'] = response['entities']
    else:
        print('Error in combined call: ', usr, response['statusInfo'])
        if response['statusInfo'] == "daily-transaction-limit-exceeded":
        	BREAK = True
        	return BREAK, None
        elif response['statusInfo'] == "unsupported-text-language":
            return BREAK, None

    response = alchemyapi.taxonomy('text', demo_text)

    if response['status'] == 'OK':

        res['taxonomy'] = response['taxonomy']

    else:
        print('Error in taxonomy call: ', usr, response['statusInfo'])
        if response['statusInfo'] == "daily-transaction-limit-exceeded":
        	BREAK = True
        	return BREAK, None
        elif response['statusInfo'] == "unsupported-text-language":
            return BREAK, None


    response = alchemyapi.sentiment('text', demo_text)

    if response['status'] == 'OK':
        #print('## Response Object ##')
        #print(json.dumps(response, indent=4))

        res['docSentiment'] = response['docSentiment']
    else:
        print('Error in sentiment analysis call: ', usr, response['statusInfo'])
        if response['statusInfo'] == "daily-transaction-limit-exceeded":
        	BREAK = True
        	return BREAK, None

    
    final_res = {}
    final_res['_id'] = str(usr)
    final_res['taxonomy'] = res
    return BREAK, final_res

main()
