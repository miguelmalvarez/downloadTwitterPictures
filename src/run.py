import tweepy
from tweepy import OAuthHandler
import json
import wget

consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'

consumer_key = 'cMCTi0MRtbjHdrrtSrI7Q'
consumer_secret = 'eTmfLHvt51RMngPM32stUVQCXtluR9XNbKU6WrUs'
access_token = '97880420-AQL6lDvSs7ZrfroBocwn5G5D5H5ZPPsBcacUn9hTd'
access_secret = 'sEJ6mEgbAB2PGeaG6VzJopS5ILWVHgiFhiAI9rTq9c'
 
# TODO: User account via shell.
username = "miguelmalvarez"

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
# User() is the data model for a user profil
tweepy.models.User.first_parse = tweepy.models.User.parse
tweepy.models.User.parse = parse
# You need to do it for all the models you need

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
 
tweets = []

tweets = api.user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True)
last_id = tweets[-1].id

while (True):
	print("call")
	more_tweets = api.user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True, max_id=last_id-1)
	if (len(more_tweets) == 0):
		break
	else:
		last_id = more_tweets[-1].id
		tweets = tweets + more_tweets

media_files = []
for status in tweets:
	media = status.entities.get('media', []) 
	if(len(media) > 0):
		media_files.append(media[0]['media_url'])

for media_file in media_files:
	wget.download(media_file)