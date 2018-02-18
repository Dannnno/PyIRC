from PyIRC.irc.executable_command import (
	ExecutableCommandMixin, InvalidCommandParameters, CommandParameter,
	CommandParameterSet, CountType)
from PyIRC.irc import IrcCommand

import unittest

try:
	range = xrange
except NameError:
	pass

try:
	import enum34 as enum
except ImportError:
	import enum

@enum.unique
class FakeEnum(ExecutableCommandMixin, enum.Enum):
	TEST = 1


class TestCommandParameterSet(unittest.TestCase):

	def test___init___no_parameters(self):
		"""
		Test that constructing a CommandParameterSet without any
		parameters doesn't error.
		"""

		cps = CommandParameterSet()
		self.assertEquals(cps.parameters, [])

	def test___init___some_parameters(self):
		"""
		Test that constructing a CommandParameterSet with some
		parameters doesn't error.
		"""

		params = ['i', 'am', 'a', 'parameter', 'list']
		cps = CommandParameterSet(*params)
		self.assertEquals(cps.parameters, params)

	def test_insert_parameter_no_index(self):
		"""Test that inserting without an index just appends."""

		param = object()
		cps = CommandParameterSet()
		cps.insert_parameter(param)
		self.assertEquals(len(cps.parameters), 1)
		self.assertIs(cps.parameters[0], param)

	def test_insert_parameter_negative_index(self):
		"""Test that a negative index raises."""

		cps = CommandParameterSet()
		params = (object(), -1)
		self.assertRaises(IndexError, cps.insert_parameter, *params)

	def test_insert_parameter_replace(self):
		"""Test that inserting at an existing location replaces."""

		original_param = object()
		cps = CommandParameterSet(original_param)
		new_param = object()
		cps.insert_parameter(new_param, 0)
		self.assertIsNot(cps.parameters[0], original_param)
		self.assertIs(cps.parameters[0], new_param)
		self.assertEquals(len(cps.parameters), 1)

	def test_insert_parameter_append(self):
		"""Test that inserting at length just appends."""

		cps = CommandParameterSet('test', 'params')
		param = object()
		cps.insert_parameter(param, 2)
		self.assertEquals(len(cps.parameters), 3)
		self.assertIs(cps.parameters[2], param)

	def test_insert_parameter_extend(self):
		"""Test that inserting beyond length backfills with None."""

		cps = CommandParameterSet()
		param = object()
		cps.insert_parameter(param, 2)
		self.assertEquals(len(cps.parameters), 3)
		self.assertIs(cps.parameters[2], param)
		for i in range(2):
			self.assertIs(cps.parameters[i], None)

	def test_validate_still_empty(self):
		"""Test that if we still have null parameters, it errors."""

		cps = CommandParameterSet()
		cps.insert_parameter("Test", 2)
		errors = list(cps.validate([]))

		self.assertEquals(len(errors), 1)
		self.assertNotEquals(errors[0], "")


	def test_validate_mismatch_length(self):
		"""
		Test that if the number of values and parameters doesn't match
		it errors.
		"""

		cps = CommandParameterSet()
		cps.insert_parameter("Test")
		errors = list(cps.validate([]))

		self.assertEquals(len(errors), 1)
		self.assertNotEquals(errors[0], "")

def test_something():
	assert True