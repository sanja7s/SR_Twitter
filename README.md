# SR_Twitter

Apply ESA (Explicit Semantic Analysis) algorithm for calculating semantic relatedness (SR) of tweets.

Using semantic knowledge database that is implemented in [SR_Wiki_ESA](https://github.com/sanja7s/SR_Wiki_ESA/), find how 'similar' or (correctly) 'related' are tweets and also Twitter users, based on the collections of their tweets.

[SR_2_Twitter_users.py](src_SR/SR_2_Twitter_users.py) is the main module to find SR for two users or words or texts in general. 

First, users tweets collections are cleaned for English and then entered in MongoDB [user_tweets_2_mongo.py](src_MONGO/user_tweets_2_mongo.py), where is as well the semantic knowledge database residing. 

Now, [SR_2_Twitter_users.py](src_SR/SR_2_Twitter_users.py) stems the tweet collections, extracts relevant concept vectors (CV) from the semantic database for each unique word in the corpus and calculates, in the end, their SR score. We can also find most relevant concepts for each word and for each user. 

Another important step was to enable faster bulk processing. Hence, in [user_CVs_2_mongo_with_check.py](src_MONGO/user_CVs_2_mongo_with_check.py) we calculate concept vector (CV) for each user and dump them in a JSON file suitable for easy input to MongoDB.

The most time and resource-consuming is SR calculation between all the users we have. This asks for a full graph, and even with 10Ks of users is demadning if each individual SR calculation is any slow. So we use pool.map from Python multiprocessing in [SR_all_Twitter_users.py](src_SR/SR_all_Twitter_users.py). 