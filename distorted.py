from TwitterAPI import TwitterAPI
import pprint
import json
import configparser
import os

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

r = api.request('statuses/filter', {'track':'#MAGA', 'filter':'twimg'})
for item in r.get_iterator():
    if 'text' in item:
        pprint.pprint(item['user']['screen_name'])
        pprint.pprint(item['text'])
        twitter_entities = {}
        try:
            twitter_entities = item['retweeted_status']['entities']
        except KeyError:
            print("not a retweet")

        if not twitter_entities:
            try:
                twitter_entities = item['quoted_status']['entities']
            except KeyError:
                print("not quoted")
                #pprint(item[])
                #entities = item['entities']

        pprint(len(twitter_entities)) #entities['media'][0]['media_url']
        #for tag in entities['hashtags']:
        #    pprint(tag)
        break
    elif 'message' in item and item['code'] == 88:
        print('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])
        break
