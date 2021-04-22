"""Get tweets and users from the Twitter DB"""
from os import getenv
import tweepy
import spacy
from .models import User, DB, Tweet


TWITTER_API_KEY = "?"
TWITTER_API_KEY_SECRET = "?"
TWITTER_AUTH = tweepy.OAuthHandler(
    getenv("TWITTER_API_KEY"),
    getenv("TWITTER_API_KEY_SECRET")
)
TWITTER = tweepy.API(TWITTER_AUTH)


"""Loads word2vect Model"""
nlp = spacy.load('en_core_web_sm')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

def add_or_update_user(username):
    """
    Gets Twitter user and tweets from Twitter DB
    
    Gets user by "username" param
    """
    try:
        #gets back twitter user object
        twitter_user = TWITTER.get_user(username)
        #Either updates or adds user to our DB
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, name=username)
        #adds user if not already in DB
        DB.session.add(db_user)
        
        
        #Getting tweets from "twitter_user"
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies = True,
            include_rts = False,
            tweet_mode = "extended",
            since_id = db_user.newest_tweet_id
        )

        
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
            
        # Tweets is list of tweet objects
        for tweet in tweets:
            #type(tweet) == object
            tweet_vector = vectorize_tweet(tweet.text)
            db_tweet = Tweet(
                id = tweet.id,
                text = tweet.text,
                vect = tweet_vector
            )
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
            
    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e
    else:
        DB.session.commit()