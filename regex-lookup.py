#!/usr/bin/python3
#
# https://developers.google.com/safe-browsing/developers_guide_v2#RegexLookup

import hashlib
from urllib.parse import urlparse

def print_hash(url):
    hashdigest = hashlib.sha256(url.encode('utf8')).hexdigest()
    print("%s: %s" % (hashdigest.upper(), url))

def print_hashes(url):
    urlparts = urlparse(url)
    hostname = urlparts.netloc
    dot = hostname.find('.')
    while dot != -1:
        # Check the full URL
        if urlparts.query:
            # Check with the fragment (not part of the spec)
            if urlparts.fragment:
                s = hostname + urlparts.path + '?' + urlparts.query + '#' + urlparts.fragment
                print_hash(s)

            s = hostname + urlparts.path + '?' + urlparts.query
            print_hash(s)

        # Check with the fragment (not part of the spec)
        if urlparts.fragment:
            s = hostname + urlparts.path + '#' + urlparts.fragment
            print_hash(s)

        # Check without the query string
        s = hostname + urlparts.path
        print_hash(s)

        # Check all 4 possible paths
        i = 0
        path = ''
        remaining = urlparts.path
        nextslash = remaining.find('/')
        while nextslash != -1 and i < 4:
            path += remaining[0:nextslash+1]
            remaining = remaining[nextslash+1:]
            s = hostname + path
            print_hash(s)

            nextslash = remaining.find('/')
            i += 1

        hostname = hostname[dot+1:]
        dot = hostname.find('.')

print_hashes('https://extremetracking.com/ve_gate/EXs.css')
