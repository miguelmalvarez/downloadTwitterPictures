# downloadTwitterPictures

Code to download all the pictures from a given twitter account. It allows to filter retweets and replies if needed. Usage:

positional arguments:
  username         The twitter screen name from the account we want to
                   retrieve all the pictures

optional arguments:
  -h, --help       show this help message and exit
  --num NUM        Maximum number of tweets to be returned.
  --retweets       Include retweets
  --replies        Include replies
  --output OUTPUT  folder where the pictures will be stored
