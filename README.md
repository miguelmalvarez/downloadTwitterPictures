# downloadTwitterPictures

_Library to download the pictures from a given twitter account or a given hashtag._


You can download the pictures for a given user as follows:

```bash
# Download 10 images from user USER_NAME
python run.py --username USER_NAME --num 10

# Download 10 images with the hashtag TAG
python run.py --hashtag TAG --num 10
```

The library also allows to include retweets or replies

```bash
python run.py --username USER_NAME --num 10 --replies --retweets
```
