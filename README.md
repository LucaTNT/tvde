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

## Example output
	{
	    "attenuation_DS0": 1.5,
	    "attenuation_DS1": 3.7,
	    "attenuation_DS2": 7.1,
	    "attenuation_US0": 0.3,
	    "attenuation_US1": 1.4,
	    "attenuation_US2": 2.5,
	    "attenuation_US3": 3.0,
	    "linerate_down": 108.0,
	    "linerate_up": 21.6,
	    "margin_down": 12.3,
	    "margin_up": 15.0,
	    "max_linerate_down": 119.87,
	    "max_linerate_up": 40.84,
	    "power_down": 14.5,
	    "power_up": -24.9,
	    "transfered_down": 3413.11,
	    "transfered_up": 3855.38,
	    "uptime": 80845
	}
