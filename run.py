#!/usr/bin/python3
import tweepy
import os
from tweepy import OAuthHandler
import json
import wget
import argparse
import configparser
from datetime import timezone


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download pictures from Twitter.')
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--config', type=str, default='./config.cfg', help='Path to the configuration file')
    group.add_argument('--username', type=str,
                       help='The twitter screen name from the account we want to retrieve all the pictures')
    group.add_argument('--hashtag', type=str, help='The twitter tag we want to retrieve all the pictures. ')
    parser.add_argument('--num', type=int, default=100, help='Maximum number of tweets to be returned.')
    parser.add_argument('--retweets', default=False, action='store_true', help='Include retweets')
    parser.add_argument('--replies', default=False, action='store_true', help='Include replies')
    parser.add_argument('--output', default=None, type=str, help='folder where the pictures will be stored')

    args = parser.parse_args()
    return args


def parse_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def save_config(config, config_file):
    with open(config_file, 'w') as fp:
        config.write(fp)
        print('Wrote ' + config_file)
    return


def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


def init_tweepy():
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profile
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse


def get_access(auth):
    # This is called if there is no access token yet in the config.cfg file.
    # This routine asks the user retrieve one from twitter.
    # Access token & secret are returned in auth.access_token{_secret}.
    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')
        sys.exit(1)

    print('Please get a PIN verifier from ' + redirect_url)
    verifier = input('Verifier: ')
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
        sys.exit(1)


def authorise_twitter_api(config_path):
    config = parse_config(config_path)
    auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])

    if 'access_token' not in config['DEFAULT']:
        # Ask the user for an access token from Twitter
        get_access(auth)
        config['DEFAULT']['access_token'] = auth.access_token
        config['DEFAULT']['access_secret'] = auth.access_token_secret
        save_config(config, config_path)

    # Tell tweepy to use the user's access token.
    auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])

    return auth


# It returns [] if the tweet doesn't have any media
def tweet_media_urls(tweet_status):
    # At least one image
    if 'media' in tweet_status.entities:
        # Grabbing all pictures
        media = tweet_status.extended_entities['media']

        return get_media_jpg_or_gif(media)
    else:
        return {}

def get_media_jpg_or_gif(media):

    a=[ { 'filename': f"{item['id_str']}.jpg", 
          'url': f"{item['media_url']}?format=jpg&name=large" }
        for item in media if item['type'] == 'photo' ]

    b=[ { 'filename': f"{item['id_str']}.mp4", 
          'url': f"{item['video_info']['variants'][0]['url']}" }
        for item in media
        if item['type'] == 'video' or item['type'] == 'animated_gif' ]

    for item in media:
        if item['type'] == 'photo': continue
        if item['type'] == 'animated_gif': continue
        if item['type'] == 'video': continue
        from pprint import pprint as pp
        pp("Unhandled media type")
        pp(item["type"])
#            import code
#            code.interact(local=dict(globals(), **locals()))

    return a+b

def create_folder(output_folder):
    "Create a folder if it doesn't exist. Return modification time of .timestamp if it does."
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        timestamp = 0
    else:
        try:
            timestamp = os.stat(os.path.join(output_folder, '.timestamp')).st_mtime
        except:
            timestamp = 0
    return timestamp

def download_images(status, num_tweets, output_folder):
    timestamp = create_folder(output_folder)
    ts_file = os.path.join(output_folder, '.timestamp')
    downloaded = 0

    for tweet_status in status:

        # XXX The tweet time is ahead by one hour. What the heck!?
        # Daylight savings? If UTC, should be 7 or 8 hours offset. 
        # Tried UTC timezone but it didn't help.
#        tweet_status.created_at = \
#            tweet_status.created_at.astimezone(timezone.utc)

#        from pprint import pprint as pp
#        pp(tweet_status._json)
#        import code
#        code.interact(local=dict(globals(), **locals()))
        
        if downloaded >= num_tweets:
            print('Stopping after downloading ' + str(num_tweets) + ' tweets.' )
            break


        # Metadata for creating the filename, image comment, timestamp
        created = tweet_status.created_at.strftime('%y-%m-%d at %H.%M.%S %Z')
        tweet_id = tweet_status.id_str
        full_text = tweet_status.full_text

        # Creation time of tweet as seconds.nanoseconds since The Epoch.
        ctime = tweet_status.created_at.strftime('%s') 
        ctime = float(ctime)
        print(ctime)

        if ctime < timestamp:
            # XXX Probably ought to use the Twitter's "cursor" to request tweets newer than timestamp
            print('Stopping at ' + created + ' which is older than .timestamp' )
            return

        for media_info in tweet_media_urls(tweet_status):
            # Download each media URL, if the file doesn't exist already.
            file_name = media_info['filename']
            media_url = media_info['url']

            output_file = os.path.join(output_folder, file_name)
            if os.path.exists(output_file):
                print(f"Skipping existing file: {file_name}")
            else:
                print(media_url)
                print(full_text)
                print(output_file)

                # TODO: Figure out how to include ':orig' at the end
                # in a way that works with wget to get the full size
                # resolution
                wget.download(media_url, out=output_file)
                downloaded += 1

                # Set modification time to the tweet creation time.
                os.utime(output_file, (ctime, ctime))

                # TODO: Embed comment (full_text)

                # Touch the .timestamp file 
                os.close(os.open(ts_file, os.O_CREAT))
                

                # XXX Eventually, we'll get tweets in forward order
                # using a cursor, in which case we'll use something
                # more like this:
               # if not os.path.exists(ts_file):
               #     os.close(os.open(ts_file, os.O_CREAT))
               # os.utime(ts_file, (ctime, ctime)) 
    print("End of tweet statuses")

def download_images_by_user(api, username, retweets, replies, num_tweets, output_folder):
    status = tweepy.Cursor(api.user_timeline, screen_name=username, include_rts=retweets, exclude_replies=replies,
                           tweet_mode='extended').items()
    download_images(status, num_tweets, output_folder)


def download_images_by_tag(api, tag, retweets, replies, num_tweets, output_folder):
    status = tweepy.Cursor(api.search, '#' + tag, include_rts=retweets, exclude_replies=replies,
                           tweet_mode='extended').items()
    download_images(status, num_tweets, output_folder)


def main():
    arguments = parse_arguments()
    username = arguments.username
    hashtag = arguments.hashtag
    retweets = arguments.retweets
    replies = arguments.replies
    num_tweets = arguments.num
    config_path = arguments.config

    for f in (arguments.output, arguments.username, arguments.hashtag):
        if f:
            output_folder = f
            break
    if not output_folder:
        output_folder='pictures/'

    auth = authorise_twitter_api(config_path)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    if hashtag:
        download_images_by_tag(api, hashtag, retweets, replies, num_tweets, output_folder)
    else:
        download_images_by_user(api, username, retweets, replies, num_tweets, output_folder)


if __name__ == '__main__':
    main()
