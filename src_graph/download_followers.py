import tweepy
import os
import json
import argparse
import time
import sys
from collections import defaultdict
import codecs

enc = lambda x: x.encode('ascii', errors='ignore')

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = 'yZO5JLzYSrNuXOvexkavIw'
CONSUMER_SECRET = 'd1oDpoTTkNfy3febH6w1xF0htxUTiqO71Jq5681HSM'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = '164190842-hgj6H2PuZRnsLspEPVgbdjZna5T4jY1DEWiKP7aA'
ACCESS_TOKEN_SECRET = 'LU38vSgaGR0Rn4Bew3crGymkNUdClPptzL3b4xdqv8'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

def read_in_usernames():

    user_names = defaultdict(str)

    with codecs.open(sys.argv[4],'r', encoding='utf8') as f:
        for line in f:
            line = line.split()
            user_id = line[0]
            user =  line[1]
            user_names[user_id] = user

    return user_names

if __name__ == '__main__':
    rs=[]
    textFile = open(sys.argv[2],"r")
    twitter_screennames = textFile.readlines()
    if (sys.argv[1]!="0"):
        user_names = read_in_usernames()
    n=len(twitter_screennames)
    k=0
    with open(sys.argv[3], 'w') as outf:
        for i in range(0,n-1):
            k=k+1
            print(str(k) + "-th check out of: " + str(n))
            try:
                users=twitter_screennames[i].split()
                fol1=0
                fol2=0
                if (sys.argv[1]=="0"):
                    fs=api.show_friendship(source_screen_name=users[0], target_screen_name=users[1])
                else:
                    print users[0], user_names[users[0]], users[1], user_names[users[1]]
                    fs=api.show_friendship(source_screen_name=user_names[users[0]], target_screen_name=user_names[users[1]])
                if (fs[0].following):
                    fol1=1
                if (fs[0].followed_by):
                    fol2=1
                if (fol1==0 and fol2==0):
                    outf.write(users[0] + '\t' + users[1] + '\t' + '0' + '\t' + users[2]  +  '\n')
                if (fol1==1 and fol2==0):
                    outf.write(users[0] + '\t' + users[1] + '\t' + '1' + '\t' + users[2]  + '\n')
                if (fol1==0 and fol2==1):
                    outf.write(users[1] + '\t' + users[0] + '\t' + '1' + '\t' + users[2]  + '\n')
                if (fol1==1 and fol2==1):
                    outf.write(users[0] + '\t' + users[1] + '\t' + '2' + '\t' + users[2]  + '\n')
            except:
                outf.write(users[0] + '\t' + users[1] + '\t' + '-1' + '\t' + users[2]  + '\n')

