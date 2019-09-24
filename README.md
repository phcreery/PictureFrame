# PictureFrame
Raspberry Pi + 3.2" GPIO LCD + Instagram/Collection

[Waveshare Touchscreen LCD](https://www.waveshare.com/3.2inch-rpi-lcd-b.htm)

## About

Raspberry Pi based instagram image scraper and slideshow picture frame.

2 Files:
 - **scraper.py** scraps Instagram for pictures based on Username or Hashtag & displays them
 - **frame.py** displays imaged that are locally stored
 
 ## Prerequisites
 
  - Python 2.7
  - pygame
  - [instagram-scraper](https://github.com/rarcega/instagram-scraper) to download the images
  - [Instagram-API-python](https://github.com/LevPasha/Instagram-API-python) to get follower count
  
  ## Running
  
Local image directory is stored in variable:
`dir="/home/pi/python/instapy/myscraper/"`
  
  `python scraper.py` 
  or 
  `python frame.py`
  
