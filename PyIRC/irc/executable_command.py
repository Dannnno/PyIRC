# Force Python 3 behaviors
from __future__ import print_function, unicode_literals, absolute_import

try:
	import enum34 as enum
except ImportError:
	import enum

try:
	from itertools import izip as zip
except ImportError:
	pass

try:
	range = xrange
except NameError:
	pass

from collections import defaultdict
from itertools import izip_longest

__all__ = [
	"InvalidCommandParametersException", "CommandParameterSet",
	"CommandParameter", "CountType", "ExecutableCommandMixin"]


class InvalidCommandParametersException(Exception):
	"""Raised when the parameters to a command are invalid."""

	def __init__(self, command, param_problems):
		"""Raise an error that a command's parameters are invalid.

		Parameters
		----------
		command: Command
			The command type that failed validation.
		param_problems: iterable[string]
			Collection of problems with the parameters
		"""

		message = '\n'.join(["Command: {}".format(command.name)] + param_problems)
		super(InvalidCommandParametersException, self).__init__(message)


class CommandParameterSet(object):
	"""A set of parameters to a command."""

	def __init__(self, *parameters):
		"""Create a new CommandParameterSet.

		Parameters
		----------
		parameters: iterable[CommandParameter]
			Collection of parameters that we expect to see. Must be an
			empty list if no parameters expected.
		"""

		self.parameters = list(parameters) or []

	def insert_parameter(self, parameter, index=None):
		"""Add another parameter to the parameter list in the given
		location, or append if not specified.

		We can't guarantee the order in which the decorators will 
		execute, so this is a little flexible. If you insert at a
		greater index than is currently supported, we'll fill it out
		with `None` until we can fit it in. If you insert at a location
		that is already populated we just replace it.

		Parameters
		----------
		parameter: CommandParameter
			A parameter to insert into this set.
		index: indexer, default=None
			Where to insert the parameter; if None then just append it.
		"""

		if index is None:
			index = len(self.parameters)
		if index < 0:
			raise IndexError(
				"CommandParameterSet doesn't support negative indices")
		
		diff = index - len(self.parameters)
		if diff == 0:
			self.parameters.append(parameter)
		elif diff > 0:
			self.parameters.extend([None]*diff + [parameter])
		else:
			self.parameters[index] = parameter

	def validate(self, values):
		"""Check if the given values pass parameter validation.

		We have to have filled in all of the parameters; if any are
		`None` then this will fail as well.

		Parameters
		----------
		values: iterable[Object]
			Collection of the values that we expect to see. Must be an
			empty list if no values to check.

		Returns
		-------
		result: generator[string]
			Yields all of the errors found; if none, then an empty generator
			is returned.
		"""

		if any(param is None for param in self.parameters):
			yield "Not all parameters are populated."
		elif len(values) != len(self.parameters):
			yield "Expected {} parameters, got {}".format(
				len(self.parameters), len(values))
		else:
			for i, (val, param) in enumerate(zip(values, self.parameters)):
				problem = param.validate(val)
				if problem:
					yield "{i}-{name} was {val} but {problem}".format(
						name=param.name, **locals())

	def __str__(self):
		"""Returns a string representation of the set."""

		return "CommandParameterSet[{}]".format(len(self.parameters))

	def __unicode__(self):
		"""Returns the unicode string representation of the set."""

		return unicode(str(self))

	def __repr__(self):
		"""Returns a round-trippable representation of the set."""

		return "CommandParameterSet({})".format(
					", ".join(repr(param) for param in self.parameters))

	def __eq__(self, other):
		"""Check whether or not two CommandParameterSets are equal."""

		if len(self) != len(other):
			return False

		return all(me == them for me, them in izip_longest(self, other, fillvalue=None))

	def __ne__(self, other):
		"""Check whether or not two CommandPArameterSets are not equal."""

		return not (self == other)

	def __len__(self):
		"""Returns the number of parameters in the set."""

		return len(self.parameters)

	def __iter__(self):
		"""Return an iterator for this command parameter set."""

		for param in self.parameters:
			yield param


@enum.unique
class CountType(enum.Enum):
	"""Possible types of "counts" we could have.

	Attributes
	----------
	MAX
		The given "count" is the most allowed.
	MIN
		The given "count" is the least allowed.
	EXACT
		The given "count" is exactly the number expected.
	"""

	MAX = 1
	MIN = 2
	EXACT = 3


class CommandParameter(object):
	"""Parameter to a command.

	Can specify validation code and options for validation.
	"""

	def __init__(self, name, validator, optional=False, count_type=None, count=1):
		"""Create a new CommandParameter.

		Parameters
		----------
		name: string
			Name of the parameter; used to describe the parameter.
		validator: function(value) -> string | None
			Function that takes in a value and returns an error message,
			or None if it was okay. If there are multiple values allowed
			(i.e. `count_type != None`) then this is called for each 
			item in the collection, _instead_ of on the entire 
			collection.
		optional: boolean, default=False
			Whether or not the parameter is optional. If it is optional,
			then `None` should be passed for validation.
		count_type: CountType, default=None
			Required if a `count` is given; describes how to interpret 
			the count (as a max, min, or exact requirement).
		count: integer, default=1
			Describes how many instances of this value are allowed. If 
			greater than 1, then `count_type` is required. If 0 or more
			are allowed, then pass `count=0` and
			`count_type=CountTypes.MIN`
		"""

		self.name = name
		self.validator = validator
		self.optional = optional
		self.count = count
		self.count_type = count_type

		if not callable(validator):
			raise TypeError("Validator must be callable")
		if count < 0:
			raise AttributeError("Count must be positive; was {}".format(count))
		if int(count) != count:
			raise TypeError("Count must be an integer; was {}".format(count))
		if count > 1 and count_type is None:
			raise AttributeError(
				"Count type is required if multiple values are allowed.")
		if count == 0 and count_type is not CountType.MIN:
			raise AttributeError(
				"Count and count type would require 0 or fewer values.")

	def validate(self, value):
		"""Check if the given value satisfies this parameter.

		Parameters
		----------
		value: Object
			The value to check for this parameter.

		Returns
		-------
		result: string|None
			None if the result is okay, otherwise an error message.
		"""

		if self.optional and value is None:
			return None

		if not self.count_type:
			return self.validator(value)
		elif self.count_type == CountType.MAX and len(value) > self.count:
			return "Expected no more than {} parameters, but got {}".format(
				self.count, len(value))
		elif self.count_type == CountType.MIN and len(value) < self.count:
			return "Expected no less than {} parameters, but got {}".format(
				self.count, len(value))
		elif len(value) != self.count:
			return "Expected exactly {} parameters, but got {}".format(
				self.count, len(value))
			
		return None

	def __str__(self):
		"""Returns a string representation of the parameter."""

		return "CommandParameter"

	def __unicode__(self):
		"""Returns the unicode string representation of the set."""

		return unicode(str(self))

	def __repr__(self):
		"""Returns a round-trippable representation of the set."""

		return \
			"CommandParameter('{}', {}, optional={}, count_type={}, count={})"\
			.format(
				self.name, self.validator.__name__, self.optional, 
				self.count_type, self.count)

	def __eq__(self, other):
		"""Check whether or not two CommandParameters are equal."""

		try:
			return (self.name == other.name 
				and self.validator is other.validator
				and self.optional is other.optional
				and self.count_type is other.count_type
				and self.count == other.count)
		except AttributeError:
			raise TypeError(
				"CommandParameter and type <{}> can't be compared.".format(
					type(other)))

	def __ne__(self, other):
		"""Check whether or not two CommandParameters are not equal."""

		return not (self == other)


class ExecutableCommandMixin(object):
	"""Mixin to make an enum of commands executable.

	Enables parameterizing a given command and specifying how to 
	validate each parameter, as well as specifying what "executing" the
	command means. Does so by providing decorator functions that will
	register functions as parameter validation or command execution.

	Notes
	-----
	Does not subclass from `enum.Enum` because working around the
	non-extensibility of enums with defined members is pretty inelegant.

	Properties
	----------
	parameters: CommandParameterSet
		Set of parameters for this command.
	execution: function(*values) -> Object
		Function that takes in the parameters and returns something.
	"""

	@property
	def parameters(self):
		return self.__class__._parameters[self]

	_executions = {}
	@property
	def execution(self):
		return self.__class__._executions[self]

	def execute_command(self, *values):
		problems = self._validate_arguments(values)
		if problems:
			raise InvalidCommandParametersException(self, problems)

		return self.execution(*values)

	def register_execution(self, func):
		"""Register a function as this command's action.

		Parameters
		----------
		func: function
			Function to execute for this parameter.

		Returns
		-------
		func: function
			The original function, unchanged.
		"""

		self.__class__._executions[self] = func
		return func

	_parameters = defaultdict(CommandParameterSet)
	def register_parameter(self, name, n_th, optional=False, count=1, count_type=None):
		"""Decorator to register a function to validate a given parameter.

		Parameters
		----------
		name: string
			Name of the parameter; used to describe the parameter.
		n_th: indexer
			Which parameter this should be in the parameter list.
		optional: boolean, default=False
			Whether or not the parameter is optional. If it is optional,
			then `None` should be passed for validation.
		count: integer, default=1
			Describes how many instances of this value are allowed. If 
			greater than 1, then `count_type` is required. If 0 or more
			are allowed, then pass `count=0` and
			`count_type=CountTypes.MIN`
		count_type: CountType, default=None
			Required if a `count` is given; describes how to interpret 
			the count (as a max, min, or exact requirement).

		Returns
		-------
		decorator: function -> function
			Wrapper function that wraps its argument function and adds
			it as validation for this parameter
		"""

		def decorator(validator):
			"""Add the actual validator function for this parameter.

			Parameters
			----------
			validator: function(value) -> string | None
				Function that takes in a value and returns an error 
				message, or None if it was okay. If there are multiple 
				values allowed (i.e. `count_type != None`) then this is 
				called for each item in the collection, _instead_ of on 
				the entire collection.

			Returns
			-------
			validator: function(value) -> string | None
				The original function, unchanged.
			"""

			self.__class__._parameters[self].insert_parameter(
				CommandParameter(name, validator, optional=optional, 
					count=count, count_type=count_type),
				n_th)

			return validator

		return decorator

	def _validate_arguments(self, arguments):
		"""Validate the command's arguments.

		Parameters
		----------
		arguments: collection[Object]
			List of the arguments being passed.

		Returns
		-------
		list[string]
			List of all of the problems with the arguments. Will be an
			empty list if no problems are present.
		"""

		errors = list(self.__class__._parameters[self].validate(arguments))

		if not errors or all(err is None for err in errors):
			return []
		return errors