# from ..compat import *
from commands import IrcCommand

if __name__ == '__main__':
	command = IrcCommand(IrcCommand.JOIN)
	command.execute("test")