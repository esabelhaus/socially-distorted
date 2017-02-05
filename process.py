from nltk.corpus import movie_reviews
from pymongo import MongoClient

client = MongoClient()
db = client.twitter

all_tweets = db.all
maga_tweets = db.maga

def movie_words(sentiment):
    sentiment_words = movie_reviews.fileids(sentiment)
    words = {}
    for file_id in sentiment_words:
        for word in movie_reviews.words(file_id):
            words[word.lower()] = True

    return words

neg_dict = movie_words('neg')
pos_dict = movie_words('pos')

def evaluate(tweet):

    words = tweet.split()

    negfeats = []
    posfeats = []
    neutfeats = []
    counter = 0
    for word in words:
        pre = counter
        if word in neg_dict:
            negfeats.append(word.lower())
            counter += 1

        if word in pos_dict:
            posfeats.append(word.lower())
            counter += 1

        # Some words may not be contained in the Movie Reviews corpus.
        # These words must be stored some way for later analysis.
        # The length must also be subtracted from the processed words
        # in order to get an accurate percentage of negative vs positive
        if counter == pre:
            neutfeats.append(word)

    # determined the number of words processed
    processed_count = len(words) - len(neutfeats)

    percent_neg = 0
    percent_pos = 0

    # determine the % negative
    if len(negfeats) > 0:
        percent_neg = len(negfeats) / processed_count


    # determine the % positive
    if len(posfeats) > 0:
        percent_pos = len(posfeats) / processed_count

    if percent_neg > percent_pos:
        return('neg')
    elif percent_neg == percent_pos:
        return('neut')
    else:
        return('pos')

all_total_processed=0
all_total_neg=0
all_total_pos=0
all_total_neut=0

for tweet in all_tweets.find():
    if 'text' in tweet:
        sentiment = evaluate(tweet['text'])
        all_total_processed += 1
        if 'neg' == sentiment:
            all_total_neg += 1
        elif 'pos' == sentiment:
            all_total_pos += 1
        else:
            all_total_neut += 1

print("[ALL] total processed: " + str(all_total_processed))
print("[ALL] total neg: " + str(all_total_neg))
print("[ALL] total pos: " + str(all_total_pos))
print("[ALL] total neut: " + str(all_total_neut))

maga_total_processed=0
maga_total_neg=0
maga_total_pos=0
maga_total_neut=0

for tweet in maga_tweets.find():
    if 'text' in tweet:
        sentiment = evaluate(tweet['text'])
        maga_total_processed += 1
        if 'neg' == sentiment:
            maga_total_neg += 1
        elif 'pos' == sentiment:
            maga_total_pos += 1
        else:
            maga_total_neut += 1

print("[MAGA] total processed: " + str(maga_total_processed))
print("[MAGA] total neg: " + str(maga_total_neg))
print("[MAGA] total pos: " + str(maga_total_pos))
print("[MAGA] total neut: " + str(maga_total_neut))
