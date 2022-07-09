# +====================================================================================================================+
# Pythonic
import inspect
# +====================================================================================================================+


def current_function():
    """Return the string name of the function we are calling this from."""
    frame = inspect.currentframe()
    return inspect.getouterframes(frame)[1].function
