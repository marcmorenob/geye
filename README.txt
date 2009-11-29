README
Version: 0.2


LICENSE
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License version 3, as published by the Free
Software Foundation.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General  Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


ABOUT
Geye is a Gnome top panel tool with a basic interaction with Google Calendar.
Geye notifies new calendar events 'X' minutes before they happen, inserts new events
in your Google calendars, list all events for each calendar, and shows the time
for the next meeting.

Geye is based on Gdata Python client library. For more information on the 
GData Python client library, please see the project on code.google.com's hosting 
service here: 
 http://code.google.com/p/gdata-python-client/

For more information about Geye, please visit http://code.google.com/p/geye/


INTRODUCTION
So you have decided to use Geye. Excellent choice! :)
My aim with this short tutorial is to introduce you in using the
Geye application for your Gnome Desktop.



--Installing Python on Linux--


To install on Linux and other *nix style operating systems, I prefer to
download the source code and compile it. However, you may be able to use your
favorite package manager to install Python. (For example, on Ubuntu this can
be as easy as running sudo apt-get install python on the command line.) To
install from source, follow these steps:

   1. Download the source tarball from the Python download page.
      http://python.org/download/
   2. Once you've downloaded the package, unpack it using the command line.
      You can use the following

      tar zxvf Python-2.<Your version>.tgz

   3. Next, you'll need to compile and install the source code for the Python
      interpreter. In the decompressed directory, run ./configure to generate
      a makefile.
   4. Then, run make. This will create a working Python executable file in 
      the local directory. If you don't have root permission or you just want
      to use Python from your home directory, you can stop here. You'll be 
      able to run Python from this directory, so you might want to add it to
      your PATH environment variable.
   5. I prefer to have Python installed in /usr/bin/ where most Python 
      scripts look for the interpreter. If you have root access, then run 
      make install as root. This will install Python in the default location
      and it will be usable by everyone on your machine.
   6. Check to see if your install is working as expected by opening a 
      terminal and running python -V.

--Installing Dependencies--

Dependencies package:

import pygtk
import gtk
import gobject
import pynotify
from xml.etree import ElementTree
import getopt
import sys
import string
import time

Dependencies from GData Python client library (http://code.google.com/p/gdata-python-client/):

import gdata.service
import gdata.calendar
import gdata.calendar.service
import atom
import atom.service

--Running Geye application--

Download Geye.tar.gz from http://code.google.com/p/geye/
>tar xvzf geye-0.1.tar.gz.
Download gdata-2.0.5.tar.gz from http://code.google.com/p/gdata-python-client/
>tar xvzf gdata-2.0.5.tar.gz inside geye folder.
Execute command >python Geye.py





