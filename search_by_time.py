import tweepy as tw
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

api = tw.API(auth)

users=[]

class Tweet(object):
    id_ = ""
    created_at = 0

    def __init__(self, id_, created_at):
        self.id_ = id_
        self.created_at = created_at



def get_older_posts(user, startDate, endDate = datetime.datetime.today()):
    list_tweets = []
    ids = []
    tweets = tw.Cursor(api.user_timeline, user_name=user).items(20)
    for tweet in tweets:
        new_tweet = Tweet(tweet.id, tweet.created_at)
        list_tweets.append(new_tweet)
    last_element = list_tweets[-1]
    while last_element.created_at > startDate:
        older_tweets = tw.Cursor(api.user_timeline, user_name=user, max_id=last_element.id_).items(20)
        for tweet in older_tweets:
            new_tweet = Tweet(tweet.id, tweet.created_at)
            list_tweets.append(new_tweet)
        last_element = list_tweets[-1]    
    for tweet in list_tweets:
        ids.append(tweet.id_)
    return ids

#Define the date you want to use as a Start Date for your search (YYYY, MM, DD, HH, MM, SS)
from_date = datetime.datetime(2019, 04, 01, 00, 00, 00)

# Define the user you want to search tweets using the @user_name
ids_old_tweets = get_older_posts('user_name', from_date)
helpers.get_users_that_liked_or_retweet(ids_old_tweets)
helpers.populate_csv_file(users)

