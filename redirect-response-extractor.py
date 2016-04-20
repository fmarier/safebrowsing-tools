#!/usr/bin/env python3
#
# Extract the contents of a Safe Browsing redirect response
# and throw an exception in case of errors.

import argparse
import os
import struct
import sys

MAX_CHUNK_SIZE = 1024 * 1024  # from toolkit/components/url-classifier/ProtocolParser.cpp


def safe_read(fh, length):
    s = fh.read(length)
    if not s:
        raise ValueError("Trying to read past EOF")
    fh.seek(fh.tell() - length)
    return fh.read(length)


# stolen from sbdbdump/dump.py
def print_prefix(prefix):
    bytebuffer = struct.Struct("=" + str(len(prefix)) + "B")
    data = bytebuffer.unpack_from(prefix, 0)
    for byte in data:
        print("%02x" % byte, end="")
    print()

# ADD-DATA = (HOSTKEY COUNT [PREFIX]*)+
# HOSTKEY  = <4 unsigned bytes>  # 32-bit hash prefix
# COUNT    = <1 unsigned byte>
# PREFIX   = <HASHLEN unsigned bytes>
def process_addData(fh, chunkLen, hashLen, verbose, quiet):
    if hashLen != 32:
        raise NotImplementedError("Only digest256 chunks are supported at the moment")

    if chunkLen % hashLen != 0:
        raise ValueError("Size of digest256 chunks must be divisible by %s" % hashLen)

    i = 0
    prefixCount = 0
    while i < chunkLen:
        # For shavar chunks
        #hostKey = struct.unpack('!i', safe_read(fh, 4))[0]
        #count = struct.unpack('B', safe_read(fh, 1))[0]
        #i += 5
        #print("hostkey has %s prefixes" % count)

        # For digest256 chunks
        count = chunkLen / hashLen

        j = 0
        while (j < count):
            prefix = safe_read(fh, hashLen)
            if verbose:
                print_prefix(prefix)
            i += hashLen
            j += 1
            prefixCount += 1

    if not quiet:
        print("Found %s prefixes in %s bytes" % (prefixCount, i))

# SUB-DATA    = (HOSTKEY COUNT (ADDCHUNKNUM | (ADDCHUNKNUM PREFIX)+))+
# HOSTKEY     = <4 unsigned bytes>  # 32-bit hash prefix
# COUNT       = <1 unsigned byte>
# ADDCHUNKNUM = <4 byte unsigned integer in network byte order>
# PREFIX      = <HASHLEN unsigned bytes>
def process_subData(fh, chunkLen, hashLen, verbose, quiet):
    if not quiet:
        print("Processing %s-byte sub chunk..." % chunkLen)

    raise NotImplementedError("Sub chunks are not implemented yet!")


# BODY      = (ADD-HEAD | SUB-HEAD)+
# ADD-HEAD  = "a:" CHUNKNUM ":" HASHLEN ":" CHUNKLEN LF CHUNKDATA
# SUB-HEAD  = "s:" CHUNKNUM ":" HASHLEN ":" CHUNKLEN LF CHUNKDATA
# CHUNKNUM  = DIGIT+  # Sequence number of the chunk
# HASHLEN   = DIGIT+  # Decimal length of each hash prefix in bytes
# CHUNKLEN  = DIGIT+  # Size of the chunk data in bytes >= 0
# CHUNKDATA = <CHUNKLEN number of unsigned bytes>
def process_control(fh, line, verbose, quiet):
    if not quiet:
        print("Processing control line...")

    (chunkType, chunkNum, hashLen, chunkLen) = line.split(':')
    s = "chunk %s contains %s bytes of %s-byte hashes" % (chunkNum, chunkLen, hashLen)

    if int(chunkLen) > MAX_CHUNK_SIZE:
        raise ValueError("Chunk %s is too big (%s bytes)" % (chunkNum, chunkLen))

    if 'a' == chunkType:
        if not quiet:
            print("Add %s" % s)
        process_addData(fh, int(chunkLen), int(hashLen), verbose, quiet)
    elif 's' == chunkType:
        if not quiet:
            print("Sub %s" % s)
        process_subData(fh, int(chunkLen), int(hashLen), verbose, quiet)
    else:
        raise ValueError("Invalid line: %s" % line)


def process_response(responsefile, verbose, quiet):
    with open(responsefile, 'rb') as fh:
        if not quiet:
            size = len(fh.read())
            print("Parsing a %s-byte response file" % size)
            fh.seek(0)

        for line in fh:
            if 10 == line[-1]:
                line = line[:-1]

            line = line.decode('ascii')
            process_control(fh, line, verbose, quiet)


def main():
    parser = argparse.ArgumentParser(
        description='Extractor for Safe Browsing redirect responses')
    parser.add_argument('responsefile', type=str,
                        help='the binary redirect response to extract')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help='display the contents of the response')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true',
                        help='suppress all non-error output')
    args = parser.parse_args()

    if not os.path.isfile(args.responsefile):
        print("Error: '%s' not found" % args.responsefile, file=sys.stderr)
        return False

    if args.quiet and args.verbose:
        print("I can either be quiet or verbose, not both!")
        return False

    process_response(args.responsefile, args.verbose, args.quiet)

    return True

if main():
    exit(0)
else:
    exit(1)
