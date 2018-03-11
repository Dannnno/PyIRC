from PyIRC.irc.executable_command import (
	ExecutableCommandMixin, InvalidCommandParametersException, CommandParameter,
	CommandParameterSet, CountType, NoHandlerExcepetion)

import unittest

try:
	range = xrange
except NameError:
	pass

try:
	import enum34 as enum
except ImportError:
	import enum


def something_bad(x):
	return "Something Bad"

def something_good(x):
	return None


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

	def test_validate_values_good(self):
		"""Test that all parameters validate correctly."""

		cps = CommandParameterSet()
		cps.insert_parameter(CommandParameter("test", something_good))
		errors = list(cps.validate([1]))

		self.assertEquals(len(errors), 0)

	def test_validate_values_bad(self):
		"""Test that all parameters validate correctly."""

		cps = CommandParameterSet()
		cps.insert_parameter(CommandParameter("test", something_bad))
		errors = list(cps.validate([1]))

		self.assertEquals(len(errors), 1)
		self.assertNotEquals(errors[0], "")

	def test_validate_values_some_bad(self):
		"""Test that all parameters validate correctly."""

		cps = CommandParameterSet()
		cps.insert_parameter(CommandParameter("test", something_bad))
		cps.insert_parameter(CommandParameter("test2", something_good))
		errors = list(cps.validate([1, 2]))

		self.assertEquals(len(errors), 1)
		self.assertNotEquals(errors[0], "")

	def test___repr___empty_round_trippable(self):
		"""Test that __repr__ can be round-tripped for empty parameters."""

		cps = CommandParameterSet()
		cps2 = eval(repr(cps))

		self.assertEquals(cps, cps2)

	def test___repr___nonempty_round_trippable(self):
		"""Test that __repr__ can be round-tripped non-empty params."""

		cps = CommandParameterSet(CommandParameter("test", something_bad))
		cps2 = eval(repr(cps))

		self.assertTrue(cps == cps2)

	def test___eq___empty(self):
		"""Test that two empty CommandParameterSets are equal."""

		cps = CommandParameterSet()
		cps2 = CommandParameterSet()

		self.assertEquals(cps, cps2)

	def test___eq___same_length(self):
		"""Test that two non-empty CommandParameterSets are equal."""

		cps = CommandParameterSet(CommandParameter("test", something_bad))
		cps2 = CommandParameterSet(CommandParameter("test", something_bad))

		self.assertTrue(cps, cps2)

	def test___eq___diff_length(self):
		"""Test that two non-empty CommandParameterSets are not equal."""

		cps = CommandParameterSet(CommandParameter("test", something_bad))
		cps2 = CommandParameterSet(
			CommandParameter("test", something_bad),
			CommandParameter("test", something_bad))

		self.assertFalse(cps == cps2)

	def test___ne___empty(self):
		"""Test that two empty CommandParameterSets are equal."""

		cps = CommandParameterSet()
		cps2 = CommandParameterSet()

		self.assertFalse(cps != cps2)

	def test___ne___same_length(self):
		"""Test that two non-empty CommandParameterSets are equal."""

		cps = CommandParameterSet(CommandParameter("test", something_bad))
		cps2 = CommandParameterSet(CommandParameter("test", something_bad))

		self.assertFalse(cps != cps2)

	def test___ne___diff_length(self):
		"""Test that two non-empty CommandParameterSets are not equal."""

		cps = CommandParameterSet(CommandParameter("test", something_bad))
		cps2 = CommandParameterSet(
			CommandParameter("test", something_bad),
			CommandParameter("test", something_bad))

		self.assertTrue(cps != cps2)

	def test___len__(self):
		"""
		Test that the length of a CommandParameterSet is the length of
		its parameters.
		"""

		cps = CommandParameterSet(
			CommandParameter("test", something_bad),
			CommandParameter("test", something_bad))

		self.assertEquals(len(cps), len(cps.parameters))


class TestCommandParameter(unittest.TestCase):

	def test___init___no_error(self):
		"""Test that constructing a normal CommandParameter works."""

		cp = CommandParameter("test", something_bad)

		self.assertEquals(cp.name, "test")
		self.assertEquals(cp.count, 1)
		self.assertIs(cp.validator, something_bad)
		self.assertIs(cp.optional, False)
		self.assertIs(cp.count_type, None)

	def test___init___not_callable(self):
		"""Test that a non-callable validator is an error."""

		args = ["test", None]

		self.assertRaises(TypeError, CommandParameter, *args)

	def test___init___neg_count(self):
		"""Test that a negative count is an error."""

		args = ["test", something_bad]
		kwargs = {"count": -1}

		self.assertRaises(AttributeError, CommandParameter, *args, **kwargs)

	def test___init___non_int_count(self):
		"""Test that a non-integer count is an error."""

		args = ["test", something_bad]
		kwargs = {"count": 3.14159}

		self.assertRaises(TypeError, CommandParameter, *args, **kwargs)

	def test___init___missing_count_type(self):
		"""Test that for count > 1, the count type is required."""

		args = ["test", something_bad]
		kwargs = {"count": 3}

		self.assertRaises(AttributeError, CommandParameter, *args, **kwargs)

	def test___init___nonsense_count_type(self):
		"""Test that for count == 0, the count type must be min."""

		args = ["test", something_bad]
		kwargs = {"count": 0}

		self.assertRaises(AttributeError, CommandParameter, *args, **kwargs)

	def test_validate_optional(self):
		"""Test that an optional parameter can be missing."""

		cp = CommandParameter("test", something_bad, optional=True)

		self.assertIs(cp.validate(None), None)

	def test_validate_no_count_type(self):
		"""Test that we can validate a single value when no count type."""

		cp = CommandParameter("test", something_good)

		self.assertIs(cp.validate("anything"), None)

	def test_validate_count_exceeded(self):
		"""Test that we don't exceed the count on CountType.MAX."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.MAX)

		error = cp.validate([1, 2, 3])

		self.assertIsNot(error, None)

	def test_validate_count_below(self):
		"""Test that we don't come below the count on CountType.MIN."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.MIN)

		error = cp.validate([1])

		self.assertIsNot(error, None)

	def test_validate_count_exact(self):
		"""Test that we get the exact count on CountType.EXACT."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)

		error = cp.validate([1])

		self.assertIsNot(error, None)

	def test___repr___round_trippable(self):
		"""Test that __repr__ can be round-tripped."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)
		cp2 = eval(repr(cp))

		self.assertEquals(cp, cp2)

	def test___eq___equal(self):
		"""Test that two equal CommandParameters can test for equality."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)
		cp2 = eval(repr(cp))

		self.assertTrue(cp == cp2)

	def test___eq___inequal(self):
		"""Test that two inequal CommandParameters can test for equality."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)
		cp2 = eval(repr(cp))
		cp2.name = "not test"

		self.assertFalse(cp == cp2)

	def test___ne___equal(self):
		"""Test that two equal CommandParameters can test for inequality."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)
		cp2 = eval(repr(cp))

		self.assertFalse(cp != cp2)

	def test___ne___inequal(self):
		"""Test that two inequal CommandParameters can test for inequality."""

		cp = CommandParameter(
			"test", something_good, count=2, count_type=CountType.EXACT)
		cp2 = eval(repr(cp))
		cp2.name = "not test"

		self.assertTrue(cp != cp2)

class TestExecutableCommandMixin(unittest.TestCase):

	def test_register_execution(self):
		"""Test that an execution can be registered."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def test_func():
			return None

		self.assertIs(ExecutableCommandMixinTester.TESTPROPERTY.execution, test_func)

	def test_register_execution_overwrite(self):
		"""Test that an execution can be overwritten."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def test_func():
			return None

		self.assertIs(ExecutableCommandMixinTester.TESTPROPERTY.execution, test_func)

		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def test_func_2():
			return "something bad"

		self.assertIs(ExecutableCommandMixinTester.TESTPROPERTY.execution, test_func_2)

	def test_register_parameter(self):
		"""Test that a parameter can be registered."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, optional=True)
		def validate_func(param):
			return None

		cps = CommandParameterSet(
			CommandParameter("test", validate_func, optional=True))

		self.assertEquals(
			ExecutableCommandMixinTester.TESTPROPERTY.parameters, cps)

	def test_register_parameter_overwrite(self):
		"""Test that a parameter can be overwritten."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, optional=True)
		def validate_func(param):
			return None
		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, count=4, count_type=CountType.MAX)
		def validate_func_2(param):
			return "something good"

		cps = CommandParameterSet(
			CommandParameter(
				"test", validate_func_2, count=4, count_type=CountType.MAX))

		self.assertEquals(
			ExecutableCommandMixinTester.TESTPROPERTY.parameters, cps)

	def test_register_validator(self):
		"""Test that an overall validator can be registered."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_validator
		def validate_parameters(param):
			return [None]

		self.assertIs(
			ExecutableCommandMixinTester.TESTPROPERTY.validator,
			validate_parameters)

	def test_execute_command_invalid_args(self):
		"""Test that there is an error if the parameters are invalid."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter("test", 0)
		def validate_func(param):
			return "something bad"
		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def execute_func(value):
			return "something good"

		self.assertRaises(
			InvalidCommandParametersException,
			ExecutableCommandMixinTester.TESTPROPERTY.execute_command)

	def test_execute_command_valid_args(self):
		"""Test that there is no error if the parameters are valid."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, optional=True)
		def validate_func(param):
			return None
		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def execute_func(value):
			return "something good"

		self.assertEquals(
			ExecutableCommandMixinTester.TESTPROPERTY.execute_command(None),
			"something good")

	def test_execute_command_valid_args_overall(self):
		"""
		Test that there is no error if the parameters are valid
		overall.
		"""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, optional=True)
		def validate_func(param):
			return None
		@ExecutableCommandMixinTester.TESTPROPERTY.register_validator
		def validate_overall(param):
			return []
		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def execute_func(value):
			return "something good"

		self.assertEquals(
			ExecutableCommandMixinTester.TESTPROPERTY.execute_command(None),
			"something good")

	def test_execute_command_invalid_args_overall(self):
		"""
		Test that there is an error if the parameters are not valid
		overall.
		"""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_parameter(
			"test", 0, optional=True)
		def validate_func(param):
			return None
		@ExecutableCommandMixinTester.TESTPROPERTY.register_validator
		def validate_overall(param):
			return ["Something bad"]
		@ExecutableCommandMixinTester.TESTPROPERTY.register_execution
		def execute_func(value):
			return "something good"

		self.assertRaises(
			InvalidCommandParametersException,
			ExecutableCommandMixinTester.TESTPROPERTY.execute_command,
			"test_value")

	def test_register_error_handler_callable(self):
		"""Test that the handler can be a function."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_error_handler(
			"I AM A COOL ERROR CODE")
		def handle_error(command, error):
			return command, error

		# No error, yay!

	def test_register_error_handler_exception(self):
		"""Test that the handler can be an exception."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_error_handler(
			"I AM A COOL ERROR CODE")
		class CustomException(Exception): pass

		# No error, yay!

	def test_register_error_handler_invalid(self):
		"""Test that the handler can't be non-callable."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		dec = ExecutableCommandMixinTester.TESTPROPERTY.register_error_handler(
			"I AM A COOL ERROR CODE")

		self.assertRaises(TypeError, dec, "I AM NOT CALLABLE")

	def test_handle_error_function(self):
		"""Test that an error handler function is called."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_error_handler(
			"I AM A COOL ERROR CODE")
		def handle_error(command, error):
			return command, error

		self.assertEquals(
			handle_error(ExecutableCommandMixinTester.TESTPROPERTY,
						 "I AM A COOL ERROR CODE"),
			ExecutableCommandMixinTester.TESTPROPERTY.handle_error(
				"I AM A COOL ERROR CODE"))

	def test_handle_error_exception(self):
		"""Test that an error handler exception is raised."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		@ExecutableCommandMixinTester.TESTPROPERTY.register_error_handler(
			"I AM A COOL ERROR CODE")
		class CustomException(Exception): pass

		self.assertRaises(
			CustomException,
			ExecutableCommandMixinTester.TESTPROPERTY.handle_error,
			"I AM A COOL ERROR CODE")

	def test_handle_error_none(self):
		"""Test that the handler must be present."""

		class ExecutableCommandMixinTester(ExecutableCommandMixin, enum.Enum):
			TESTPROPERTY = 1

		self.assertRaises(
			NoHandlerExcepetion,
			ExecutableCommandMixinTester.TESTPROPERTY.handle_error,
			"I AM ANY UNREGISTERED ERROR CODE")
