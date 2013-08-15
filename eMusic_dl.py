#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as etree
import os, errno
import sys
import pycurl
import shutil

def mkdir_p(path):
    """Make all directories in a path if they don't already exist."""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def clean_name(d):
    """Remove funny characters from strings that want to use as file or dir names."""
    d = d.replace(' ', '_')
    for c in ',:;@#~<>"':
        d = d.replace(c, '')
    d = d.replace("'", '')
    return d

def download(url, path, fname=None):
    """Download a URL to a path to a file with the same name as the URL or a specified filename."""
    if not fname:
        fname = url.rsplit('/', 1)[1]
    with open(os.path.join(path, fname), 'wb') as f:
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.WRITEDATA, f)
        curl.perform()
        curl.close()

def eMusic_dl(emx_fname, target_path):
    """Download album specified in an eMusic EMX file to artist+album-specific dirs under target_path."""

    # check target_path is writable
    if not os.path.isdir(target_path + '/'):
        raise Exception('Cannot download to {} as not a valid directory'.format(target_path))
        sys.exit(-1)

    # Try to read EMX file to get root of the XML document
    root = None
    try:
        root = etree.parse(emx_fname).getroot()
    except IOError:
       print 'Could not open eMusic EMX file "{}"'.format(emx_fname)

    download_path = None
    for tracklist in root.iter('TRACKLIST'):
        for track in tracklist.iter('TRACK'):
            if not download_path:
                # Get album+artist specific info
                artist = clean_name(track.find('ARTIST').text)
                album = clean_name(track.find('ALBUM').text)
                print "Downloading '{}' by {} to {}:".format(album, artist, download_path)
                download_path = os.path.join(target_path, artist, album)
                # Create path to save music and album art into
                mkdir_p(download_path)
                
                # Copy EMX to download dir
                print " - copying EMX file to download directory"
                shutil.copy2(emx_fname, os.path.join(download_path, 
                    '{}-{}.emx'.format(artist, album)))
                    
                # Download album art
                for elem in ('ALBUMART', 'ALBUMARTLARGE'):
                    print " - getting album art"
                    download(track.find(elem).text, download_path)

            # Download tracks
            track_num = int(track.find('TRACKNUM').text)
            track_url = track.find('TRACKURL').text
            track_fname = "{:02}-{}".format(track_num, track_url.rsplit('/', 1)[1])
            print " - getting {}".format(track_fname)
            download(track_url, download_path, fname=track_fname)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: {} emx_fname target_path'.format(sys.argv[0])
        sys.exit(-1)
    eMusic_dl(emx_fname=sys.argv[1], target_path=sys.argv[2])
