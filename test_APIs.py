import tweepy
import csv
import json
from datetime import datetime, timedelta

# Twitter API tokens
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# num of tweets: max 200
num_tweets = 200 
# num of days ago from today
num_days = 7

def get_tweets_from_user(userID):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=userID,count=num_tweets)
    
    # write tweets info into csv file 
    csvFile = open('tweets_' + userID + '.csv', 'a')
    csvWriter = csv.writer(csvFile)
  
    tweets_from_user_list = [tweet for tweet in tweets] 
    for tweet in tweets_from_user_list:
        csvWriter.writerow([tweet.user.screen_name.encode('utf-8'), tweet.created_at, tweet.text.encode('utf-8'), tweet.user.location.encode('utf-8')])

def get_tweets_from_hashtag(hashtag):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    date = datetime.now() - timedelta(days=num_days)
    date_since = date.strftime("%Y-%m-%d")
    tweets = tweepy.Cursor(api.search, q=hashtag, since=date_since).items(num_tweets)
    
    # write tweets info into csv file 
    csvFile = open('tweets_' + hashtag  + '.csv', 'a')
    csvWriter = csv.writer(csvFile)

    tweets_from_hashtag_list = [tweet for tweet in tweets]
    for tweet in tweets_from_hashtag_list:
        csvWriter.writerow([tweet.user.screen_name.encode('utf-8'), tweet.created_at, tweet.text.encode('utf-8'), tweet.user.location.encode('utf-8'), tweet.entities['hashtags']])

if __name__ == '__main__':
    print("Enter username that you want to search for: ")
    userID = input()
    get_tweets_from_user(userID)

    # you can use this for keyword searching if you do not enter # before word
    print("Enter keyword that you want to search for: ")
    hashtag = input()
    get_tweets_from_hashtag(hashtag)