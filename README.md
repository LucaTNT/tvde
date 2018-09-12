# Technicolor VDSL Data Extractor - TVDE.py
This scripts scrapes the web interface of (some) Technicolor VDSL routers in order to grab the line data and output it in a convenient JSON format

So far it has only been tested on a Technicolor DGA 4132 (AGTHP) (aka Tim Hub).

It is based on [this incredibly useful Gist](https://gist.github.com/DanielO/76c6c337ff09f6011f408427df376e68) by DanielO, I stole most of the code from it.

## Usage
    tvde.py [DEVICE_IP] [USERNAME] [PASSWORD]

## Dependencies
* [mechanize](https://pypi.org/project/mechanize/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

You can install them both from pip (`pip install mechanize beautifulsoup4`)