from django.conf import settings
from django import template

from time import time

"""
Always ensure breakpoints are off when the django app
has been deployed, which implies settings.DEBUG=False

Note that PEP553 was implemented in python 3.7+
This means a built-in breakpoint() function exists to
replace the 'import pdb; pdb.set_trace()' idiom.

All breakpoint() functions in code can be ignored by
setting PYTHONBREAKPOINT=0 in the execution environment.
This is great for disabling any stray breakpoint
methods left in code, specifically development code
as we gurantee they will be off in production code
by leveraging the settings.py DEBUG environment variable.

"""


""" get an instance of the template library for filter registration """
register = template.Library()


def __breakpoint__(enable=True):
    """ macro to set a breakpoint anywhere inline """
    if settings.DEBUG and enable:
        breakpoint()


def pdb(function):
    """ decorator to set a breakpoint at the beginning of a function.

    Since a decorator effectively wraps a function to execute code
    before and/or after a function, those are our options to set
    a breakpoint with a decorator. Since we can type r(eturn) into
    pdb to run to the end of a function, it only makes sense to
    set the breakpoint at the beginning of any function that uses
    this decorator.

    Note that decorators run at two different stages
    1) the outer most part when a callable is decorated
    2) the inner most part when the callable is executed.

    """

    def wrapped(*args, **kwargs):
        if settings.DEBUG:
            breakpoint()
        return function(*args, **kwargs)

    return wrapped


def timeit(function):
    """ Decorator for printing function execution time. """
    def timed(*args, **kwargs):
        ts = time()
        result = function(*args, **kwargs)
        te = time()
        print("{0} ({1}, {2}) {3:.2} sec"
              .format(function.__name__, args, kwargs, te - ts))
        return result
    return timed


def logtime(function):

    def wrapper(*args, **kwargs):
        ts = time()
        result = function(*args, *kwargso)
        tt = time() - ts

        with open('/tmp/timelog.txt', 'a') as out:
            out.write(f'{time()}\t{function.__name__}\t{tt}')

        return result
    return wrapper


