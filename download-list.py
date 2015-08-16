#!/usr/bin/python3

import urllib.request

clientId = 'navclient-auto-ffox'
appVersion = '42.0a1'
baseUrl = 'https://tracking.services.mozilla.com/'
#baseUrl = 'https://safebrowsing.clients.google.com/safebrowsing/'
list = b'mozpub-track-digest256'

listUrl = baseUrl + 'downloads?client=%s&appver=%s&pver=2.2' % (clientId, appVersion)
data = list + b';'

f= urllib.request.urlopen(listUrl, data=data)
print(f.read().decode('ISO8859-1'))
