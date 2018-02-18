# Force Python 3 behaviors
from __future__ import print_function, unicode_literals, absolute_import

from .executable_command import ExecutableCommandMixin, CountType

try:
	import enum34 as enum
except ImportError:
	import enum

@enum.unique
class IrcCommand(ExecutableCommandMixin, enum.Enum):
	LIST = 1


@IrcCommand.LIST.register_parameter(
	"channels", 1, optional=True, count=1, count_type=CountType.MIN)
def validate_channel_name(name):
	"""Validate that a given name is a valid channel name.

	Uses RFC 1459 validation.

	Parameters
	----------
	name: string
		Name of the channel.

	Returns
	-------
	err: string | None
		Returns an error string describing what is wrong, otherwise 
		returns None if it is okay.
	"""

	## TODO: implement this
	return None

@IrcCommand.LIST.register_parameter("server", 2, optional=True)
def validate_server_name(hostname):
	"""Validate that a given name is a valid server name.

	Uses RFC 952, 1123, and 2810.

	Parameters
	----------
	hostname: string
		Name of the server.

	Returns
	-------
	err: string | None
		Returns an error string describing what is wrong, otherwise 
		returns None if it is okay.
	"""

	## TODO: implement this
	return None

@IrcCommand.LIST.register_execution
def list_channels(channels=None, server=None):

	## TODO: implement this
	return None