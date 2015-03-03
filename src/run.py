import tweepy
from tweepy import OAuthHandler
import json
import wget

consumer_key = 'YOUR-CONSUMER-KEY'
consumer_secret = 'YOUR-CONSUMER-SECRET'
access_token = 'YOUR-ACCESS-TOKEN'
access_secret = 'YOUR-ACCESS-SECRET'

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
	more_tweets = api.user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True, max_id=last_id)
	if (last_id == more_tweets[-1].id):
		break
	else:
		last_id = more_tweets[-1].id
		tweets = tweets + more_tweets

media_files = set()
for status in tweets:
	media = status.entities.get('media', []) 
	if(len(media) > 0):
		media_files.add(media[0]['media_url'])

for media_file in media_files:
	wget.download(media_file)