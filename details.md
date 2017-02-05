# Socially Distorted

a data science experiment to determine whether Make America Great Again is intrinsically a negative sentiment

## Hypothesis

My hypothesis is that tweets associated with Make America Great Again are statistically more negative than the stream of all tweets including tweets associated with Make America Great Again

## Limitations

I will be unable to determine whether a tweet contains MAGA for the "all tweets" collection, this is by design

I will not be able to determine context if a tweet is a reply

I am limited to the tweets provided through the sample feed for the control group

Due to the nature of tweets, some which are sparse text with images will not be useful metrics

## P-value

The value of statistical significance for this hypothesis is .05

## Strategy

### Gathering

For the control sample, I will use the 'streams/sample' endpoint

For the test sample, I will use the 'streams/filter' and pass in a single filter of `{'track':'#MAGA'}`

### Pre-Processing

Due to the diverse nature of tweets, I've defined an algorithm which determines the contents of a tweet, and then extracts the actionable information within.

#### Data being collected:

* Name
 * I may also look at whether the name of the user is a negative sentiment
 * May also be helpful for classification of new sentiments
* Screen Name
 * Used to gather associative properties for analysis of who uses which hashtags how often
* Profile Image URL
 * Potential for analyzing profile image for comparison, eg. how many people have "this" profile photo
* Text
 * This is the bulk of the analysis, raw text.
 * May require translation possibly, not sure on that yet.
* Entities
 * For retweets and quoted tweets, this will contain the text of the original tweet for concatenation with the tweet being inspected.
 * This attribute can also be good for gathering images to associate with potentially negative/positive tweets
  * I may use this for another study using image analysis
* Is it a retweet or quoted tweet
 * allows for further inspection to gather the text attribute of the original tweet

### Storage

In an effort to quickly store and access tweets in a semi-uniform fashion, I'm using MongoDB to store the collections respectively by type

The control collection will be `db.twitter.all`

The test collection will be `db.twitter.maga`

The data will be collected as a dict(), and stored as JSON in MongoDB

### Comparison Method

Using the Movie Reviews corpus from NLTK, I will create two dict() structures containing positive and negative words respectively

The algorithm will split the contents of the tweet(plus sub-tweet if available) on any whitespace

The algorithm will then iteratively loop over words within the tweet, and determine if the word exists in the positive, negative, or neither dict().

Once the loop has completed, the algorithm will subtract the number of words which did not exist in either dict(), as they are extraneous to the calculation of positive or negative in this context

The algorithm will divide the number of negative words by the total number of words processed(minus unknowns) and multiply this by 100

The value of this result will determine sentiment classification of the tweet being inspected, and the result will be upserted to MongoDB with the addition of the array of positive, negative, and neutral words, as well as a boolean value to signify it has been processed

## Control

The algorithm will collect all tweets (including MAGA tweets), and perform sentiment analysis on the tweet 'text' attribute using the above comparison method defined

In an effort to determine the full sentiment of a retweet/quoted tweet, I will compose the full tweet string as a concatenation of the original tweet, as well as any retweet context added by the user.

This analysis will be used as a neutral basis with which to compare the test analysis

## Test

The algorithm will collect all MAGA tweets, and perform sentiment analysis on the tweet 'text' attribute using the above comparison method defined
