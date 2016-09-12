#!/usr/bin/env python
#
# Extract the contents of the download_file_types.pb file, part of the Chrome
# extension which updates this list in Chrome.

import argparse
import os
import download_file_types.download_file_types_pb2 as pb2


extensions = []


def process_platform_settings(extension, ping, settings):
    platform = "any"
    if settings.platform == pb2.DownloadFileType.PLATFORM_ANDROID:
        platform = "android"
    elif settings.platform == pb2.DownloadFileType.PLATFORM_CHROME_OS:
        platform = "chromeos"
    elif settings.platform == pb2.DownloadFileType.PLATFORM_LINUX:
        platform = "linux"
    elif settings.platform == pb2.DownloadFileType.PLATFORM_MAC:
        platform = "mac"
    elif settings.platform == pb2.DownloadFileType.PLATFORM_WINDOWS:
        platform = "windows"

    danger_level = "not"
    if settings.danger_level == pb2.DownloadFileType.ALLOW_ON_USER_GESTURE:
        danger_level = "gesture"
    elif settings.danger_level == pb2.DownloadFileType.DANGEROUS:
        danger_level = "YES"

    print "[%s] %s (danger=%s, ping=%s)" % (platform, extension, danger_level, ping)


def process_file_type(file_type):
    extension = file_type.extension
    if len(file_type.platform_settings) != 1:
        print "WARNING: %s (%d != 1 platform settings)"\
            % (extension, len(file_type.platform_settings))

    ping = "sampled"
    if file_type.ping_setting == pb2.DownloadFileType.NO_PING:
        ping = "no"
    elif file_type.ping_setting == pb2.DownloadFileType.FULL_PING:
        ping = "FULL"
        # Chrome only submits FULL_PING extensions to the server
        extensions.append(extension)

    if file_type.is_archive:
        extension += "[a]"

    for platform_setting in file_type.platform_settings:
        process_platform_settings(extension, ping, platform_setting)


def process_config(protobuffile, verbose, quiet):
    with open(protobuffile, 'rb') as fh:
        binary_string = fh.read()
        if not quiet:
            print "Parsing a %s-byte file" % len(binary_string)
        config = pb2.DownloadFileTypeConfig()
        config.ParseFromString(binary_string)

        default_file_type = config.default_file_type
        print "\nDefaults:\n--------------------\n%s--------------------\n"\
            % default_file_type

        for file_type in config.file_types:
            process_file_type(file_type)


def dump_extensions():
    print ""
    extensions.sort()
    for extension in extensions:
        print "StringEndsWith(fileName, NS_LITERAL_STRING(\".%s\")) ||"\
            % extension


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
        print "Error: '%s' not found" % args.protobuffile
        return False

    if args.quiet and args.verbose:
        print "I can either be quiet or verbose, not both!"
        return False

    process_config(args.protobuffile, args.verbose, args.quiet)
    # dump_extensions()

    return True

if main():
    exit(0)
else:
    exit(1)
