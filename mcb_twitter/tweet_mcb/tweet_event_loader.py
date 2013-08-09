from mcb_twitter.tweet_mcb.models import TweetStatus, MCBTweetEvent
from mcb_website.events.models import CalendarEvent
from datetime import datetime, timedelta
import copy

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
MCBTweetEvent.objects.all().delete()
load_upcoming_tweet_events()
"""
def load_upcoming_tweet_events():
    
    # so we don't reload events
    loaded_event_ids_of_tweet = MCBTweetEvent.objects.values_list('mcb_event__id', flat=True).all()
    
    # retrieve new future events
    today = datetime.now()
    
    events_to_add = CalendarEvent.objects.filter(start_time__gte=today\
                            , visible=True\
                        ).exclude(id__in=loaded_event_ids_of_tweet)
    
    # process events
    for cal_evt in events_to_add:
        mcb_tweet = MCBTweetEvent.create_tweet_from_calendar_event(cal_evt) 
        
        if is_potential_lecture(cal_evt.title):
            #print '\nYes! potential lecture: %s' % cal_evt.title
            one_week_notice_date = mcb_tweet.tweet_pubdate + timedelta(days=-7)
            #print 'one_week_notice_date: [%s] today [%s]' % (one_week_notice_date, today)
            if one_week_notice_date > today:
                mcb_tweet_copy = copy.copy(mcb_tweet)                
                mcb_tweet_copy.tweet_pubdate = one_week_notice_date
                mcb_tweet_copy.tweet_text = 'Next Week! %s' % mcb_tweet.tweet_text[:129]
                mcb_tweet_copy.id = None
                mcb_tweet_copy.save()
                print 'new text: %s' % mcb_tweet_copy.tweet_text
        
        
        