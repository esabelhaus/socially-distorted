from TwitterAPI import TwitterAPI
import pprint
import json
import configparser
import os
from pymongo import MongoClient

# initialize mongo connection, set collection
client = MongoClient()
db = client.test_database
collection = db.tweets

# create a config object
config = configparser.ConfigParser()
# get the current directory of THIS file at runtime
dir_path = os.path.dirname(os.path.realpath(__file__))

# read in configuration file
config.read(dir_path + '/config/auth')

# populate auth block from config
consumer_key =         config['twitter']['c_key']
consumer_secret =      config['twitter']['c_secret']
access_token_key=api = config['twitter']['a_key']
access_token_secret =  config['twitter']['a_secret']

# instantiate twitter api using auth block above
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

# instantiate stream from filter endpoint, filter on Make America Great Again
r = api.request('statuses/filter', {'track':'#MAGA'})
# iterate over incoming tweets from filter
for item in r.get_iterator():
    # initialize data for dynamic population conditionally
    tweet_entities = {}
    screen_name = ""
    name = ""
    tweet_text = ""
    profile_img_url = ""
    if 'message' in item and item['code'] == 88:
        print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        break

    if 'text' in item:
        #pprint.pprint(item['text'])
        tweet_text = item['text']

    if 'user' in item:
        #pprint.pprint(json.dumps(item['user']))
        screen_name = item['user']['screen_name']
        name = item['user']['name']
        profile_img_url = item['user']['profile_image_url']

    if 'retweeted_status' in item:
        #pprint.pprint(json.dumps(item['retweeted_status']['entities']))
        tweet_entities = item['retweeted_status']['entities']

    if 'quoted_status' in item:
        #pprint.pprint(json.dumps(item['quoted_status']['entities']))
        tweet_entities = item['quoted_status']['entities']

    if 'entities' in item:
        tweet_entities = item['entities']

    tweet = {}
    tweet['screen_name'] = screen_name
    tweet['name'] = name
    tweet['entities'] = tweet_entities
    tweet['profile_img_url'] = profile_img_url
    tweet['text'] = tweet_text
    #pprint.pprint(json.dumps(tweet))
    collection.insert_one(tweet)
