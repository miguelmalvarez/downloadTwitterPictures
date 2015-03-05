import tweepy
from tweepy import OAuthHandler
import json
import wget
import argparse
import configparser

#TODO: Limit by number of tweets?
def parse_arguments():
	parser = argparse.ArgumentParser(description='Download pictures from a Twitter feed.')
	parser.add_argument('username', type=str, help='the twitter screen name from the account we want to retrieve all the pictures')
	args = parser.parse_args()
	return args

def parse_config(config_file):
	config = configparser.ConfigParser()
	config.read(config_file)
	# TODO: Return a dictionary with all the key-values
	return config 
	
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def init_tweepy():
	# Status() is the data model for a tweet
	tweepy.models.Status.first_parse = tweepy.models.Status.parse
	tweepy.models.Status.parse = parse
	# User() is the data model for a user profil
	tweepy.models.User.first_parse = tweepy.models.User.parse
	tweepy.models.User.parse = parse

def authorise_twitter_api(config):
	auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
	auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
	return auth

def main():    
	username = parse_arguments().username
	config = parse_config('config.cfg')
	auth = authorise_twitter_api(config)	
 
	api = tweepy.API(auth)
 
	tweets = []

	tweets = api.user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True)
	last_id = tweets[-1].id

	while (True):
		more_tweets = api.user_timeline(screen_name=username, count=200, include_rts=False, exclude_replies=True, max_id=last_id-1)
		if (len(more_tweets) == 0):
			break
		else:
			last_id = more_tweets[-1].id-1
			tweets = tweets + more_tweets

	media_files = []
	for status in tweets:
		media = status.entities.get('media', []) 
		if(len(media) > 0):
			media_files.append(media[0]['media_url'])

	for media_file in media_files:
		wget.download(media_file)

if __name__=='__main__':
    main()
