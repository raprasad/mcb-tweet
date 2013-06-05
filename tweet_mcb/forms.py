from django import forms
from django.conf import settings
from tweet_mcb.tweeter import post_new_tweet

MAX_TWEET_SIZE = 140
class TweetForm(forms.Form):
    message = forms.CharField(label="Enter tweet"\
            , help_text="" 
            , widget=forms.Textarea(attrs={'rows':'2'\
                                , 'style':'width:300px'\
                                , 'class' : 'input-xlarge'\
                                , 'maxlength' : '120'\
                                , 'placeholder' : ''\
                                , 'data-provide' : 'limit'\
                                , 'data-counter' : '#msg_counter'\
                                })\
            )                    
    hashtag = forms.CharField(initial='#MCB_Event')
    link = forms.URLField(initial=''\
                        , required=False\
                        , widget=forms.TextInput(attrs={'size': 50 })\
                        ) 
 
 
    def send_tweet(self):
        full_msg = self.get_full_message()
        if full_msg is None:
            return None
            
        return post_new_tweet(full_msg) 
        
    def get_full_message(self):
        if not self.cleaned_data:
            return None
        
        message = self.cleaned_data.get('message', None)
        if message is None:
            return None
            
        hashtag = self.cleaned_data.get('hashtag', '')
        if message is None:
            return None

        link = self.cleaned_data.get('link', '')

        if len(link) > 0: 
            link = ' %s' % link
        return '%s %s%s' % (message, hashtag, link)
        
        
        
    def clean(self):
        
        full_msg = self.get_full_message()
        if full_msg is None:
            raise forms.ValidationError("Please enter at least a message and a hashtag.")
            
        print 'len(full_msg)', len(full_msg) 
        if len(full_msg) > MAX_TWEET_SIZE:
            err_msg = 'Please reduce the length of your message, hashtag or link'
            self._errors['message'] = self.error_class([err_msg])
            self._errors['hashtag'] = self.error_class([err_msg])
            self._errors['link'] = self.error_class([err_msg])

            raise forms.ValidationError("Your full message is more than %s characters (including links and hashtags).  Please reduce it." % MAX_TWEET_SIZE)
            

        return self.cleaned_data
        
        