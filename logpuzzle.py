#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__: "Diarte Jeffcoat w/help from Stack Overflow('https://stackoverflow.com/questions/33530725/alphabetically-sorting-urls-to-download-image') and ('https://stackoverflow.com/questions/15035123/what-command-to-use-instead-of-urllib-request-urlretrieve')"

import os
import re
import sys
import urllib.request
import argparse

def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename) as f:
        s = {i.rstrip() for i in f if 'puzzle' in i}
    return sorted(s, key=lambda url: url[-8:-4])


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    
    index = file(os.path.join(dest_dir, 'index.html'))
    index.write('<html><body>\n')

    i = 0
    for url in img_urls:
        local = 'img' + str(i) + '.jpg'
        print("Retrieving...", local)
        print(local)
        print(dest_dir)
        print(url)
        
        response = requests.get(url)
        if response.status_code == 200:
            f = open(os.path.join(dest_dir, local + '.jpg'), 'wb')
            f.write(response.content)
            f.close()
        index.write('<img src="%s">' % (local + ".jpg"))
        i += 1
    index.write("\n</body></html>\n")
    index.close()

def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
