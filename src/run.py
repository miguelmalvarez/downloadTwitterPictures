import tweepy
from tweepy import OAuthHandler
import json
import wget
import argparse
import configparser

#TODO: Limit by number of tweets?
def parse_arguments():
	parser = argparse.ArgumentParser(description='Download pictures from a Twitter feed.')
	parser.add_argument('username', type=str, help='The twitter screen name from the account we want to retrieve all the pictures')

	parser.add_argument('--num', type=int, help='Maximum number of tweets to be returned.')
	parser.set_defaults(num=100)

	parser.set_defaults(retweets=False)
	parser.add_argument('--retweets', action='store_true', help='Include retweets')
	
	parser.set_defaults(replies=False)	
	parser.add_argument('--replies', action='store_true', help='Include replies')
	
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

def download_images(api, username, retweets, replies, num_tweets):
 	# Better efficiency, save every tweet as they come instead of reading them all?
	tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies)
	last_id = tweets[-1].id

	# TODO: Make more efficient 
	downloaded = 0
	while (True):		
		if (len(tweets) == 0):
			break
		else:
			last_id = tweets[-1].id-1
		
		for status in tweets:
			media = status.entities.get('media', []) 
			if(len(media) > 0 and downloaded < num_tweets):
				wget.download(media[0]['media_url'])
				downloaded += 1				

		tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies, max_id=last_id-1)

def main():    
	#TODO: Restructure in a dictionary?
	arguments = parse_arguments() 
	username = arguments.username
	retweets = arguments.retweets
	replies = arguments.replies
	num_tweets = arguments.num

	config = parse_config('config.cfg')
	auth = authorise_twitter_api(config)	 
	api = tweepy.API(auth)

	download_images(api, username, retweets, replies, num_tweets)

if __name__=='__main__':
    main()
