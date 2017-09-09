import tweepy
import os
from tweepy import OAuthHandler
import json
import wget
import argparse
import configparser

#TODO: Limit by number of tweets?
def parse_arguments():
  parser = argparse.ArgumentParser(description='Download pictures from a Twitter feed.')
  parser.add_argument('username', type=str, help='The twitter screen name from the account we want to retrieve all the pictures')
  parser.add_argument('--num', type=int, default=100, help='Maximum number of tweets to be returned.')
  parser.add_argument('--retweets', default=False, action='store_true', help='Include retweets')
  parser.add_argument('--replies', default=False, action='store_true', help='Include replies')
  parser.add_argument('--output', default='../pictures/', type=str, help='folder where the pictures will be stored')

  args = parser.parse_args()
  return args

def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)  
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

def download_images(api, username, retweets, replies, num_tweets, output_folder):
  # Initialize downloaded and create output folder if it doesn't exist
  downloaded = 0
  if not os.path.exists(output_folder):
    os.makedirs(output_folder)

  # Iterate through tweets
  for status in tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=retweets, exclude_replies=replies, tweet_mode='extended').items():

    # If we've downloaded all the images, break the loop; no point hammering the API more
    if downloaded >= num_tweets:
      break

    # Get all entities (can be multiple per tweet)
    media = status._json.get('extended_entities', {}).get('media', [])
    
    # If the tweet had media
    if media:
      # Iterate through all pictures in the tweet and download them
      for image in media:
        wget.download(image['media_url'], out=output_folder)

      # Increment our media tweet counter
      downloaded += 1

def main():    
  arguments = parse_arguments() 
  username = arguments.username
  retweets = arguments.retweets
  replies = arguments.replies
  num_tweets = arguments.num
  output_folder = arguments.output

  config = parse_config('../config.cfg')
  auth = authorise_twitter_api(config)   
  api = tweepy.API(auth, wait_on_rate_limit=True)

  download_images(api, username, retweets, replies, num_tweets, output_folder)

if __name__=='__main__':
    main()
