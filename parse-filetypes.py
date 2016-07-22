#!/usr/bin/env python
#
# Extract the contents of the download_file_types.pb file, part of the Chrome
# extension which updates this list in Chrome.

import argparse
import os
import struct
import sys
import download_file_types.download_file_types_pb2 as pb2


def process_file_type(file_type):
    print file_type.extension


def process_config(protobuffile, verbose, quiet):
    with open(protobuffile, 'rb') as fh:
        binary_string = fh.read()
        if not quiet:
            print "Parsing a %s-byte file" % len(binary_string)
        config = pb2.DownloadFileTypeConfig()
        config.ParseFromString(binary_string)
        for file_type in config.file_types:
            process_file_type(file_type)


def main():
    parser = argparse.ArgumentParser(
        description='Extractor for download_file_types.pb')
    parser.add_argument('protobuffile', type=str,
                        help='the binary file to extract')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='display the contents of the response')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help='suppress all non-error output')
    args = parser.parse_args()

    if not os.path.isfile(args.protobuffile):
        print "Error: '%s' not found" % args.protobuffile # TODO: file=sys.stderr
        return False

    if args.quiet and args.verbose:
        print "I can either be quiet or verbose, not both!"
        return False

    process_config(args.protobuffile, args.verbose, args.quiet)

    return True

if main():
    exit(0)
else:
    exit(1)
