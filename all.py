from TwitterAPI import TwitterAPI
import configparser
import os
from pymongo import MongoClient

# initialize mongo connection, set collection
client = MongoClient()
db = client.twitter
collection = db.all

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
r = api.request('statuses/sample')
# iterate over incoming tweets from filter
for item in r.get_iterator():
    # initialize data for dynamic population conditionally
    tweet = {}
    if 'message' in item and item['code'] == 88:
        print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        break

    if 'text' in item:
        tweet['text'] = item['text']

    if 'user' in item:
        tweet['screen_name'] = item['user']['screen_name']
        tweet['name'] = item['user']['name']
        tweet['profile_img_url'] = item['user']['profile_image_url']

    if 'retweeted' in item:
        tweet['retweeted'] = item['retweeted']

    if 'retweeted_status' in item:
        tweet['entities'] = item['retweeted_status']['entities']

    if 'quoted_status' in item:
        tweet['entities'] = item['quoted_status']['entities']

    if 'entities' in item:
        tweet['entities'] = item['entities']

    collection.insert_one(tweet)
