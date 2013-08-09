from django.conf import settings
from twitter import *
import urllib
#import httplib2
import json
from twitter import Twitter, NoAuth, OAuth, read_token_file, TwitterHTTPError

# https://github.com/sixohsix/twitter/blob/master/tests/test_sanity.py

def assemble_full_tweet(description, short_url='', hashtag=''):
    parts = [description, short_url, hashtag]
    parts = filter(lambda x: x is not None and len(x.strip())>0, parts)
    if len(parts) == 0:
        return None
    parts = map(lambda x: x.strip(), parts)
    
    full_tweet = ' '.join(parts)
    
    return full_tweet
    
def post_new_tweet_as_parts(description, short_url, hashtag):
    new_tweet = assemble_full_tweet(description, short_url, hashtag)
    if new_tweet is None:
        return None
        
    post_new_tweet(new_tweet)

def post_new_tweet(new_tweet):
    """post status to twitter using twitter API through the twitter module
    https://twitter.com/MCB_Harvard
    """
    oauth = OAuth(*read_token_file(settings.TWITTER_OAUTH_PARAM_FILE)\
                   + (settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET))
    #               
    tweet_conn = Twitter( auth=oauth\
                    , api_version='1.1')
    
    # authentication
    #new_tweet = "%s %s #%s" % (description, short_url, hashtag)
    """example: "Harvard Professor Doug Melton discovers novel protein.
    Check it out. short_url #harvard"""
    if len(new_tweet) <= 140:
        tweet_conn.statuses.update( status = "%s" % new_tweet)
        #print 'status updated: %s' % new_tweet
        return True
    else: 
        #print "Status cannot be over 140 characters."
        return False
        
if __name__=='__main__':
    description = 'Hopi Hoekstra Appointed HHMI Investigator'
    long_url = 'https://www.mcb.harvard.edu/mcb/news/news-detail/3669/how-does-e-coli-segregate-its-sisters-without-a-spindle-kleckner-lab/'
    hashtag = "MCB_News"
    #short_url = shorten_url(long_url)
    short_url = 'http://goo.gl/TIYIg'
    post_new_tweet_as_parts(description, short_url, hashtag)
