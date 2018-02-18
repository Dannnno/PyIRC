from __future__ import unicode_literals, absolute_import, print_function

__all__ = ['map', 'zip', 'range', 'enum']

try:
	from itertools import imap as map
except ImportError:
	pass

try:
	from itertools import izip as zip
except ImportError:
	pass

try:
	range = xrange
except NameError:
	pass

try:
	import enum34 as enum
except ImportError:
	import enum