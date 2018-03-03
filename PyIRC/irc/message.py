import enum
import re
import sys


# Compile our regular expressions
if sys.version_info.major < 3:
	# Unnecessary before Python 3
	re.ASCII = 0
standard_flags = re.ASCII | re.VERBOSE | re.IGNORECASE
letter = r"[a-z]"
number = r"\d"
special = r"[\[\]\\`\^\{\}-]"
nonwhite = r"[^\x20\x00\x0d\x0a]"
name = r"""
	(?:{letter}|{number}          # RFC 1123 relaxed to letter or number
	(?:
		(?:{letter}|{number}|\-)* # Letters, numbers, or hyphens
		(?:{letter}|{number})     # Ending on a letter or number
	)?)""".format(**locals())
user = r"{nonwhite}+".format(**locals())
host = r"{name}(?:\.{name})*".format(**locals())
servername = re.compile(host, standard_flags)
nickname = re.compile(
	r"""{letter}                         # Leading letter
		(?:{letter}|{number}|{special})* # Then the rest of the name
		(?:!({user}))?                   # Then an optional !user
		(?:@({host}))?                   # Then an optional at-hostname
		""".format(**locals()),
	standard_flags)

@enum.unique
class MessageErrorEnum(enum.Enum):
	"""Enum holding exception messages for invalid messages."""

	# General message errors
	END_WITH_NEWLINE = "Message must end with carriage return - line feed pair"

	# Prefix errors
	SPACE_AFTER_COLON = "Colon must not have a space immediately following it."
	NOT_HOST_OR_NICK = "Prefix doesn't look liek either a hostname or nickname"

class InvalidMessageException(Exception):
	"""Indicates an invalid message."""

	def __init__(self, error_code):
		"""Create a new exception.

		Parameters
		----------
		error_code: MessageErrorEnum
			Code indicating which error occurred.
		"""

		super(InvalidMessageException, self).__init__(error_code.value)

def validate_message(message_content):
	"""

	"""

	if not message_content.endswith("\r\n"):
		raise InvalidMessageException(MessageErrorEnum.END_WITH_NEWLINE)

	if len(message_content) > 512:
		return "Message is {} characters long, but cannot exceed 512.".format(
			len(message_content))

	prefix, message_content = extract_prefix(message_content)
	
	return None


def extract_prefix(message_content):
	"""
	Extract the optional prefix from a message as per RFC1459_, RFC952_,
	and RFC1123_.

	Does no additional validation of the prefix as per RFC1459_; whether
	a prefix can be a server name or nickname depends on the context,
	which the caller must be aware of.

	Returns
	-------
	prefix: string
		The prefix of the message. May be an empty string if there is no
		prefix to the messsage.
	message_content: string
		The remainder of the message after the prefix is removed.

	.. _RFC1459: https://tools.ietf.org/html/rfc1459#section-2.3.1
	.. _RFC952: https://tools.ietf.org/html/rfc952
	.. _RFC1123: https://tools.ietf.org/html/rfc1123#page-13
	"""

	# If there is a prefix, there must be a leading colon
	if not message_content.startswith(':'):
		return "", message_content

	# Prefix is delimited by a space
	delim_index = message_content.find(' ')
	if delim_index == 1:  # The colon must not be followed by a space
		raise InvalidMessageException(MessageErrorEnum.SPACE_AFTER_COLON)

	prefix = message_content[1:delim_index]
	# Don't include any leading spaces
	message_content = message_content[delim_index:].lstrip()

	if nickname.match(prefix) or servername.match(prefix):
		return prefix, message_content

	raise InvalidMessageException(MessageErrorEnum.NOT_HOST_OR_NICK)





