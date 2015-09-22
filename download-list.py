#!/usr/bin/python3

import urllib.request

clientId = 'navclient-auto-ffox'
appVersion = '42.0a1'

baseUrl = 'https://shavar.services.mozilla.com/'
#baseUrl = 'https://shavar.stage.mozaws.net/'
list = b'mozstd-track-digest256'

#baseUrl = 'https://safebrowsing.clients.google.com/safebrowsing/'
#list = b'googpub-phish-shavar'

listUrl = baseUrl + 'downloads?client=%s&appver=%s&pver=2.2' % (clientId, appVersion)
data = list + b';'
headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"
}

request = urllib.request.Request(listUrl, data=data, headers=headers)
f = urllib.request.urlopen(request)
print(f.read().decode('ISO8859-1'))
