from django.db import models
from django.core.urlresolvers import reverse 

from mcb_website.events.models import CalendarEvent
from mcb_twitter.tweet_mcb.tweeter import assemble_full_tweet

TWEET_STATUS_PK_AWAITING_APPROVAL = 1
TWEET_STATUS_PK_APPROVED = 2
TWEET_STATUS_PK_REJECTED = 3
TWEET_STATUS_PK_TWEETED = 4



class TweetStatus(models.Model):
    name = models.CharField(max_length=200, unique=True)
    sort_key = models.IntegerField()
    description = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ('sort_key', 'name')
        verbose_name_plural = 'Tweet statuses'
    
    
class MCBTweetEvent(models.Model):
    """
    Pre-load CalendarEvents for tweeting
    """
    mcb_event = models.ForeignKey(CalendarEvent, verbose_name='MCB Event')
    tweet_text = models.CharField(max_length=140)
    status = models.ForeignKey(TweetStatus)
    
    reject_tweet = models.BooleanField(default=False, help_text='auto-filled on save')
    approved = models.BooleanField(default=False, help_text='auto-filled on save')
    
    tweet_pubdate = models.DateTimeField()
    
    tweet_tag_text = models.CharField(max_length=75, default='#MCB_Event', blank=True)
    tweet_short_url = models.URLField(max_length=75, blank=True)
    
    full_tweet = models.CharField(max_length=255, blank=True, help_text='auto-filled on save')
    
    @staticmethod
    def create_tweet_from_calendar_event(cal_event):
        status_awaiting_approval = TweetStatus.objects.get(pk=TWEET_STATUS_PK_AWAITING_APPROVAL)
        mcb_tweet = MCBTweetEvent(mcb_event=cal_event\
                                , status=status_awaiting_approval\
                                , tweet_text=cal_event.title[:140]\
                                , tweet_pubdate=cal_event.start_time\
                                , tweet_short_url = cal_event.short_url\
                                )
            
        mcb_tweet.save()
        return mcb_tweet
    
    def view_mcb_event(self):
        #return 'balh'
        if not self.mcb_event:
            return 'n/a'
            
        lnk = reverse('admin__events__calendarevent__change', args=(self.mcb_event.id))
        return '<a href="%s">view event</a>' % lnk
        
    view_mcb_event.allow_tags = True
    
    def get_full_tweet(self):
        full_tweet = assemble_full_tweet(self.tweet_text\
                                        , self.tweet_short_url\
                                        , self.tweet_tag_text)
        if len(full_tweet) <= 140:
            return full_tweet
            
        full_tweet = assemble_full_tweet(self.tweet_text\
                                            , self.tweet_short_url\
                                    )
        if len(full_tweet) <= 140:
            return full_tweet

        if self.tweet_text <= 140:
            return self.tweet_text
        
        return self.tweet_text[:140]
        
            
            
            
    def save(self, *args, **kwargs):
        self.full_tweet = self.get_full_tweet()
        
        if self.full_tweet is None:
            self.full_tweet = '' 

        if self.status.id == TWEET_STATUS_PK_REJECTED:
            self.reject_tweet = True                              
        else:
            self.reject_tweet = False 
    
        if self.status.id in (TWEET_STATUS_PK_APPROVED, TWEET_STATUS_PK_TWEETED) :
            self.approved = True
        else:
            self.approved = False 


        super(MCBTweetEvent, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return '%s' % self.tweet_text
        
    class Meta:
        verbose_name = 'MCB Tweet Event'
        ordering = ('status__sort_key', '-tweet_pubdate', 'tweet_text')