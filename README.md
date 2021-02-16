# downloadTwitterPictures

_Library to download the pictures from a given twitter account or a given hashtag._

## Basic usage

You can download the pictures for a given user as follows:

```bash
# Download 10 images from the National Geographic Twitter Account
python run.py --username NatGeoPhotos --num 10

# Download 10 images with the hashtag Photography
python run.py --hashtag Photography --num 10
```

The library also allows to include retweets or replies, and to specify a different folder to save the pictures in ("pictures" is the default)

```bash
python run.py --username NASA --num 10 --replies --retweets
python run.py --username NASA --num 10 --replies --retweets --output ../NASA_Pictures
python run.py --username NASA --num 10 --replies --retweets --config config.cfg --output ../NASA_Pictures
```

The library will only download pictures that are not in the output folder already to avoid duplications. 