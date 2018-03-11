# Force Python 3 behaviors
from __future__ import unicode_literals, absolute_import
import enum


MAX_NICKNAME_LENGTH = 9

@enum.unique
class IrcError(enum.Enum):
    """Error codes that can be returned by an IRC server.

    Codes and documentation taken from RFC1459_.

    Attributes
    ----------
    ERR_NOSUCHNICK: 401
        Used to indicate that the nickname parameter supplied to a
        command is unused
    ERR_NOSUCHSERVER: 402
        Used to indicate the server name given currently doesn't exist.
    ERR_NOSUCHCHANNEL: 403
        Used to indicate the given channel name is invalid.
    ERR_CANNOTSENDTOCHAN: 404
        Sent to a user who is either (a) not on a channel which is mode
        +n or (b) not a chanop (or mode +v) on a channel which has mode
        +m set and is trying to send a PRIVMSG message to that channel.
    ERR_TOOMANYCHANNELS: 405
        Sent to a user when they have joined the maximum number of
        allowed channels and they try to join another channel.
    ERR_WASNOSUCHNICK: 406
        Returned by WHOWAS to indicate there is no history information
        for that nickname.
    ERR_TOOMANYTARGETS: 407
        Returned to a client which is attempting to send a
        PRIVMSG/NOTICE using the user@host destination format and for a
        user@host which has several occurrences.
    ERR_NOORIGIN: 409
        PING or PONG message missing the originator parameter which is
        required since these commands must work without valid prefixes.
    ERR_NORECIPIENT: 411
        No recipient given.
    ERR_NOTEXTTOSEND: 412
        Returned by PRIVMSG to indicate that the message wasn't
        delivered because there was no text to send.
    ERR_NOTOPLEVEL: 413
        Returned by PRIVMSG to indicate that the message wasn't
        delivered because there was no top level domain specified.
        Returned when an invalid use of "PRIVMSG ${server_name}" or
        "PRIVMSG #<host>" is attempted.
    ERR_WILDTOPLEVEL: 414
        Returned by PRIVMSG to indicate that the message wasn't
        delivered because there was a wildcard in the top level domain.
        Returned when an invalid use of "PRIVMSG ${server_name}" or
        "PRIVMSG #<host>" is attempted.
    ERR_UNKNOWNCOMMAND: 421
        Returned to a registered client to indicate that the command
        sent is unknown by the server.
    ERR_NOMOTD: 422
        Server's MOTD file could not be opened by the server.
    ERR_NOADMININFO:423
        Returned by a server in response to an ADMIN message when there
        is an error in finding the appropriate information.
    ERR_FILEERROR: 424
        Generic error message used to report a failed file operation
        during the processing of a message.
    ERR_NONICKNAMEGIVEN: 431
        Returned when a nickname parameter expected for a command and
        isn't found.
    ERR_ERRONEUSNICKNAME: 432
        Returned after receiving a NICK message which contains
        characters which do not fall in the defined set. See section
        x.x.x for details on valid nicknames.
    ERR_NICKNAMEINUSE: 433
        Returned when a NICK message is processed that results in an
        attempt to change to a currently existing nickname.
    ERR_NICKCOLLISION: 436
        Returned by a server to a client when it detects a nickname
        collision (registered of a NICK that already exists by another
        server).
    ERR_USERNOTINCHANNEL: 441
        Returned by the server to indicate that the target user of the
        command is not on the given channel.
    ERR_NOTONCHANNEL: 442
        Returned by the server whenever a client tries to perform a
        channel effecting command for which the client isn't a member.
    ERR_USERONCHANNEL: 443
        Returned when a client tries to invite a user to a channel they
        are already on.
    ERR_NOLOGIN: 444
        Returned by the summon after a SUMMON command for a user was
        unable to be performed since they were not logged in.
    ERR_SUMMONDISABLED: 445
        Returned as a response to the SUMMON command.  Must be returned
        by any server which does not implement it.
    ERR_USERSDISABLED: 446
        Returned as a response to the USERS command.  Must be returned
        by any server which does not implement it.
    ERR_NOTREGISTERED: 451
        Returned by the server to indicate that the client must be
        registered before the server will allow it to be parsed in
        detail.
    ERR_NEEDMOREPARAMS: 461
        Returned by the server by numerous commands to indicate to the
        client that it didn't supply enough parameters.
    ERR_ALREADYREGISTRED: 462
        Returned by the server to any link which tries to change part of
        the registered details (such as password or user details from
        second USER message).
    ERR_NOPERMFORHOST: 463
        Returned to a client which attempts to register with a server
        which does not been setup to allow connections from the host the
        attempted connection is tried.
    ERR_PASSWDMISMATCH: 464
        Returned to indicate a failed attempt at registering a
        connection for which a password was required and was either not
        given or incorrect.
    ERR_YOUREBANNEDCREEP: 465
        Returned after an attempt to connect and register yourself with
        a server which has been setup to explicitly deny connections to
        you.
    ERR_KEYSET: 467
        Chnnel key already set.
    ERR_CHANNELISFULL: 471
        Can't join channel (+l).
    ERR_UNKNOWNMODE: 472
        Returned when an unknown mode character is passed.
    ERR_INVITEONLYCHAN: 473
        Can't join channel (+i).
    ERR_BANNEDFROMCHAN: 474
        Can't join channel (+b).
    ERR_BADCHANNELKEY: 475
        Can't join channel (+k).
    ERR_NOPRIVILEGES: 481
        Any command requiring operator privileges to operate must return
        this error to indicate the attempt was unsuccessful.
    ERR_CHANOPRIVSNEEDED: 482
        Any command requiring 'chanop' privileges (such as MODE
        messages) must return this error if the client making the
        attempt is not a chanop on the specified channel.
    ERR_CANTKILLSERVER: 483
        Any attempts to use the KILL command on a server are to be
        refused and this error returned directly to the client.
    ERR_NOOPERHOST: 491
        If a client sends an OPER message and the server has not been
        configured to allow connections from the client's host as an
        operator, this error must be returned.
    ERR_UMODEUNKNOWNFLAG: 501
        Returned by the server to indicate that a MODE message was sent
        with a nickname parameter and that the a mode flag sent was not
        recognized.
    ERR_USERSDONTMATCH: 502
        Error sent to any user trying to view or change the user mode
        for a user other than themselves.

    .. _RFC1459: https://tools.ietf.org/html/rfc1459
    """

    ERR_NOSUCHNICK = 401
    _ERR_NOSUCHNICK = "{nickname} :No such nick/channel"
    ERR_NOSUCHSERVER = 402
    _ERR_NOSUCHSERVER = "{server_name} :No such server"
    ERR_NOSUCHCHANNEL = 403
    _ERR_NOSUCHCHANNEL ="{channel_name} :No such channel"
    ERR_CANNOTSENDTOCHAN = 404
    _ERR_CANNOTSENDTOCHAN = "{channel_name} :Cannot send to channel"
    ERR_TOOMANYCHANNELS = 405
    _ERR_TOOMANYCHANNELS = "{channel_name} :You have joined too many channels"
    ERR_WASNOSUCHNICK = 406
    _ERR_WASNOSUCHNICK = "{nickname} :There was no such nickname"
    ERR_TOOMANYTARGETS = 407
    _ERR_TOOMANYTARGETS = "{target} :Duplicate recipients. No message delivered"
    ERR_NOORIGIN = 409
    _ERR_NOORIGIN = ":No origin specified"
    ERR_NORECIPIENT = 411
    _ERR_NORECIPIENT = ":No recipient given ({command})"
    ERR_NOTEXTTOSEND = 412
    _ERR_NOTEXTTOSEND = ":No text to send"
    ERR_NOTOPLEVEL = 413
    _ERR_NOTOPLEVEL = "{mask} :No toplevel domain specified"
    ERR_WILDTOPLEVEL = 414
    _ERR_WILDTOPLEVEL = "{mask} :Wildcard in toplevel domain"
    ERR_UNKNOWNCOMMAND = 421
    _ERR_UNKNOWNCOMMAND = "{command} :Unknown command"
    ERR_NOMOTD = 422
    _ERR_NOMOTD = ":MOTD File is missing"
    ERR_NOADMININFO = 423
    _ERR_NOADMININFO = "{server_name} :No administrative info available"
    ERR_FILEERROR = 424
    _ERR_FILEERROR = ":File error doing {file_operation} on {file}"
    ERR_NONICKNAMEGIVEN = 431
    _ERR_NONICKNAMEGIVEN = ":No nickname given"
    ERR_ERRONEUSNICKNAME = 432
    _ERR_ERRONEUSNICKNAME = "{nickname} :Erroneus nickname"
    ERR_NICKNAMEINUSE = 433
    _ERR_NICKNAMEINUSE = "{nickname} :Nickname is already in use"
    ERR_NICKCOLLISION = 436
    _ERR_NICKCOLLISION = "{nickname} :Nickname collision KILL"
    ERR_USERNOTINCHANNEL = 441
    _ERR_USERNOTINCHANNEL = "{nickname} {channel_name} :They aren't on that channel"
    ERR_NOTONCHANNEL = 442
    _ERR_NOTONCHANNEL = "{channel_name} :You're not on that channel"
    ERR_USERONCHANNEL = 443
    _ERR_USERONCHANNEL = "{user} {channel_name} :is already on channel"
    ERR_NOLOGIN = 444
    _ERR_NOLOGIN = "{user} :User not logged in"
    ERR_SUMMONDISABLED = 445
    _ERR_SUMMONDISABLED = ":SUMMON has been disabled"
    ERR_USERSDISABLED = 446
    _ERR_USERSDISABLED = ":USERS has been disabled"
    ERR_NOTREGISTERED = 451
    _ERR_NOTREGISTERED = ":You have not registered"
    ERR_NEEDMOREPARAMS = 461
    _ERR_NEEDMOREPARAMS = "{command} :Not enough parameters"
    ERR_ALREADYREGISTERED = 462
    _ERR_ALREADYREGISTERED = ":You may not reregister"
    ERR_NOPERMFORHOST = 463
    _ERR_NOPERMFORHOST = ":Your host isn't among the privileged"
    ERR_PASSWDMISMATCH = 464
    _ERR_PASSWDMISMATCH = ":Password incorrect"
    ERR_YOUREBANNEDCREEP = 465
    _ERR_YOUREBANNEDCREEP = ":You are banned from this server"
    ERR_KEYSET = 467
    _ERR_KEYSET = "{channel_name} :Channel key already set"
    ERR_CHANNELISFULL = 471
    _ERR_CHANNELISFULL = "{channel_name} :Cannot join channel (+l)"
    ERR_UNKNOWNMODE = 472
    _ERR_UNKNOWNMODE = "{char} :is unknown mode char to me"
    ERR_INVITEONLYCHAN = 473
    _ERR_INVITEONLYCHAN = "{channel_name} :Cannot join channel (+i)"
    ERR_BANNEDFROMCHAN = 474
    _ERR_BANNEDFROMCHAN = "{channel_name} :Cannot join channel (+b)"
    ERR_BADCHANNELKEY = 475
    _ERR_BADCHANNELKEY = "{channel_name} :Cannot join channel (+k)"
    ERR_NOPRIVILEGES = 481
    _ERR_NOPRIVILEGES = ":Permission Denied- You're not an IRC operator"
    ERR_CHANOPRIVSNEEDED = 482
    _ERR_CHANOPRIVSNEEDED = "{channel_name} :You're not channel operator"
    ERR_CANTKILLSERVER = 483
    _ERR_CANTKILLSERVER = ":You cant kill a server!"
    ERR_NOOPERHOST = 491
    _ERR_NOOPERHOST = ":No O-lines for your host"
    ERR_UMODEUNKNOWNFLAG = 501
    _ERR_UMODEUNKNOWNFLAG = ":Unknown MODE flag"
    ERR_USERSDONTMATCH = 502
    _ERR_USERSDONTMATCH = ":Cant change mode for other users"

@enum.unique
class IrcCommandResponse(enum.Enum):
    """Response codes that can be returned by an IRC server.

    Codes and documentation taken from RFC1459_.

    Attributes
    ----------
    RPL_TRACELINK: 200
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.

        Sent by any server which handles a TRACE message and has to pass
        it on to another server. The list of RPL_TRACELINKs sent in
        response to a TRACE command traversing the IRC network should
        reflect the actual connectivity of the servers themselves along
        that path.
    RPL_TRACECONNECTING: 201
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.

        Used for connections which have not been fully established and
        are still attempting to connect.
    RPL_TRACEHANDSHAKE: 202
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.

        Used for connections which have not been fully established and
        are in the process of completing the 'server handshake'.
    RPL_TRACEUNKNOWN: 203
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.

        Used for connections which have not been fully established and
        are unknown.
    RPL_TRACEOPERATOR: 204
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.
    RPL_TRACEUSER: 205
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.
    RPL_TRACESERVER: 206
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.
    RPL_TRACENEWTYPE: 208
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.

        Used for any connection which does not fit in the other
        categories but is being displayed anyway.
    RPL_UMODEIS: 221
        To answer a query about a client's own mode, RPL_UMODEIS is sent back.
    RPL_LUSERCLIENT: 251
        In processing an LUSERS message, the server sends a set of
        replies from RPL_LUSERCLIENT, RPL_LUSEROP, RPL_USERUNKNOWN,
        RPL_LUSERCHANNELS and RPL_LUSERME. When replying, a server must
        send back RPL_LUSERCLIENT and RPL_LUSERME. The other replies are
        only sent back if a non-zero count is found for them.
    RPL_ADMINME: 256
        When replying to an ADMIN message, a server is expected to use
        replies RLP_ADMINME through to RPL_ADMINEMAIL and provide a text
        message with each. For RPL_ADMINLOC1 a description of what city,
        state and country the server is in is expected, followed by
        details of the university and department (RPL_ADMINLOC2) and
        finally the administrative contact for the server (an email
        address here is required) in RPL_ADMINEMAIL.
    RPL_TRACELOG: 261
        Returned by the server in response to the TRACE message. How
        many are returned is dependent on the the TRACE message and
        whether it was sent by an operator or not. There is no
        predefined order for which occurs first.
    RPL_NONE: 300
        Dummy reply number. Not used.
    RPL_AWAY: 301
        Used with the AWAY command (if allowed). Sent to any client
        sending a PRIVMSG to a client which is away. Only sent by the
        server to which the client is connected.
    RPL_USERHOST: 302
        Reply format used by USERHOST to list replies to the query list.
        The reply string is composed as follows:

        <reply> ::= {nickname}['*'] '=' <'+'|'-'><hostname>

        The '*' indicates whether the client has registered as an
        Operator. The '-' or '+' characters represent whether the client
        has set an AWAY message or not respectively.
    RPL_ISON: 303
        Reply format used by ISON to list replies to the query list.
    RPL_UNAWAY: 305
        Used with the AWAY command (if allowed). Sent when the client
        removes their AWAY message.
    RPL_NOWAWAY: 306
        Used with the AWAY command (if allowed). Sent when the client
        sets their AWAY message.
    RPL_WHOISUSER: 311
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply.  The '*' in RPL_WHOISUSER
        is there as the literal character and not as a wild card.
    RPL_WHOISSERVER: 312
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply.
    RPL_WHOISOPERATOR: 313
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply.
    RPL_WHOWASUSER: 314
        When replying to a WHOWAS message, a server must use the replies
        RPL_WHOWASUSER, RPL_WHOISSERVER or ERR_WASNOSUCHNICK for each
        nickname in the presented list.
    RPL_WHOISIDLE: 317
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply.
    RPL_ENDOFWHOIS: 318
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply. The RPL_ENDOFWHOIS reply is
        used to mark the end of processing a WHOIS message.
    RPL_WHOISCHANNELS: 319
        Generated in response to a WHOIS message. Given that there are
        enough parameters present, the answering server must either
        formulate a reply out of the above numerics (if the query nick
        is found) or return an error reply. For each reply set, only
        RPL_WHOISCHANNELS may appear more than once (for long lists of
        channel names). The '@' and '+' characters next to the channel
        name indicate whether a client is a channel operator or has been
        granted permission to speak on a moderated channel.
    RPL_WHOWASUSER: 314
        When replying to a WHOWAS message, a server must use the replies
        RPL_WHOWASUSER, RPL_WHOISSERVER or ERR_WASNOSUCHNICK for each
        nickname in the presented list.
    RPL_ENDOFWHO: 315
        Used to answer a WHO message. If there is a list of parameters
        supplied with a WHO message, must be sent after processing each
        list item with <name> being the item.
    RPL_LISTSTART: 321
        Marks the start of the server's response to a LIST ommand. Sent
        even if there are no channels available to return.
    RPL_LIST: 322
        Marks the actual content of the server's response to a LIST
        command. Not sent if there are no channels available to return.
    RPL_LISTEND: 323
        Marks the end of the server's response to a LIST command. Sent
        even if there are no channels available to return.
    RPL_CHANNELMODEIS: 324
        Returns the channel mode.
    RPL_NOTOPIC: 331
        Returned when the server processes a TOPIC message and a topic
        is not set.
    RPL_TOPIC: 332
        Returned when the server processes a TOPIC message and a topic
        is set.
    RPL_INVITING: 341
        Returned by the server to indicate that the attempted INVITE
        message was successful and is being passed onto the end client.
    RPL_SUMMONING: 342
        Returned by a server answering a SUMMON message to indicate that
        it is summoning that user.
    RPL_VERSION: 351
        Reply by the server showing its version details. The <version>
        is the version of the software being used (including any
        patchlevel revisions) and the <debuglevel> is used to indicate
        if the server is running in "debug mode".

        The "comments" field may contain any comments about the version
        or further version details.
    RPL_ENDOFWHOWAS: 369
        When replying to a WHOWAS message, a server must use the replies
        RPL_WHOWASUSER, RPL_WHOISSERVER or ERR_WASNOSUCHNICK for each
        nickname in the presented list.  At the end of all reply
        batches, there must be RPL_ENDOFWHOWAS (even if there was only
        one reply and it was an error).
    RPL_WHOREPLY: 352
        Used to answer a WHO message. Only sent if there is an
        appropriate match to the query.
    RPL_NAMEREPLY: 353
        Part of the reply to a NAMES message. If no channel found in the
        query, this part is omitted, unless the NAMES command is send
        with no parameters and all visible channels and contents are
        sent back in a series of RPL_NAMEREPLY messages.
    RPL_LINKS: 364
        Response to the LINKS message.
    RPL_ENDOFLINKS: 365
        Marks the end of a series of RPL_LINKS messages in response to a
        LINKS message.
    RPL_ENDOFNAMES: 366
        Part of the reply to a NAMES message. Marks the end of a series
        of RPL_NAMEREPLY messages (possible 0 if no channels matched).
    RPL_BANLIST: 367
        Sent for each active banid in a given channel.
    RPL_ENDOFBANLIST: 368
        Marks the end of a list of active bans in a given channel.
    RPL_INFO: 371
        A server responding to an INFO message is required to send all
        of its 'info' in a series of these messages.
    RPL_MOTD: 372
        Single line of the MOTD file sent in response to the MOTD
        message; each line is no longer than 80 characters.
    RPL_ENDOFINFO: 374
        Indicates the end of a server's response to an INFO message.
    RPL_MOTDSTART: 375
        Marks the start of the server response to the MOTD message.
    RPL_ENDOFMOTD: 376
        Marks the end of the server response to the MOTD message.
    RPL_YOUREOPER: 381
        RPL_YOUREOPER is sent back to a client which has just
        successfully issued an OPER message and gained operator status.
    RPL_REHASHING: 382
        If the REHASH option is used and an operator sends a REHASH
        message, an RPL_REHASHING is sent back to the operator.
    RPL_TIME: 391
        When replying to the TIME message, a server must send the reply
        using the RPL_TIME format. The string showing the time need only
        contain the correct day and time there. There is no further
        requirement for the time string.
    RPL_USERSSTART: 392
        Marks the start of the server response to a USERS message.
    RPL_USERS: 393
        Marks a user on a given channel.
    RPL_ENDOFUSERS: 394
        Marks the end of the server response to a USERS message.
    RPL_NOUSERS: 395
        Indicates that there are no users on the channel.


    .. _RFC1459: https://tools.ietf.org/html/rfc1459
    """

    RPL_TRACELINK = 200
    _RPL_TRACELINK = "Link <version & debug level> <destination> "\
                         "<next server>"
    RPL_TRACECONNECTING = 201
    _RPL_TRACECONNECTING = "Try. <class> {server_name}"
    RPL_TRACEHANDSHAKE = 202
    _RPL_TRACEHANDSHAKE = "H.S. <class> {server_name}"
    RPL_TRACEUNKNOWN = 203
    _RPL_TRACEUNKNOWN = "???? <class> [<client IP address in dot form>]"
    RPL_TRACEOPERATOR = 204
    _RPL_TRACEOPERATOR = "Oper <class> {nickname}"
    RPL_TRACEUSER = 205
    _RPL_TRACEUSER = "User <class> {nickname}"
    RPL_TRACESERVER = 206
    _RPL_TRACESERVER = "Serv <class> <int>S <int>C {server_name} "\
                         "<nick!user|*!*>@<host|server>"
    RPL_TRACENEWTYPE = 208
    _RPL_TRACENEWTYPE = "<newtype> 0 <client name>"
    RPL_STATSLINKINFO = 211
    _RPL_STATSLINKINFO = "<linkname> <sendq> <sent messages> " \
                             "<sent bytes> <received messages> " \
                             "<received bytes> <time open>"
    RPL_STATSCOMMANDS = 212
    _RPL_STATSCOMMANDS  = "{command} <count>"
    RPL_STATSCLINE = 213
    _RPL_STATSCLINE = "C <host> * <name> <port> <class>"
    RPL_STATSNLINE = 214
    _RPL_STATSNLINE = "N <host> * <name> <port> <class>"
    RPL_STATSILINE = 215
    _RPL_STATSILINE = "I <host> * <host> <port> <class>"
    RPL_STATSKLINE = 216
    _RPL_STATSKLINE = "K <host> * <username> <port> <class>"
    RPL_STATSYLINE = 218
    _RPL_STATSYLINE = "Y <class> <ping frequency> <connect frequency> " \
                          "<max sendq>"
    RPL_ENDOFSTATS = 219
    _RPL_ENDOFSTATS = "<stats letter> :End of /STATS report"
    RPL_UMODEIS = 221
    _RPL_UMODEIS = "<user mode string>"
    RPL_STATSLLINE = 241
    _RPL_STATSLLINE = "L <hostmask> * <servername> <maxdepth>"
    RPL_STATSUPTIME = 242
    _RPL_STATSUPTIME = ":Server Up %d days %d:%02d:%02d"
    RPL_STATSOLINE = 243
    _RPL_STATSOLINE = "O <hostmask> * <name>"
    RPL_STATSHLINE = 244
    _RPL_STATSHLINE = "H <hostmask> * <servername>"
    RPL_LUSERCLIENT = 251
    _RPL_LUSERCLIENT = ":There are <integer> users and <integer> " \
                           "invisible on <integer> servers"
    RPL_LUSEROP = 252
    _RPL_LUSEROP = "<integer> :operator(s) online"
    RPL_LUSERUNKNOWN = 253
    _RPL_LUSERUNKNOWN = "<integer> :unknown connection(s)"
    RPL_LUSERCHANNELS = 254
    _RPL_LUSERCHANNELS = "<integer> :channels formed"
    RPL_LUSERME = 255
    _RPL_LUSERME = ":I have <integer> clients and <integer> \
                          servers"
    RPL_ADMINME = 256
    _RPL_ADMINME = "{server_name} :Administrative info"
    RPL_ADMINLOC1 = 257
    _RPL_ADMINLOC1 = ":<admin info1>"
    RPL_ADMINLOC2 = 258
    _RPL_ADMINLOC2 = ":<admin info2>"
    RPL_ADMINEMAIL = 259
    _RPL_ADMINEMAIL = ":<admin mail>"
    RPL_TRACELOG = 261
    _RPL_TRACELOG = "File <logfile> <debug level>"
    RPL_NONE = 300
    _RPL_NONE = ""
    RPL_AWAY = 301
    _RPL_AWAY = "{nickname} :<away message>"
    RPL_USERHOST = 302
    _RPL_USERHOST = ":[<reply>{<space><reply>}]"
    RPL_ISON = 303
    _RPL_ISON = ":[{nickname} {<space>{nickname}}]"
    RPL_UNAWAY = 305
    _RPL_UNAWAY = ":You are no longer marked as being away"
    RPL_NOWAWAY = 306
    _RPL_NOWAWAY = ":You have been marked as being away"
    RPL_WHOISUSER = 311
    _RPL_WHOISUSER = "{nickname} {user} <host> * :<real name>"
    RPL_WHOISSERVER = 312
    _RPL_WHOISSERVER = "{nickname} {server_name} :<server info>"
    RPL_WHOISOPERATOR = 313
    _RPL_WHOISOPERATOR = "{nickname} :is an IRC operator"
    RPL_WHOWASUSER = 314
    _RPL_WHOWASUSER = "<former nick> {user} <host> * :<real name>"
    RPL_ENDOFWHO = 315
    _RPL_ENDOFWHO = "<name> :End of /WHO list"
    RPL_WHOISIDLE = 317
    _RPL_WHOISIDLE = "{nickname} <integer> :seconds idle"
    RPL_ENDOFWHOIS = 318
    _RPL_ENDOFWHOIS = "{nickname} :End of /WHOIS list"
    RPL_WHOISCHANNELS = 319
    _RPL_WHOISCHANNELS = "{nickname} :{[@|+]{channel_name}<space>}"
    RPL_LISTSTART = 321
    _RPL_LISTSTART = "Channel :Users  Name"
    RPL_LIST = 322
    _RPL_LIST = "{channel_name} <# visible> :<topic>"
    RPL_LISTEND = 323
    _RPL_LISTEND = ":End of /LIST"
    RPL_CHANNELMODEIS = 324
    _RPL_CHANNELMODEIS = "{channel_name} <mode> <mode params>"
    RPL_NOTOPIC = 331
    _RPL_NOTOPIC = "{channel_name} :No topic is set"
    RPL_TOPIC = 332
    _RPL_TOPIC = "{channel_name} :<topic>"
    RPL_INVITING = 341
    _RPL_INVITING = "{channel_name} {nickname}"
    RPL_SUMMONING = 342
    _RPL_SUMMONING = "{user} :Summoning user to IRC"
    RPL_VERSION = 351
    _RPL_VERSION = "<version>.<debuglevel> {server_name} :<comments>"
    RPL_WHOREPLY = 352
    _RPL_WHOREPLY = "{channel_name} {user} <host> {server_name} {nickname} " \
                        "<H|G>[*][@|+] :<hopcount> <real name>"
    RPL_NAMEREPLY = 353
    _RPL_NAMEREPLY = "{channel_name} :[[@|+]{nickname} [[@|+]{nickname} [...]]]"
    RPL_LINKS = 364
    _RPL_LINKS = "{mask} {server_name} :<hopcount> <server info>"
    RPL_ENDOFLINKS = 365
    _RPL_ENDOFLINKS = "{mask} :End of /LINKS list"
    RPL_ENDOFNAMES = 366
    _RPL_ENDOFNAMES = "{channel_name} :End of /NAMES list"
    RPL_BANLIST = 367
    _RPL_BANLIST = "{channel_name} <banid>"
    RPL_ENDOFBANLIST = 368
    _RPL_ENDOFBANLIST = "{channel_name} :End of channel ban list"
    RPL_ENDOFWHOWAS = 369
    _RPL_ENDOFWHOWAS = "{nickname} :End of WHOWAS"
    RPL_INFO = 371
    _RPL_INFO = ":<string>"
    RPL_MOTD = 372
    _RPL_MOTD = ":- <text>"
    RPL_ENDOFINFO = 374
    _RPL_ENDOFINFO = ":End of /INFO list"
    RPL_MOTDSTART = 375
    _RPL_MOTDSTART = ":- {server_name} Message of the day - "
    RPL_ENDOFMOTD = 376
    _RPL_ENDOFMOTD = ":End of /MOTD command"
    RPL_YOUREOPER = 381
    _RPL_YOUREOPER = ":You are now an IRC operator"
    RPL_REHASHING = 382
    _RPL_REHASHING = "<config file> :Rehashing"
    RPL_TIME = 391
    _RPL_TIME = "{server_name} :<string showing server's local time>"
    RPL_USERSSTART = 392
    _RPL_USERSSTART = ":UserID   Terminal  Host"
    RPL_USERS = 393
    _RPL_USERS = ":%-8s %-9s %-8s"
    RPL_ENDOFUSERS = 394
    _RPL_ENDOFUSERS = ":End of users"
    RPL_NOUSERS = 395
    _RPL_NOUSERS = ":Nobody logged in"


@enum.unique
class IrcReservedCodes(enum.Enum):
    """Reserved IRC codes that are not generally supported.

    These numerics fall into one of the following categories:
        1. no longer in use
        2. reserved for future planned use
        3. in current use but are part of a non-generic 'feature' of
           the current IRC server
    """

    RPL_TRACECLASS = 209
    RPL_STATSQLINE = 217
    RPL_ENDOFSERVICES = 232
    RPL_SERVICEINFO = 231
    RPL_SERVICE = 233
    RPL_SERVLIST = 234
    RPL_SERVLISTEND = 235
    RPL_WHOISCHANOP = 316
    RPL_KILLDONE = 361
    RPL_CLOSING = 362
    RPL_CLOSEEND = 363
    RPL_INFOSTART = 373
    RPL_MYPORTIS = 384
    ERR_YOUWILLBEBANNED = 466
    ERR_BADCHANMASK = 476
    ERR_NOSERVICEHOST = 492

@enum.unique
class IrcChannelModes(enum.Enum):
    """IRC channel modes for the MODE command."""

    OPERATOR = 'o'
    PRIVATE = 'p'
    SECRET = 's'
    INVITE = 'i'
    TOPIC = 't'
    NO_MESSAGES  = 'n'
    MODERATED = 'm'
    LIMIT = 'l'
    BAN = 'b'
    ABILITY = 'v'
    KEY = 'k'

@enum.unique
class IrcUserModes(enum.Enum):
    """IRC user modes for the MODE command."""

    INVISIBLE = 'i'
    SERVER_NOTICES = 's'
    WALLOP = 'w'
    OPERATOR = 'o'

@enum.unique
class IrcModeChanges(enum.Enum):
    """Modifiers for user/channel modes."""

    GIVE = "+"
    TAKE = "-"
