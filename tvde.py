#!/usr/bin/env python
# Author: @LucaTNT
# Creation date: 2018-09-12
# Version: 0.1
#
# This scripts connects to a Technicolor DGA 4132 (AGTHP) (aka Tim Hub),
# grabs the VDSL line info from the status page and outputs it as JSON.
#
# Usage: tvde.py [DEVICE_IP] [USERNAME] [PASSWORD]
#
# Adapted from https://gist.github.com/DanielO/76c6c337ff09f6011f408427df376e68

import binascii
import bs4
import json
import mechanize
import re
import sys
import mysrp as srp
import urllib

def authenticate(br, host, username, password):
    #br.set_debug_http(True)
    #br.set_debug_responses(True)
    #br.set_debug_redirects(True)
    r = br.open('http://' + host)
    bs = bs4.BeautifulSoup(r, features="html5lib")
    token = bs.head.find(lambda tag: tag.has_attr('name') and tag['name'] == 'CSRFtoken')['content']
    #print('Got CSRF token ' + token)

    usr = srp.User(username, password, hash_alg = srp.SHA256, ng_type = srp.NG_2048)
    uname, A = usr.start_authentication()

    req = mechanize.Request('http://' + host + '/authenticate', data = urllib.urlencode({'CSRFtoken' : token, 'I' : uname, 'A' : binascii.hexlify(A)}))
    r = br.open(req)
    j = json.decoder.JSONDecoder().decode(r.read())
    #print('Sent challenge, got ' + str(j))

    M = usr.process_challenge(binascii.unhexlify(j['s']), binascii.unhexlify(j['B']))
    req = mechanize.Request('http://' + host + '/authenticate', data = urllib.urlencode({'CSRFtoken' : token, 'M' : binascii.hexlify(M)}))
    r = br.open(req)
    j = json.decoder.JSONDecoder().decode(r.read()
)    #print('Got response ' + str(j))

    usr.verify_session(binascii.unhexlify(j['M']))
    if not usr.authenticated():
        #print('Failed to authenticate')
        return False

    #print('Authenticated OK')
    return True


if (len(sys.argv) != 4):
    print '{"error": "Not enough arguements (' + str(len(sys.argv) - 1) + ' supplied, 3 needed).", "usage": "' + sys.argv[0] + ' [DEVICE_IP] [USERNAME] [PASSWORD]"}'
else:
    host = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    br = mechanize.Browser()
    br.set_handle_robots(False)
    status = authenticate(br, host, username, password)
    if status:
        r = br.open('http://' + host + '/modals/broadband-modal.lp?auto_update=true')
        bs = bs4.BeautifulSoup(r, features="html5lib")

       	# Handy regular expression to match numbers
        pattern = re.compile('(-?[0-9]+\.?[0-9]+)')

        uptime_html  = repr(bs.body.find(id='dsl_uptime'))
        uptime = pattern.findall(uptime_html)

        max_linerate_html = repr(bs.body.find(id='dsl_max_linerate'))
        max_linerate = pattern.findall(max_linerate_html)

        linerate_html = repr(bs.body.find(id='dsl_linerate'))
        linerate = pattern.findall(linerate_html)

        power_html = repr(bs.body.find(id='dsl_power'))
        power = pattern.findall(power_html)

        attenuation_html = repr(bs.body.find(id='dsl_attenuation'))
        attenuation = pattern.findall(attenuation_html)

        margin_html = repr(bs.body.find(id='dsl_margin'))
        margin = pattern.findall(margin_html)

        transfered_html = repr(bs.body.find(id='dsl_transfered'))
        transfered = pattern.findall(transfered_html)

      	# Uptime is "fuzzy": e.g. 23 days 2 hours 43 minutes 5 seconds
      	# If < 1 day, than the first number is the number of hours,
      	# If < 1 hour, then the first number is the number of minutes,
      	# If < 1 minute, then the first (and only) number is the number of seconds
        if (len(uptime) == 4):
            uptime_value = int(uptime[3]) + int(uptime[2])*60 + int(uptime[1])*60*60 + int(uptime[0])*60*60*24
        if (len(uptime) == 3):
            uptime_value = int(uptime[2]) + int(uptime[1])*60 + int(uptime[0])*60*60
        if (len(uptime) == 2):
            uptime_value = int(uptime[1]) + int(uptime[0])*60
        if (len(uptime) == 1):
            uptime_value = int(uptime)

        dsl_data = {
            'uptime': uptime_value,
            'max_linerate_up' : float(max_linerate[0]),
            'max_linerate_down' : float(max_linerate[1]),
            'linerate_up' : float(linerate[0]),
            'linerate_down' : float(linerate[1]),
            'power_up' : float(power[0]),
            'power_down' : float(power[1]),
            'margin_up' : float(margin[0]),
            'margin_down' : float(margin[1]),
            'transfered_up' : float(transfered[0]),
            'transfered_down' : float(transfered[1]),
            'attenuation_US0' : float(attenuation[0]),
            'attenuation_US1' : float(attenuation[1]),
            'attenuation_US2' : float(attenuation[2]),
            'attenuation_US3' : float(attenuation[3]),
            'attenuation_DS0' : float(attenuation[4]),
            'attenuation_DS1' : float(attenuation[5]),
            'attenuation_DS2' : float(attenuation[6])
        }

        print json.dumps(dsl_data)
    else:
        print '{"error": "Authentication failed"}'
