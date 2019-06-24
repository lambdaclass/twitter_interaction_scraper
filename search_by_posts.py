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

# Given a user gets engagement on the last posts, items is the number of post to retrieve

def get_engagement(user, items):
    ids = []
    user_id = api.get_user(user).id
    for status in tw.Cursor(api.user_timeline, user_name=user).items(items):
        ids.append(status.id)
        if status.in_reply_to_status_id == user_id:
            u = api.get_user(status.user.id)
            if u.id not in users:
                users.append(u.id)
    helpers.get_users_that_liked_or_retweet(ids)

helpers.populate_csv_file(users)