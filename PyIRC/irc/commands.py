# Force Python 3 behaviors
from __future__ import print_function, unicode_literals, absolute_import

from .executable_command import ExecutableCommandMixin, CountType
from .constants import (
    IrcError, IrcCommandResponse, IrcReservedCodes, MAX_NICKNAME_LENGTH,
    IrcChannelModes, IrcUserModes, IrcModeChanges)

import enum
import warnings
from textwrap import dedent


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
    USER
        Used to identify a new user.

        Parameters
        ----------
        username: string
            Username of the new user.
        hostname: string
            Name of the server the user is on. Typically ignored in
            client to server communiations, but used in server to server
            communication.
        servername: string
            Name of the server the user is connecting to. Typically
            ignored in client to server communiations, but used in
            server to server communication.
        realname: string
            Real name of the user. **Must** be the last parameter, and
            be prefixed with a leading colon, as it may have spaces.
    SERVER
        Used to tell a server that the other end of a new connection is
        a server.

        Parameters
        ----------
        servername: string
            Name of the new server.
        hopcount: int
            How far away the server is.
        info: string
            More information about the server.
    OPER
        Used by a normal user to obtain operator privileges.

        Parameters
        ----------
        user: string
            Username of the user requesting operator privileges.
        password: string
            Password of the user requesting operator privileges.
    QUIT
        End a client session

        Parameters
        ----------
        message: string, optional
            Message to display when ending a client session.
    SQUIT
        Tell about quitting or dead servers.

        Parameters
        ----------
        server: string
            Server whose connection is being broken
        comment: string
            Why the connection is being broken.
    JOIN
        Used by a client to start listening to a specific channel.

        Parameters
        ----------
        channel: string
            Channel name to start listening to.
        key: string
            Password for this channel.
    PART
        Remove the sending client from the list of active users for one
        or more listed channels.

        Parameters
        ----------
        channel: string
            Channel to leave.


    .. _RFC1459: https://tools.ietf.org/html/rfc1459
    """

    # Connection Registration
    PASS = 1
    NICK = 2
    USER = 3
    SERVER = 4
    OPER = 5
    QUIT = 6
    SQUIT = 7

    # Channel operations
    JOIN = 8
    PART = 9
    MODE = 10

    LIST = -1

# TODO: Make default error handlers for some response codes
@IrcCommand.PASS.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.PASS.register_error_handler(IrcError.ERR_ALREADYREGISTERED)

@IrcCommand.NICK.register_error_handler(IrcError.ERR_NONICKNAMEGIVEN)
@IrcCommand.NICK.register_error_handler(IrcError.ERR_NICKNAMEINUSE)
@IrcCommand.NICK.register_error_handler(IrcError.ERR_NICKCOLLISION)
@IrcCommand.NICK.register_error_handler(IrcError.ERR_ERRONEUSNICKNAME)

@IrcCommand.USER.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.USER.register_error_handler(IrcError.ERR_ALREADYREGISTERED)

@IrcCommand.SERVER.register_error_handler(IrcError.ERR_ALREADYREGISTERED)

@IrcCommand.OPER.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.OPER.register_error_handler(IrcError.ERR_NOOPERHOST)
@IrcCommand.OPER.register_error_handler(IrcError.ERR_PASSWDMISMATCH)

@IrcCommand.SQUIT.register_error_handler(IrcError.ERR_NOPRIVILEGES)
@IrcCommand.SQUIT.register_error_handler(IrcError.ERR_NOSUCHSERVER)

@IrcCommand.JOIN.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_INVITEONLYCHAN)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_CHANNELISFULL)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_NOSUCHCHANNEL)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_BANNEDFROMCHAN)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_BADCHANNELKEY)
@IrcCommand.JOIN.register_error_handler(IrcError.ERR_TOOMANYCHANNELS)

@IrcCommand.PART.register_error_handler(IrcError.ERR_NEEDMOREPARAMS)
@IrcCommand.PART.register_error_handler(IrcError.ERR_NOTONCHANNEL)
@IrcCommand.PART.register_error_handler(IrcError.ERR_NOSUCHCHANNEL)

# # TODO: Handle responses differently
# @IrcCommand.OPER.register_error_handler(IrcCommandResponse.RPL_YOUREOPER)
# @IrcCommand.JOIN.register_error_handler(IrcCommandResponse.RPL_TOPIC)
# @IrcCommand.JOIN.register_error_handler(IrcCommandResponse.RPL_NAMEREPLY)

# # TODO: Handle reserved codes differently
# @IrcCommand.JOIN.register_error_handler(IrcReservedCodes.ERR_BADCHANMASK)
class IrcCommandNumericReplyException(Exception):

    def __init__(self, command, error, message=None, **kwargs):
        """Exception to represent an IRC numeric reply.

        Parameters
        ----------
        command: IrcCommand
            The command that received the error.
        error: IrcError
            The numeric reply received
        message: string, default=None
            Optional additional message. The command name, error name,
            and error description will be formatted into it if provided.
        kwargs: dict
            Any additional parameters that can be passed to the error
            description. Will default to a description of each parameter
            if not passed explicitly.
        """

        # Use the default description from RFC 1459
        default_description_parameters = {
            "nickname": "<nickname>",
            "server_name": "<server name>",
            "channel_name": "<channel name>",
            "target": "<target>",
            "mask": "<mask>",
            "file_operation": "<file op>",
            "file": "<file>",
            "user": "<user>",
            "char": "<char>"
        }

        description = getattr(
            getattr(IrcError, "_{}".format(error.name), None), "value", None)

        if description is not None:
            kwargs.update(command=command.name, error=error.value)
            default_description_parameters.update(kwargs)
            description = description.format(**default_description_parameters)

        if message is None:
            message = dedent(
                """
                Command {command.name} had error {error.name}.
                {description}
                """)

        super(IrcCommandNumericReplyException, self).__init__(
            message.format(command=command, error=error, description=description))

@IrcCommand.PASS.register_parameter("password", 0)
@IrcCommand.USER.register_parameter("username", 0)
@IrcCommand.OPER.register_parameter("user", 0)
@IrcCommand.OPER.register_parameter("password", 1)
@IrcCommand.JOIN.register_parameter(
    "key", 1, optional=True, count=1, count_type=CountType.MIN)
@IrcCommand.MODE.register_parameter("limit", 3, optional=True)
@IrcCommand.MODE.register_parameter("user", 4, optional=True)
@IrcCommand.MODE.register_parameter("ban_mask", 5, optional=True)
def always_valid(*args, **kwargs):
    """Validator for parameters that don't need validation, or cannot be
    validated with information at this level of the stack.

    For example, it is impossible to validate that a nickname has no
    duplicates without more detailed knowledge of the servers/channels
    connected to, which isn't available in this context.

    Returns
    -------
    None
    """

    return None

@IrcCommand.NICK.register_parameter("nickname", 0)
def validate_nickname(nickname):
    """Validate that the nickname doesn't exceed the maximum allowed
    length.

    Notes
    -----
    Per RFC2812_, clients SHOULD accept longer strings as they may be
    used in future evolutions of the protocol. This function only emits
    a warning as a result.

    Parameters
    ----------
    nickname: string
        The nickname to validate.

    Returns
    -------
    None

    . _RFC2812: https://tools.ietf.org/html/rfc2812#section-1.2.1
    """

    if len(nickname) > MAX_NICKNAME_LENGTH:
        warnings.warn(dedent(
            """
            Under current IRC standard, nicknames cannot exceed {} characters,
            but this nickname is {} characters long. Per RFC 2812, clients
            SHOULD accept longer strings as they may be used in future
            evolutions of the protocol.
            """.format(MAX_NICKNAME_LENGTH, len(nickname))), FutureWarning)

    return None

@IrcCommand.NICK.register_parameter("hopcount", 1, optional=True)
@IrcCommand.SERVER.register_parameter("hopcount", 1)
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

@IrcCommand.USER.register_parameter("realname", 3)
@IrcCommand.SERVER.register_parameter("info", 2)
@IrcCommand.QUIT.register_parameter("message", 0)
@IrcCommand.SQUIT.register_parameter("comment", 1)
def validate_param_with_spaces(argument):
    """Parameters that allow spaces need a leading colon."""

    if not argument.startswith(":"):
        return dedent(
            """This parameter must have a leading colon because it may
            contain spaces.""")

    return None

@IrcCommand.JOIN.register_parameter(
    "channel", 0, count=1, count_type=CountType.MIN)
@IrcCommand.PART.register_parameter(
    "channel", 0, count=1, count_type=CountType.MIN)
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
            return "Channel name cannot contain `{}`.".format(bad_char)

    return None

@IrcCommand.USER.register_parameter("hostname", 1)
@IrcCommand.USER.register_parameter("servername", 2)
@IrcCommand.SERVER.register_parameter("servername", 0)
@IrcCommand.SQUIT.register_parameter("server", 0)
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

    return None

@IrcCommand.JOIN.register_validator
def same_length_lists(channels, keys):
    """Validate that the two parameter lists are the same length."""

    if keys and len(channels) != len(keys):
        return "Expected same number of channels ({}) and keys ({}).".format(
            len(channels), len(keys))

    return None

@IrcCommand.MODE.register_parameter("channel_or_nickname", 0)
def validate_channel_or_nickname(name):
    """Validate that a name is either a channel or a nickname."""

    is_valid_channel = validate_channel_name(name)
    if is_valid_channel is None:
        return None

    is_valid_nickname = validate_nickname(name)
    if is_valid_nickname is None:
        return None

    return is_valid_channel or is_valid_nickname

@IrcCommand.MODE.register_parameter("mode_modifier", 1)
def validate_mode_modifier(modifier):
    """Validate that something is a valid mode modifier."""

    try:
        IrcModeChanges(modifier)
    except ValueError as e:
        return e.message

    return None

@IrcCommand.MODE.register_parameter(
    "mode", 2, count=1, count_type=CountType.MIN)
def validate_mode(mode):
    """Validate that the mode is an actual mode."""

    try:
        IrcChannelModes(mode)
    except ValueError as e:
        try:
            IrcUserModes(mode)
        except ValueError as e:
            warning.warn(dedent(
                """
                {} is not a valid channel or user mode.
                More modes may be added in the future.
                """.format(mode)))

    return None

@IrcCommand.MODE.register_validator
def validate_mode(name, modifier, mode, limit=None, user=None, ban_mask=None):
    """Validate that the overall mode looks okay."""

    # If it isn't a channel message, disallow that configuration
    if validate_channel_name(name):
        if limit is not None:
            return "No limit may be provided for user MODE commands"

        if user is not None:
            return "No user may be provided for user MODE commands"

        if ban_mask is not None:
            return "No ban mask may be provided for user MODE commands"

        try:
            IrcChannelModes(mode)
        except ValueError as e:
            return e.message

        if (IrcUserModes(mode) is IrcUserModes.OPERATOR
                and IrcModeChanges(modifier) is IrcModeChanges.GIVE):
            return "You can't MODE yourself operator privileges"

        return None

    if (IrcChannelModes(mode) is not IrcChannelModes.LIMIT
            and limit is not None):
        return "When not in limit MODE, no limit should be provided."
    if (IrcChannelModes(mode) is IrcChannelModes.LIMIT
            and limit is None):
        return "When limit MODE, a limit must be provided."

    if (IrcChannelModes(mode) is not IrcChannelModes.BAN
            and ban_mask is not NONE):
        return "When not in ban mask MODE, no ban mask should be provided."
    if (IrcChannelModes(mode) is IrcChannelModes.BAN
            and ban_mask is NONE):
        return "When in ban mask MODE, a ban mask must be provided."

    if (IrcChannelModes(mode) in
            [IrcChannelModes.OPERATOR, IrcChannelModes.ABIILTY,
             IrcChannelModes.KEY]
            and user is None):
        return "When in operator, ability, or key MODE a user must be provided."
    if (IrcChannelModes(mode) not in
            [IrcChannelModes.OPERATOR, IrcChannelModes.ABIILTY,
             IrcChannelModes.KEY]
            and user is not None):
        return dedent("""
            When not in operator, ability, or key MODE a user
            should not be provided.""")

    return None








@IrcCommand.PASS.register_execution
def build_password_message(password):
    """Build the PASS message to send."""

    return "PASS {password}".format(**locals())

@IrcCommand.NICK.register_execution
def build_nick_command(nickname, hopcount=0):

    return "NICK {nickname} {hopcount}".format(**locals())

@IrcCommand.USER.register_execution
def build_user_command(username, hostname, servername, realname):

    return "USER {username} {hostname} {servername} {realname}".format(
        **locals())

@IrcCommand.SERVER.register_execution
def build_server_command(servername, hopcount, info):

    return "SERVER {servername} {hopcount} {info}".format(**locals())

@IrcCommand.OPER.register_execution
def build_oper_command(username, password):

    return "OPER {username} {password}".format(**locals())

@IrcCommand.QUIT.register_execution
def build_quit_command(message=""):

    return "QUIT {message}".format(**locals())

@IrcCommand.SQUIT.register_execution
def build_squit_command(server, comment):

    return "SQUIT {server} {comment}".format(**locals())

@IrcCommand.JOIN.register_execution
def build_join_command(channels, keys=None):

    keys = ','.join(keys or [])
    channels = ','.join(channels)

    return "JOIN {channels} {keys}".format(**locals())

@IrcCommand.PART.register_execution
def build_part_command(channels):

    channels = ",".join(channels)

    return "PART {channels}".format(**locals())
