from django.conf import settings
from twitter import *
import urllib
#import httplib2
import json
from twitter import Twitter, NoAuth, OAuth, read_token_file, TwitterHTTPError

# https://github.com/sixohsix/twitter/blob/master/tests/test_sanity.py
MAX_TWEET_LENGTH = 140

def shorten_tweet_to_fit_url_and_tag(title, max_length=MAX_TWEET_LENGTH, add_ellipsis=False):
    """
    Shorten the title to a target length.
    Example:
        tag length: 10      '#MCB_Event'
        link length: 20     'http://goo.gl/sTbpGG'
        spacing between title/link/tag = 2
        
        title max length: 140 - (10 + 20 + 2) = 108
    """
    if title is None:
        return None
            
    if len(title) <= max_length:
        return title
    
    ellipsis_str = '...'
    
    if add_ellipsis:
        max_length = max_length - 3
        
    # trim last words from title
    tparts = title.split()
    if len(tparts) == 1:       # Is it contiguous characters?  Yes, truncate it
        if add_ellipsis:
            return title[:max_length] + ellipsis_str
        return title[:max_length]
    
    # Try pulling off the end words, until target length reaached
    #   example: "cow jumped over the moon"
    #               length: 24; target length: 16
    #       "cow jumped over the moon" - nope
    #       "cow jumped over the" - nope, length 19
    #       "cow jumped over" - YES, length 15; 15<=16     
    ""   
    for idx in range(1, len(tparts)):
        shortened_title = ' '.join(tparts[0:-idx])  
        if len(shortened_title) <= max_length:
            if add_ellipsis:
                return shortened_title + ellipsis_str
            return shortened_title
            
    # should never reach here
    return title[:max_length]  


def assemble_full_tweet(description, short_url='', hashtag=''):
    """
    Shorten tweet to 140 characters.
    """
    parts = [description, short_url, hashtag]
        
    parts = filter(lambda x: x is not None and len(x.strip())>0, parts)
    if len(parts) == 0:
        return None
    
    parts = map(lambda x: x.strip(), parts)
    
    if len(parts) == 1:
        updated_description = shorten_tweet_to_fit_url_and_tag(\
                                        parts[0]\
                                      , MAX_TWEET_LENGTH)
        return updated_description
        
    num_spaces_between_parts = len(parts) - 1
    non_description_length = len(''.join(parts[1:])) + num_spaces_between_parts
    
    # Are the links, hashtags too long?  Then start dropping them
    if non_description_length > (MAX_TWEET_LENGTH/2):
        while len(parts) > 1:
            parts.pop()
            num_spaces_between_parts = len(parts) - 1
            non_description_length = len(''.join(parts[1:])) + num_spaces_between_parts
            if non_description_length <= (MAX_TWEET_LENGTH/2):
                break
                
    max_description_length = MAX_TWEET_LENGTH - non_description_length

    updated_description = shorten_tweet_to_fit_url_and_tag(parts[0]\
                                    , max_description_length\
                                    , add_ellipsis=True)
    
    if len(parts) == 1:
        return updated_description
        
    full_tweet = updated_description + ' ' + ' '.join(parts[1:])
    
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
    hashtag = "#MCB_News"
    #short_url = shorten_url(long_url)
    short_url = 'http://goo.gl/TIYIg'
    post_new_tweet_as_parts(description, short_url, hashtag)
