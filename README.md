# downloadTwitterPictures

## Fork from miguelmalvarez

This is a (hopefully temporary) fork of miguelmalvarez's
downloadTwitterPictures which has some bug fixes and improvements. For
example, it downloads animations as mp4 instead of jpeg and it prompts
the user to retrieve the authorization if there is no existing
config.cfg file.

____

_Library to download the pictures from a given Twitter account or a given hashtag._

Note: In order to use this code, you have to [register your own 'app' in Twitter](http://apps.twitter.com/)  so that you can have your own credentials (consumer key and secret). 
Once this is done, you should add these details in a 'config.cfg' file (with the same structure as 'sample-config.cfg').  

## Basic usage

You can download the pictures for a given user as follows:

```bash
# Download 10 images from the National Geographic Twitter Account
./run.py --username NatGeoPhotos --num 10

# Download 10 images with the hashtag Photography
./run.py --hashtag Photography --num 10
```

The library also allows to --retweets and --replies to include retweets or replies, and --output to specify a different directory to save the pictures in. By default, a directory will be created with the same --username or --hashtag as was specified on the command line. Failing that, the default output directory is "pictures/".

```bash
./run.py --username NASA --num 10 --replies --retweets
./run.py --username NASA --num 10 --replies --retweets --output ../NASA_Pictures
./run.py --username NASA --num 10 --replies --retweets --config config.cfg --output ../NASA_Pictures
```

The library will only download pictures that are not in the output folder already to avoid duplications. It will also try to download the pictures in their largest possible size.

Usually one is interested in only new pictures that have been posted since the last time an account was checked. However, if the previous pictures were deleted or renamed, they would be redownloaded. To prevent that from happening, a file in the output directory called ".timestamp" is created which is used to mark the last time images were downloaded. If for some reason you want to search further back in time, you may simply delete the .timestamp file. 
