import tweepy
import os
import json
import argparse
import time
import sys


enc = lambda x: x.encode('ascii', errors='ignore')

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
CONSUMER_KEY = 'mB2nn3NuN9lGWpVmKTuwTA'
CONSUMER_SECRET = 'FYvYywBmAIhVo5K1c11fRLPNdDqOlKv3nxj0koJctk'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
ACCESS_TOKEN = '117220030-XGrXJn3xCR1yKRu6uBMkjg0kMHMfNgGGRsPAeecb'
ACCESS_TOKEN_SECRET = 'HAdGP9Lk43Uun7sZYRxH4cLmxPzAMavWNUyFcsDjQ'

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
api.wait_on_rate_limit = True
api.wait_on_rate_limit_notify = True

if __name__ == '__main__':
    rs=[]
    textFile = open(sys.argv[2],"r")
    twitter_screennames = textFile.readlines()
    n=len(twitter_screennames)
    k=0
    with open(sys.argv[3], 'w') as outf:
        for i in range(0,n-1):
            k=k+1
            print(str(k) + "-th check out of: " + str(n))
            try:
                users=twitter_screennames[i].split('\t')
                fol1=0
                fol2=0
                if (sys.argv[1]=="0"):
                    fs=api.show_friendship(source_screen_name=users[0], target_screen_name=users[1])
                else:
                    fs=api.show_friendship(source_id=users[0], target_id=users[1])
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


