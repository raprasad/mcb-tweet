import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from mcb_twitter.tweet_util.group_util import is_user_in_group
from mcb_twitter.tweet_mcb.forms import TweetForm
from mcb_twitter.tweet_util.url_shortener import shorten_url
from mcb_twitter.tweet_mcb.models import MCBTweetEvent, TWEET_GROUP_NAME

def view_event_list(request, **kwargs):
    """
    Success page after report form has been filled out.
    """
    #lu = get_common_lookup(request)
    lu = { 'page_title' : 'MCB Event Tweets'\
            , 'IS_TWEET_EVENT_PAGE' : True
            , 'TWEET_SUCCESS' : kwargs.get('success_msg', False)
      }
        
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')
    
    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')
 
    upcoming_events = MCBTweetEvent.get_events_awaiting_approval()
            
    lu.update({ 'upcoming_events' : upcoming_events\
        #,   'my_checked_codes' : get_previously_checked_expense_codes(request)\
     })
    #
    return render_to_response('tweet/events/event_list.html', lu, context_instance=RequestContext(request))

def get_httpresponse_json_err(msg):
    d = { 'status' : 0, 'msg' : msg}
    return HttpResponse(json.dumps(d)\
                        , content_type="application/json")
    
def view_ajax_schedule_tweet(request, tweet_event_id=None):
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')
    
    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')
    
    try:
        tweet_event = MCBTweetEvent.objects.get(pk=tweet_event_id)
    except MCBTweetEvent.DoesNotExist:
        return get_httpresponse_json_err('Tweet Event not found')
        
    if tweet_event.approved:
        return get_httpresponse_json_err('Tweet Event already approved')

    if tweet_event.reject_tweet:
        return get_httpresponse_json_err('Tweet Event already rejected')
        
      
    tweet_event.approve_tweet_without_save()
    tweet_event.save()
    
    msg = 'Scheduled for %s' % tweet_event.tweet_pubdate.strftime('%m/%d/%y')
    d = { 'status' : 1\
        , 'msg' : msg\
        }
    
    return HttpResponse(json.dumps(d), content_type="application/json")
    

def view_ajax_reject_tweet(request, tweet_event_id=None):
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')

    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')

    try:
        tweet_event = MCBTweetEvent.objects.get(pk=tweet_event_id)
    except MCBTweetEvent.DoesNotExist:
        return get_httpresponse_json_err('Tweet Event not found')

    if tweet_event.approved:
        return get_httpresponse_json_err('Tweet Event already approved')

    if tweet_event.reject_tweet:
        return get_httpresponse_json_err('Tweet Event already rejected')


    tweet_event.reject_tweet_without_save()
    tweet_event.save()

    msg = 'Rejection confirmed'
    d = { 'status' : 1\
        , 'msg' : msg\
        }

    return HttpResponse(json.dumps(d), content_type="application/json")
