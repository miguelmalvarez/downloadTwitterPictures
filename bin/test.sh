python ../run.py --username NatGeoPhotos --num 10 --config ../config.cfg
mv pictures pictures-NatGeo
python ../run.py --hashtag Photography --num 10 --config ../config.cfg
mv pictures pictures-Photo
python ../run.py --username NASA --num 10 --replies --retweets --config ../config.cfg
mv pictures pictures-NASA
python ../run.py --username NASA --num 10 --replies --retweets --output NASA_Pictures --config ../config.cfg