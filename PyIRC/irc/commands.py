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
    .. _RFC1459: https://tools.ietf.org/html/rfc1459
    """

    # Channel commands
    LIST = 1
    MODE = 2
    JOIN = 3
    NAMES = 4
    WHO = 5
    WHOIS = 6

    # Operator commands
    SQUIT = 7
    CONNECT = 8
    KILL = 9
    KICK = 10
    MODE = 11
    INVITE = 12
    TOPIC = 13

    PASS = 14
    USER = 15
    NICK = 16

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
