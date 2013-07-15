from mcb_twitter.tweet_mcb.models import MCBTweetEvent
from mcb_twitter.tweet_mcb.forms import MAX_TWEET_SIZE

from django import forms
from django.conf import settings
from tweet_mcb.tweeter import post_new_tweet
from mcb_twitter.tweet_mcb.tweeter import assemble_full_tweet

MAX_TWEET_SIZE = 140
class TweetAdminForm(forms.ModelForm):
        
    def clean(self):
        tweet_text = self.cleaned_data.get('tweet_text', None)
        tweet_short_url = self.cleaned_data.get('tweet_short_url', None)
        tweet_tag_text = self.cleaned_data.get('tweet_tag_text', None)
        
        full_tweet = assemble_full_tweet(tweet_text, tweet_short_url, tweet_tag_text)
        if full_tweet is None:
            err_msg = 'This field is required'
            raise forms.ValidationError("Please enter Tweet Text.")
            
        if len(full_tweet) > 140:
            err_msg = 'Please reduce the length of your message, hashtag or link'
            
            self._errors['tweet_text'] = self.error_class([err_msg])
            self._errors['tweet_short_url'] = self.error_class([err_msg])
            self._errors['tweet_tag_text'] = self.error_class([err_msg])
            
            raise forms.ValidationError("Your full message is more than %s characters (including links and hashtags).  Please reduce it." % MAX_TWEET_SIZE)
            
        return self.cleaned_data
        
    class Meta:
        widgets = {  'tweet_text': forms.TextInput(attrs={'size': 140})                    
                      #    , 'location': forms.TextInput(attrs={'size': 50}) 
                          #, 'start_date': forms.TextInput(attrs={'size': 10}) 
                          #, 'end_date': forms.TextInput(attrs={'size': 10}) 
                       #   , 'email': forms.TextInput(attrs={'size': 11}) 
                        #  , 'phone': forms.TextInput(attrs={'size': 10}) 
                      }


