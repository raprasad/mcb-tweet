from django.conf.urls.defaults import *


urlpatterns = patterns(
    'mcb_twitter.tweet_mcb.views'
    , url(r'^console/$', 'view_tweet_console', name='view_tweet_console')

    , url(r'^console-tweeted/$', 'view_tweet_success', name='view_tweet_success')

    , url(r'^shorten-url/$', 'view_ajax_shorten_url', name='view_ajax_shorten_url')

)

urlpatterns += patterns(
    'mcb_twitter.tweet_mcb.views_news'
 
    , url(r'^news/$', 'view_news_tweet', name='view_news_tweet')
    
)


urlpatterns += patterns(
    'mcb_twitter.tweet_mcb.views_events'
 
    , url(r'^events/$', 'view_event_list', name='view_event_list')
    
)

