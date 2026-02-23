from abc import (
    ABC,
    abstractmethod
)


reader_type_map = {}


class Reader(ABC):
    """
      An abstract base for all Reader types.
    """

    subclass_type_key = "format"

    def __init_subclass__(cls, /, **kwargs):
        super().__init_subclass__(**kwargs)
        keyattr = __class__.subclass_type_key
        reader_type = getattr(cls, keyattr, None)
        if not reader_type or not isinstance(reader_type, str):
            raise NotImplementedError(f"Reader subclass {cls.__qualname__} "
                                      f"does not define a {reader_type} key")
        reader_type_map[reader_type] = cls


    @abstractmethod
    def process(self):
        pass

    @classmethod
    @abstractmethod
    def handle_args(cls, args):
        pass


def make_reader(args):
    cls = reader_type_map[args.command]
    ctor_args, ctor_kwargs = cls.handle_args(args)
    return cls(*ctor_args, **ctor_kwargs)
