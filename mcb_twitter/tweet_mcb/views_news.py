from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from mcb_twitter.tweet_util.group_util import is_user_in_group
from mcb_twitter.tweet_mcb.models import TWEET_GROUP_NAME
from mcb_twitter.tweet_mcb.views import view_tweet_console, TITLE_KEY, SHORT_URL_KEY 

def get_tweet_news_url(title, short_url=''):
    if title is None:
        return None
        
    params = '%s=%s&%s=%s' % (TITLE_KEY, str(title).strip(), SHORT_URL_KEY, str(short_url).strip() )
    
    return '%s?%s' % ( reverse('view_news_tweet', args=()), params)
    
def view_news_tweet(request):
    """
    http://127.0.0.1:8000/mcb/tweet/news/?t=Murray%20Lab&su=www.google.com
    http://127.0.0.1:8000/mcb/tweet/news-tweet/t=Murray Lab&su=www.google.com
    ?t=(some title)&su=(short url)
    """
    #print 'NEWS'
    if not request.user.is_authenticated():
        return HttpResponse('not logged in')

    if not is_user_in_group(request, TWEET_GROUP_NAME):
        return HttpResponse('not in tweet group')

    if not (request.GET.has_key(TITLE_KEY) and request.GET.has_key(SHORT_URL_KEY)):
        print 'keys not found!'
        return view_tweet_console(request)
        
    #print 'title', request.GET[TITLE_KEY]
    #print 'SHORT_URL_KEY', request.GET[SHORT_URL_KEY]
    return view_tweet_console(request\
                            , title=request.GET[TITLE_KEY]
                            , short_url=request.GET[SHORT_URL_KEY]\
                            )
