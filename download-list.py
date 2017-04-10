#!/usr/bin/env python3

import urllib.request

clientId = 'navclient-auto-ffox'
appVersion = '45.0.1'
key = ''

baseUrl = 'https://shavar.services.mozilla.com/'
#baseUrl = 'https://shavar.stage.mozaws.net/'
lists = 'base-track-digest256'
lists = 'base-track-digest256,mozstd-trackwhite-digest256,mozplugin-block-digest256,allow-flashallow-digest256,except-flashallow-digest256,block-flash-digest256,except-flash-digest256,block-flashsubdoc-digest256,except-flashsubdoc-digest256'

#baseUrl = 'https://safebrowsing.google.com/safebrowsing/'
#lists = 'googpub-phish-shavar'

data = b''
for list in lists.split(','):
    data += list.encode('ascii') + b';\n'

headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
}

listUrl = baseUrl + 'downloads?client=%s&appver=%s&pver=2.2&key=%s' % (clientId, appVersion, key)

request = urllib.request.Request(listUrl, data=data, headers=headers)
f = urllib.request.urlopen(request)
print(f.read().decode('ISO8859-1'))
