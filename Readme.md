#eMusic_dl.py - simple command-line eMusic downloader#

It is not possible on Linux to install the eMusic Download Manager software.  
To download albums one can use this simple script instead.

Requirements

* Python 2.7
* [PycURL](https://pypi.python.org/pypi/pycurl) python module

Usage instructions:
 
* Sign in to eMusic
* Visit the URL http://www.emusic.com/dlm/install/ - this tricks eMusic into thinking that the currently-signed-in user has installed Download Manager
* Click 'download' on an eMusic album page and download and save to disk the `0.emx` file when prompted.
* Run the script using `python eMusic_dl.py path/to/saved/0.emx /path/to/music/library`

The script will then:

* Create the directory `/path/to/music/library/<artist>/<album>` if it does not already exist
* Copy the `.emx` file to that directory (and rename it to `<artist>-<album>.emx`)
* Download standard and large album art files to that directory
* Download all tracks to that directory
