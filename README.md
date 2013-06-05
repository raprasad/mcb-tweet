mcb-tweet
=========

Twitter app for the MCB Website (Pre-format tweets of events and news stories)

# Dependencies
Python Twitter API https://github.com/sixohsix/twitter
Bootstrap http://twitter.github.io/bootstrap/
    The templates uses the bootstrap assets, v2.3.1.  
    Theses files are in the the static_files directory

# Set-up
## Needed in the settings file
    TWITTER_CONSUMER_KEY  = 'the key'
    TWITTER_CONSUMER_SECRET  = 'the secret'
    TWITTER_OAUTH_PARAM_FILE = 'full path to the oauth param file'
    (for TWITTER_OAUTH_PARAM_FILE, see example https://github.com/sixohsix/twitter/blob/master/tests/oauth_creds)
