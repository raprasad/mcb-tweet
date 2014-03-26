"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from tweet_mcb.tweeter import assemble_full_tweet, shorten_tweet_to_fit_url_and_tag, MAX_TWEET_LENGTH

class TweetLengthTest(TestCase):

    test_title_01 = 'Next Week! Eva Nogales, HHMI Investigator: "High-Resolution Structures of Microtubules towards a Mechanistic Understanding of Dynamic Instability" (MCB Thursday Seminar Series)'

    test_title_02 = 'The cow jumped over the moon'
    
    def test_tweet_sizes(self):
        """
        Test title too long, should truncate it by chopping off words
        Tested with and without ellipsis add to end
        """
        expected_result1 = 'Next Week! Eva Nogales, HHMI Investigator: "High-Resolution Structures of Microtubules towards a Mechanistic Understanding of Dynamic'

        t1 = shorten_tweet_to_fit_url_and_tag(self.test_title_01, max_length=MAX_TWEET_LENGTH, add_ellipsis=False)
        self.assertEqual(t1, expected_result1)

        #----------------------------------------------
        # with 'add_ellipsis=True'

        expected_result2 = 'Next Week! Eva Nogales, HHMI Investigator: "High-Resolution Structures of Microtubules towards a Mechanistic Understanding of Dynamic...'
        t2 = shorten_tweet_to_fit_url_and_tag(self.test_title_01, max_length=MAX_TWEET_LENGTH, add_ellipsis=True)
        self.assertEqual(t2, expected_result2)


    def test_title_size2(self):
        
        expected_result1 = 'The cow'
        t1 = shorten_tweet_to_fit_url_and_tag(self.test_title_02, max_length=10, add_ellipsis=False)
        self.assertEqual(t1, expected_result1)

        #----------------------------------------------

        expected_result2 = 'The cow...'
        t2 = shorten_tweet_to_fit_url_and_tag(self.test_title_02, max_length=10, add_ellipsis=True)
        self.assertEqual(t2, expected_result2)
        
    
    def test_tweet_assembly(self):
        # assemble_full_tweet(description, short_url='', hashtag=''):
        d = 'You can help make a difference on the issues that matter to you'
        u = 'http://t.co/0123456789'
        ht = '#MCB_Event'
        
        expected_result = ' '.join([d, u, ht ]) 
        r1 = assemble_full_tweet(d, short_url=u, hashtag=ht)
        self.assertEqual(r1, expected_result)
        
        #----------------------------------------------
        # description too long (description is "doubled")
        #----------------------------------------------
        d2 = 'You can help make a difference on the issues that matter to youYou can help make a difference on the...'
        expected_result = ' '.join([d2, u, ht ]) 
        r2 = assemble_full_tweet(d * 2, short_url=u, hashtag=ht)
        self.assertEqual(r2, expected_result)
        
        #----------------------------------------------
        # hashtag too long, should get removed
        #----------------------------------------------
        long_ht = 'ht' * 70
        expected_result = ' '.join([d, u ]) 
        r3 = assemble_full_tweet(d, short_url=u, hashtag=long_ht)
        self.assertEqual(r3, expected_result)

        #----------------------------------------------
        # url too long, url and hashtag should get removed.  
        #----------------------------------------------
        long_u = 'lnk' * 50
        expected_result = ' '.join([d]) 
        r4 = assemble_full_tweet(d, short_url=long_u, hashtag=ht)
        self.assertEqual(r4, expected_result)
        
        #----------------------------------------------
        # Everything is too long
        #----------------------------------------------
        expected_result = ' '.join([d*2]) + 'You can...'
        r5 = assemble_full_tweet(d*3, short_url=long_u, hashtag=ht)
        self.assertEqual(r5, expected_result)
        
        

