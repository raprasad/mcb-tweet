from django.contrib import admin
from mcb_twitter.tweet_mcb.forms_admin import TweetAdminForm
from mcb_twitter.tweet_mcb.models import TweetStatus, MCBTweetEvent, TWEET_STATUS_PK_TWEETED

def reject_tweet(modeladmin, request, queryset):
    # Set the status of selected TweetStatus objects to rejected
    #     
    for mcb_tweet in queryset:
        mcb_tweet.reject_tweet_without_save()
        mcb_tweet.save()
    reject_tweet.short_description = "Reject Tweet(s)"
    
def set_to_awaiting_approval(modeladmin, request, queryset):
    # Set the status of selected TweetStatus objects to approveed
    #     
    for mcb_tweet in queryset.exclude(status=TWEET_STATUS_PK_TWEETED):
        mcb_tweet.set_tweet_to_awaiting_approval_without_save()
        mcb_tweet.save()
    approve_tweet.short_description = "Set to 'Awaiting Approval'"

def approve_tweet(modeladmin, request, queryset):
    # Set the status of selected TweetStatus objects to approveed
    #     
    for mcb_tweet in queryset:
        mcb_tweet.approve_tweet_without_save()
        mcb_tweet.save()
    approve_tweet.short_description = "Approve Tweet(s)"

    
    
class TweetStatusAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name', 'description' )
    list_display = ('name', 'sort_key', 'description')
    list_editable = ('sort_key',)
admin.site.register(TweetStatus, TweetStatusAdmin)


class MCBTweetEventAdmin(admin.ModelAdmin):
    actions = [approve_tweet, reject_tweet, set_to_awaiting_approval]
    form = TweetAdminForm
    save_on_top = True
    search_fields = ('tweet_text', 'status__name' )
    list_display = ('tweet_text', 'status', 'tweet_pubdate',  'approved','reject_tweet', 'tweet_tag_text' )
    list_filter = ('status', 'tweet_tag_text')
    readonly_fields = ('reject_tweet', 'approved', 'full_tweet', 'view_calendar_event',)
    
    def get_actions(self, request):
        actions = super(MCBTweetEventAdmin, self).get_actions(request)
        #if request.user.username[0].upper() != 'J':
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(MCBTweetEvent, MCBTweetEventAdmin)

