import tweepy as tw
import csv
import urllib2
import re
import os
from dotenv import load_dotenv, find_dotenv
from config import tweetsId, tweets_user
import datetime
import time

load_dotenv(find_dotenv())


users = []
users_ids = []

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')


auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tw.API(auth, wait_on_rate_limit=True)




users = []
users_ids = []


def get_user_ids_of_post_likes(post_id):
    try:
        json_data = urllib2.urlopen(
            'https://twitter.com/i/activity/favorited_popup?id=' + str(post_id)).read()
        found_ids = re.findall(r'data-user-id=\\"+\d+', json_data)
        unique_ids = list(set([re.findall(r'\d+', match)[0]
                               for match in found_ids]))
        return unique_ids
    except urllib2.HTTPError:
        return False

# from a list of tweets Id get the users that liked or retweeted that tweet

def get_users_that_liked_or_retweet(tweetsId):
    for tweet in tweetsId:
        user_likes = get_user_ids_of_post_likes(str(tweet))
        for user_id in user_likes:
            if user_id not in users:
                users.append(user_id)
        retweets = api.retweets(tweet)
        for retweet in retweets:
            u = retweet.user
            if u.id not in users:
                users.append(u.id)



# from a list of tweets ids gets the users that replied to that tweet
def get_users_responded_tweet(tweetsId, user):
    userTw = api.user_timeline(user)
    for tweet in userTw:
        for id_ in tweetsId:
            if tweet.in_reply_to_status_id == id_:
                u = api.get_user(tweet.id)
                if u.id not in users:
                    users.append(u.id)





def populate_csv_file(users):
# With a given list of users creates the csv file
    with open('tweets_data.csv', 'w') as f:
        the_writer = csv.writer(f)
        the_writer.writerow(['users ids'])
        for user in users:
            the_writer.writerow([user])