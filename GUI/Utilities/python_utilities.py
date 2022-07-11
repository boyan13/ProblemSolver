# +====================================================================================================================+
# Pythonic
import inspect
from operator import itemgetter
# +====================================================================================================================+


def current_function(go_back=1):
    """Return the string name of the function we are calling this from."""
    frame = inspect.currentframe()
    return inspect.getouterframes(frame)[go_back].function


def get_multiple(gettable, *keys):
    """Get all the values of the object matching the given keys and return them in a tuple. Always returns a tuple."""
    result = itemgetter(*keys)(gettable)

    if result is None:
        return tuple()
    elif type(result) is not tuple:
        return (result, )
    else:
        return result
