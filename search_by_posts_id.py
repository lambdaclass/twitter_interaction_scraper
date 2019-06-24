import tweepy as tw
import csv
import urllib2
import re
import os
from dotenv import load_dotenv, find_dotenv
import datetime
import time
import helpers
load_dotenv(find_dotenv())


CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')


auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tw.API(auth, wait_on_rate_limit=True)

users = []

#Given a list of tweets id and user, get engagement on status

list_of_tweets = [
]

user='@'

helpers.get_users_that_liked_or_retweet(list_of_tweets)
helpers.get_users_responded_tweet(user)
helpers.populate_csv_file(users)