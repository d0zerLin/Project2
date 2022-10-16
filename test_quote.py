import tweepy
import re
from google.cloud import language_v1
import os
import io
import pytest
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '' # google cloud credentials here

# Twitter API credentials here
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

# Tweepy authoritation
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# exclude unnecessary words such as @screen_name and URL included during searching
def format_text(text):
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('\n', " ", text)
    text=re.sub(r'@?[!-~]+', "", text)
    return text

# extract replies and quote retweets with tweetID
def get_replies_and_quotetweets(tweetID):
    status = api.get_status(tweetID)
    row = []
    # query for reply
    query_reply = '@' + status._json['user']['screen_name'] + ' exclude:retweets'
    # extract replies 
    for status_reply in api.search_tweets(q=query_reply, lang='en', count=100):
        if status_reply._json['in_reply_to_status_id'] == status._json['id']:
            row.append(format_text(status_reply._json['text']))
        else:
            continue
    # query for quote tweets 
    query_quote = status._json['id_str'] + ' exclude:retweets'
    # extract quote tweets 
    for status_quote in api.search_tweets(q=query_quote, lang='en', count=100):
        if status_quote._json['id_str'] == status._json['id_str']:
            continue
        else:
            row.append(format_text(status_quote._json['text']))
    
    return row

# take text and return sentiment score 
def analyze_nlp(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    return response.document_sentiment.score

# take denominator and numerator and return percentage in integer 
def calc_percentage(num, total):
    if (total != 0):
        return int((num/total)*100)
    else:
        return 0

# take tweetID and return the percentage of positive, negative and neutral replies and quote tweets 
def get_sentiment_of_retweets(tweetID):
    row = get_replies_and_quotetweets(tweetID)
    num_positive = 0
    num_negative = 0
    num_neutral = 0
    for retweet in row:
        sentiment_score = analyze_nlp(retweet)
        if (sentiment_score > 0):
            num_positive += 1
        elif (sentiment_score < 0):
            num_negative += 1
        else: 
            num_neutral += 1
    length = len(row)
    return calc_percentage(num_positive, length), calc_percentage(num_negative, length), calc_percentage(num_neutral, length)

# take text and return sentiment score 
def analyze_nlp(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    return response.document_sentiment.score

def print_result_sentiment(tweetID):
    num_positive, num_negative, num_neutral = get_sentiment_of_retweets(tweetID)
    print("The result of sentiment analysis of replies and quote tweets for the tweet")
    print("positive🙂: ", num_positive, "%")
    print("negative🙁: ", num_negative, "%")
    print("neutral😐: ", num_neutral, "%")

if __name__ == '__main__':
    print("Enter tweet ID you want to analyze: ") 
    tweetID = input()
    # print the result of sentiment analysis
    print_result_sentiment(tweetID)

def test_format_text():
    assert format_text("@d0zer") == ""
  
def test_get_replies_and_quotetweets():
    assert get_replies_and_quotetweets(1448674345027399681) == []

def test_calc_percentage():
    assert calc_percentage(30, 100) == 30
    assert calc_percentage(20, 0) == 0

def test_get_sentiment_of_retweets():
    assert get_sentiment_of_retweets(1448674345027399681) == (0, 0, 0)

def test_analyze_nlp():
    assert analyze_nlp("Today is a good day") == 0.8999999761581421
    assert analyze_nlp("I hate the weather of Boston") == -0.8999999761581421