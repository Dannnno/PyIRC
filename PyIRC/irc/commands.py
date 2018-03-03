# Force Python 3 behaviors
from __future__ import print_function, unicode_literals, absolute_import

from .executable_command import ExecutableCommandMixin, CountType
from .constants import IrcErrors, IrcCommandResponse, IrcReservedCodes

try:
    import enum34 as enum
except ImportError:
    import enum

@enum.unique
class IrcCommand(ExecutableCommandMixin, enum.Enum):
    """
    Commands supported by the IRC protocol as per RFC1459_.

    Attributes
    ----------
    PASS
        Used to set a connection password. Can and must be sent
        before any attempt to register the connection.

        Parameters
        ----------
        password: string
            The actual password to use.
    NICK
    	Used to give a user a nickname, or change the previous one.
    	Parameters
    	----------
    	nickname: string
    		The nickname to use
    	hopcount: int, optional
    		How far away a nick is from its home server. Only used by
    		servers

    .. _RFC1459: https://tools.ietf.org/html/rfc1459
    """

    PASS = 1
    NICK = 2

    LIST = -1

@IrcCommand.PASS.register_parameter("password", 0)
def validate_password(password):
    """
    Validate that the given password meets IRC specifications.

    Parameters
    ----------
    password: string
        The password to validate

    Returns
    -------
    string|None
        None if it passes validation, otherwise an error message.
    """

    return None

@IrcCommand.PASS.register_error_handler(IrcErrors.ERR_NEEDMOREPARAMS)
def handle_missing_password(command, error):
	"""Handle a missing password from a PASS command.

	Raises
	------
	ValueError
	"""

	raise ValueError("Didn't send a password with a PASS command.")

@IrcCommand.PASS.register_error_handler(IrcErrors.ERR_ALREADYREGISTERED)
def handle_already_registered(command, error):
	"""Handle sending a password when already registered."""

	return None

@IrcCommand.PASS.register_execution
def build_password_message(password):
	"""Build the PASS message to send."""

	return "PASS {password}".format(**locals())

@IrcCommand.NICK.register_parameter("nickname", 0)
def validate_nickname(nickname):

	return None

@IrcCommand.NICK.register_parameter("hopcount", 1, optional=True)
def validate_hopcount(hopcount):
	"""Validate that the hopcount is an integer."""

	try:
		count = int(hopcount)
	except TypeError:
		return "Hopcount can't be converted to an integer"

	# Anything convertable to int should convert to float
	floating_count = float(hopcount)

	if count != floating_count:
		return "Hopcount must be an integer, not floating point"

	return None

@IrcCommand.NICK.register_error_handler(IrcErrors.ERR_NONICKNAMEGIVEN)
def handle_missing_nickname(command, error):

	raise ValueError("NICK command missing a nickname")

@IrcCommand.NICK.register_error_handler(IrcErrors.ERR_NICKNAMEINUSE)
def handle_duplicate_nickname(command, error):

	raise ValueError("Nickname given is a duplicate; current and previous nickname dropped.")

@IrcCommand.NICK.register_error_handler(IrcErrors.ERR_NICKCOLLISION)
def handle_local_duplicate_nickname(command, error):

	raise ValueError("Nickname given is a duplicate; no KILL generated")

@IrcCommand.NICK.register_error_handler(IrcErrors.ERR_ERRONEUSNICKNAME)
def handle_erroneous_nickname(command, error):

	raise ValueError("Nickname is in an invalid format")

@IrcCommand.NICK.register_execution
def build_nick_command(nickname, hopcount=0):

	return "NICK {nickname} {hopcount}".format(**locals())

@IrcCommand.LIST.register_parameter(
    "channels", 0, optional=True, count=1, count_type=CountType.MIN)
def validate_channel_name(name):
    """Validate that a given name is a valid channel name.

    Uses RFC1459_ validation for the channel name.

    Parameters
    ----------
    name: string
        Name of the channel.

    Returns
    -------
    err: string | None
        Returns an error string describing what is wrong, otherwise
        returns None if it is okay.

    .. _RFC1459: https://tools.ietf.org/html/rfc1459#section-1.3
    """

    if not (name.startswith('&') or name.startswith('#')):
        return "Channel name must start with a '&' or '#' character."

    if len(name) > 200:
        return "Channel name cannot exceed 200 characters."

    ctl_g = chr(0x07) # ^G
    bad_chars = (' ', ',', ctl_g)
    for bad_char in bad_chars:
        if bad_char in name:
            return "Channel name cannot contain {}.".format(bad_char)

    return None

@IrcCommand.LIST.register_parameter("server", 1, optional=True)
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
