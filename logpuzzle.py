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

__author__ = "Diarte Jeffcoat (see full credits in credits.txt)"

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
    domain_link = "http://" + filename.split("_")[1]

    # Get access into the file and retrieve all of
    # the URLs into a set, eliminating duplicates

    with open(filename) as f:
        url_img = set()
        img_list = re.findall(r'GET (\/.*?\.jpg)', f.read())
        for image in img_list:
            if 'puzzle' in image:
                url_img.add(domain_link + image)
        # print(sorted(url_img, key=lambda i: i[-8:]))
    return sorted(url_img, key=lambda i: i[-8:])


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    # Check to see if dest_dir exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    # if it already exists, change the current directory to the dest_dir

    # Set up an index file
    with open(os.path.join(dest_dir, "index.html"), "w") as f:
        f.write("<html><body>\n")
        # Set up a loop to go through each of the image URLs to
        # add to the index.html file
        count = 0
        for url in img_urls:
            local = f'img{count}.jpg'
            print("Retrieving " + f'{local}' + "...")
            print(url)
            urllib.request.urlretrieve(
                url, os.path.join(dest_dir, f'{local}'))
            f.write(f'<img src="{local}">')

            # img_file = open(local, 'wb')
            # img_file.write(url_grab.read())
            # tags.append('<img src="{0}">'.format(local))
            count += 1
        f.write("\n</body></html>\n")


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
