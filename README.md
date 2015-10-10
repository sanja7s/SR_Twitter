# SR_Twitter

Apply ESA for calculating semtnatic relatedness (SR) of tweets.

Using semantic knowledge database that is implemented in [SR_Wiki_ESA](https://github.com/sanja7s/SR_Wiki_ESA/), find how 'similar' or (correctly) 'related' are tweets and also Twitter users, based on the collections of their tweets.

[SR_2_Twitter_users.py](SR_2_Twitter_users.py) is the main module. 

First, users tweets collections are cleaned for English and then entered in MongoDB [user_tweets_2_mongo.py](user_tweets_2_mongo.py), where is as well the semantic knowledge database residing. 

Now, [SR_2_Twitter_users.py](SR_2_Twitter_users.py) stems the tweet collections, extracts relevant concept vectors (CV) from the semantic database for each unique word in the corpus and calculates, in the end, their SR score. We can also find most relevant concepts for each word and for each user. 
