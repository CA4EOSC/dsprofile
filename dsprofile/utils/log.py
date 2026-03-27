import functools
import logging
import types

from dsprofile import config
from dsprofile.lib import Reader

logger = config.getLogger()


def logged(*dargs, time=False):
    """
      Decorator which causes its wrapped Reader member-function
      to emit a log message when invoked.

      When applied with no arguments, this causes the wrapped
      function to be preceeded by a INFO message which contains
      the classname and function name called.

      When applied with a single positional argument corresponding
      to a log level name, the message is emitted at the specified
      level.

      When the `time=True` kwarg is provided, this causes two
      messages to be emitted, one before and one after the wrapped
      function call. The time difference between these indicates
      the duration of the call, making this useful for profiling
      long-running operations on large datasets,

      See tests/test_logging.py for usage examples.
    """
    level_map = logging.getLevelNamesMapping()
    level_num = level_map["INFO"]
    """
      If no args are provided to the decorator, the first darg received
      here will be the wrapped function itself so this must be
      identified and handled.
    """
    func_is_arg = len(dargs) > 0 and isinstance(dargs[0], types.FunctionType)
    if not func_is_arg:
        for darg in dargs:
            if not isinstance(darg, str):
                continue
            if darg not in level_map:
                continue
            if num := level_map.get(darg.upper()):
                level_num = num
    time_txt = " start" if time else ""

    def m_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(self, Reader):
                logger.log(level_num, f"{self.__class__.__qualname__}.{func.__name__}{time_txt}")
            if time:
                ret = func(self, *args, **kwargs)
                logger.log(level_num, f"{self.__class__.__qualname__}.{func.__name__} end")
                return ret
            else:
                return func(self, *args, **kwargs)

        return wrapper

    if func_is_arg:
        return m_wrapper(dargs[0])
    return m_wrapper
