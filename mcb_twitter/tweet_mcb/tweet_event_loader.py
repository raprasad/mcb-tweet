import copy
from datetime import date, datetime, time, timedelta

from mcb_website.events.models import CalendarEvent

from mcb_twitter.tweet_mcb.models import TweetStatus, MCBTweetEvent, TWEET_STATUS_PK_APPROVED
from mcb_twitter.tweet_mcb.tweeter import post_new_tweet

EVENT_KEYWORDS = ['seminar', 'lecture', 'forum']
def is_potential_lecture(event_title):
    global EVENT_KEYWORDS
    
    if event_title is None:
        return False
    
    event_title = event_title.lower()
    for event_keyword in EVENT_KEYWORDS:
        if event_keyword in event_title:
            return True
    return False


"""
from mcb_twitter.tweet_mcb.tweet_event_loader import *
#MCBTweetEvent.objects.all().delete()
load_upcoming_tweet_events()


for evt in MCBTweetEvent.objects.all():
    if not evt.tweet_short_url:
        evt.mcb_event.save()
        if evt.mcb_event.short_url:
            evt.tweet_short_url = evt.mcb_event.short_url
            evt.save()
            print 'update short url: %s' % evt.tweet_short_url
"""

def delete_tweets_of_removed_future_events():
    pass
    #today = datetime.now()

    #loaded_event_ids_of_tweet = MCBTweetEvent.objects.values_list('mcb_event__google_id', flat=True).all()

def load_upcoming_tweet_events():
    
    
    # so we don't reload events
    loaded_tweet_google_ids = MCBTweetEvent.objects.values_list('google_id', flat=True).exclude(google_id='')
    #print 'loaded_tweet_google_ids', loaded_tweet_google_ids
    # retrieve new future events
    today = datetime.now()
    
    events_to_add = CalendarEvent.objects.filter(start_time__gte=today\
                            , visible=True\
                        ).exclude(google_id__in=loaded_tweet_google_ids)
    
    # process events: 
    #  - Iterate through upcoming CalendarEvent objects and create MCBTweetEvent objects
    #   - For lectures and seminars, create 2 MCBTweetEvent objects:
    #           - 1 for the event day
    #           - 1 for a week before the event day
    #
    new_tweet_cnt = 0
    new_tweets = []
    for cal_evt in events_to_add:
        mcb_tweet = MCBTweetEvent.create_tweet_from_calendar_event(cal_evt) 
        new_tweets.append(mcb_tweet)
        new_tweet_cnt +=1
        if is_potential_lecture(cal_evt.title) or is_potential_lecture(cal_evt.description):
            #print '\nYes! potential lecture: %s' % cal_evt.title
            one_week_notice_date = mcb_tweet.tweet_pubdate + timedelta(days=-7)
            #print 'one_week_notice_date: [%s] today [%s]' % (one_week_notice_date, today)
            if one_week_notice_date > today:
                mcb_tweet_copy = copy.copy(mcb_tweet)                
                mcb_tweet_copy.tweet_pubdate = one_week_notice_date
                mcb_tweet_copy.tweet_text = 'Next Week! %s' % mcb_tweet.tweet_text[:129]
                mcb_tweet_copy.id = None
                mcb_tweet_copy.save()
                new_tweets.append(mcb_tweet_copy)
                
                new_tweet_cnt+=1
                print 'new text: %s' % mcb_tweet_copy.tweet_text
    return new_tweets
    
"""
from mcb_twitter.tweet_mcb.tweet_event_loader import *
send_daily_tweets()
"""        
def send_daily_tweets():
    
    today = date.today()
    start_time = datetime.combine(date.today(), time.min)
    end_time = datetime.combine(date.today(), time.max)

    kwargs = {  'tweet_pubdate__gte' : start_time\
                , 'tweet_pubdate__lte' : end_time\
                , 'status__id' : TWEET_STATUS_PK_APPROVED
            }
    todays_tweets = MCBTweetEvent.objects.filter(**kwargs)
    
    msgs = []
    cnt =0 
    for tweet_event in todays_tweets:
        cnt+=1
        print '(%s) sending tweet id:%s - %s' % (cnt, tweet_event.id, tweet_event)
        post_new_tweet(tweet_event.full_tweet)
        tweet_event.set_status_to_tweeted_without_save()
        tweet_event.save()
        msgs.append('(%s) %s' % (cnt, tweet_event.full_tweet))
        
    return msgs
        
    
        
        
        
        
        
        