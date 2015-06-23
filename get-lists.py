#!/usr/bin/python3

import urllib.request

clientId = 'navclient-auto-ffox'
appVersion = '41.0a1'
baseUrl = 'http://safebrowsing.clients.google.com/safebrowsing/'

listUrl = baseUrl + 'list?client=%s&appver=%s&pver=2.2' % (clientId, appVersion)

f= urllib.request.urlopen(listUrl, data=b'')
print(f.read().decode('UTF-8'))
