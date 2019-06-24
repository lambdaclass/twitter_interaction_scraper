import tweepy as tw
from tweepy.auth import OAuthHandler
import csv
import urllib2
import re
import os
from dotenv import load_dotenv, find_dotenv
from config import tweetsId, tweets_user


load_dotenv(find_dotenv())


CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')


auth = tw.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tw.API(auth)


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


user_likes = get_user_ids_of_post_likes('1138112412693848065')
users = []

for tweet in tweetsId:
    user_likes = get_user_ids_of_post_likes(str(tweet))
    for user_id in user_likes:
        u = api.get_user(user_id)
        users.append(u.screen_name)
    retweets = api.retweets(tweet)
    for retweet in retweets:
        u = retweet.user
        users.append(u.screen_name)

userTw = api.search_users(tweets_user)
responses = []


for tweet in userTw:
    for _id in tweetsId:
        if tweet.status.in_reply_to_status_id == _id:
            u = api.get_user(tweet.id)
            users.append(u.screen_name)


with open('tweets_data.csv', 'w') as f:
    the_writer = csv.writer(f)
    the_writer.writerow(['users'])

    for user in users:
        the_writer.writerow([user])
