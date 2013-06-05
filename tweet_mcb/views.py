import json

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from mcb_website.utils.view_util import get_common_lookup, is_user_in_group
from tweet_mcb.forms import TweetForm
from tweet_util.url_shortener import shorten_url
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def view_tweet_success(request):
    return view_tweet_console(request, success_msg=True)
    
    
    
TWEET_GROUP_NAME = 'TWEET_GROUP'
def view_tweet_console(request, **kwargs):
    """
    Success page after report form has been filled out.
    """
    #lu = get_common_lookup(request)
    lu = { 'page_title' : 'Send MCB Tweet'\
            , 'TWEET_SUCCESS' : kwargs.get('success_msg', False)
      }
     
        
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')
    
    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')

    if request.method=='POST':        
        tweet_form = TweetForm(request.POST)
        if tweet_form.is_valid():
            tweet_form.send_tweet()
            return HttpResponseRedirect(reverse('view_tweet_success', args=()))
        else:
            print 'NOT valid!'
            lu.update({ 'ERR_form_not_valid' : True })
    else: 
        tweet_form = TweetForm()#**kw={ 'resources' : resources})

    lu.update({ 'tweet_form' : tweet_form\
        #,   'my_checked_codes' : get_previously_checked_expense_codes(request)\
     })

    return render_to_response('tweet/tweet_console.html', lu, context_instance=RequestContext(request))

def view_upcoming_events(request):
    """
    Success page after report form has been filled out.
    """
    #lu = get_common_lookup(request)
    lu = { 'page_title' : 'Send MCB Tweet'\
      }
      
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')
    
    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')


    return HttpResponse('view_upcoming_events')

    return render_to_response('tweet/tweet_console.html', lu, context_instance=RequestContext(request))


def view_ajax_shorten_url(request):
    
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')

    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')

    if not request.GET.has_key('lnk'):
        json_response = { 'success' : 0, 'err_msg':'Link not found'}
        return HttpResponse(json.dumps(json_response), mimetype="application/json")
    
    long_url = request.GET['lnk']
    
    # (1) Is the URL Valid? (regex check)
    url_validator = URLValidator()
    try:
        if not long_url.lower().startswith('http'):
            url_validator('http://%s' % long_url)        
        else:
            url_validator(long_url)
    except ValidationError, e:
        json_response = { 'success' : 0, 'err_msg':'Please enter a valid url.'}
        return HttpResponse(json.dumps(json_response), mimetype="application/json")
    
    # (2) Shorten the URL
    short_url = shorten_url(long_url)
    if short_url is None:
        json_response = { 'success' : 0, 'err_msg':'Failed to shorten the url'}
    else:
        json_response = { 'success' : 1, 'short_url':short_url}
    
    return HttpResponse(json.dumps(json_response), mimetype="application/json")
    