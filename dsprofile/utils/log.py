import functools
import logging
import types

from dsprofile import config
from dsprofile.lib import Reader

logger = config.getLogger()


def logged(*dargs, time=False):
    """
      Decorator which causes its wrapped function to emit
      a log message when invoked.
    """
    level_map = logging.getLevelNamesMapping()
    level_num = level_map["INFO"]
    func_is_arg = len(dargs) > 0 and isinstance(dargs[0], types.FunctionType)
    if not func_is_arg:
        for darg in dargs:
            if not isinstance(darg, str):
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
