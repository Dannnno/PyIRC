import warnings
import textwrap

def raises(func, allowed_exceptions, *args, **kwargs):
    """Determine whether or not a function raises an exception.

    Parameters
    ----------
    func: function(*args, **kwargs) -> object
        Function to test; can take any arbitrary parameters.
    allowed_exceptions: tuple[BaseException]
        Tuple of the expected exceptions.
    args: list[object]
        All of the arguments to be passed to the function.
    kwargs: dict[object: object]
        All of the keyword arguments to be passed to the function.

    Returns
    -------
    boolean
        Whether or not the function raises the given exceptions.
    """

    try:
        func(*args, **kwargs)
    except allowed_exceptions:
        return True
    return False

IGNORED_EXCEPTIONS = [
    KeyboardInterrupt,
    MemoryError,
    StopIteration,
    SystemError,
    SystemExit,
    GeneratorExit
]
try:
    IGNORED_EXCEPTIONS.append(StopAsyncIteration)
except NameError:
    pass
IGNORED_EXCEPTIONS = tuple(IGNORED_EXCEPTIONS)

def is_raisable(exception, exceptions_to_exclude=IGNORED_EXCEPTIONS):
    """Determine whether or not something can be raised as an exception.

    Parameters
    ----------
    exception: Exception
        Exception to attempt to raise.
    exceptions_to_include: tuple, default=IGNORED_EXCEPTIONS
        Exceptions that we should ignore when testing if its raisable.
        These are things that are more likely to happen behind the
        scenes outside of user control; if they want to test if they're
        raisable then they should know that they're testing for that.

    Notes
    -----
    There is very little that can be done to detect an error that occurs
    while attempting to raise an otherwise valid error, e.g. if the
    passed-in `exception` is an instance of an old-style class, and it
    raises an error we'd typically plan on excluding during its own
    construction.

    Similarly, we can't really detect a difference between an error
    during an exception's construction and the error itself.

    These situations should be exceedingly rare, and are much more
    likely to be a problem with the custom exception.

    Returns
    -------
    boolean
        Whether or not the exception is raiseable.
    """

    funcs_to_try = (isinstance, issubclass)
    can_raise = False

    try:
        can_raise = issubclass(exception, BaseException)
    except TypeError:
        # issubclass doesn't like when the first parameter isn't a type
        pass

    if can_raise or isinstance(exception, BaseException):
        return True

    # Handle old-style classes
    try:
        raise exception
    except TypeError as e:
        # It didn't raise, so it must not be raisable unless exception was a
        # TypeError, which could only happen if there was a bizarre, and
        # potentially impossible, class hierarchy existed
        return exception is e or isinstance(exception, TypeError)
    except exceptions_to_exclude as e:
        # These are errors that are unlikely to be explicitly tested here,
        # and if they were we would have caught them before, so percolate up
        raise
    except:
        # Must be bare, otherwise no way to reliably catch an instance of an
        # old-style class

        warnings.warn(
            textwrap.dedent(
                """The passed-in parameter appears to be an old-style class that
                doesn't inherit from BaseException. This is probably a bug with
                the custom exception type, but is technically raisable."""))
        return True
