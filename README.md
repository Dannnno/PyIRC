[![Docs built](https://readthedocs.org/projects/PyIRC/badge/?version=latest)](http://pyirc.readthedocs.org/en/latest/)
[![Build passed](https://travis-ci.org/Dannnno/PyIRC.svg?branch=master)](https://travis-ci.org/Dannnno/PyIRC)
##PyIRC

Implementation of an IRC client in python.  Will be implemented in various different ways (sockets w/ select, sockets w/ asyncore, Twisted, etc)

#### Implementation using sockets and select
Can be found in IRC_sockselect.py

This is the lowest level my program is likely to go.  It uses the stdlib implementation of sockets and select to implement an IRC client.

#### Implementation using asyncore
Can be found in IRC_sockasyncore.py

This is the mid level implementation I'm working on.  Asyncore and asynchat are modules in the stdlib that operate at a higher level than select but offer similar functionality

#### Implementation using asynchat
This might just get folded into IRC_sockasyncore.py

#### Implementation using Twisted
Not yet started, will likely be found in IRC_Twisted.py

Twisted is a high level event-driven framework for handling asynchronous server-client communications.  It will (theoretically) be the highest level I use, and (hopefully) the simplest

#### GUI
Not yet started

The GUI will likely be implemented using Kivy.  I expect it will look like your pretty standard IRC client, and functionality between implementations should be identical

### Testing

All tests can be run from the command line using nose

    \path\PyIRC\> nosetests